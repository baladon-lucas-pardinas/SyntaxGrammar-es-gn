#!/bin/bash
#==============================================================================
# Submit stage-3-only 8B training job (train_only.sbatch) with timestamped
# output directory and synthetic-mode passthrough.
#
# Usage:
#   ./slurm/submit_train_only.sh <MODEL_PATH> [SPLITS_DIR] [OUTPUT_DIR] [PARTITION] [QOS] [GPU_TYPE]
#
# Examples:
#   ./slurm/submit_train_only.sh models/qwen-guarani-initialized
#   SYNTHETIC_MODE=mixed SYNTHETIC_PROPORTION=0.5 \
#     ./slurm/submit_train_only.sh models/qwen-guarani-initialized data/splits
#==============================================================================

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(realpath "$SCRIPT_DIR/..")"

MODEL_PATH="${1:?ERROR: provide MODEL_PATH (initialized model path)}"
SPLITS_DIR="${2:-$PROJECT_ROOT/data/splits}"

MODE_TAG="${SYNTHETIC_MODE:-real_only}"
STAMP="$(date +%y%m%d-%H%M)"
OUTPUT_DIR="${3:-$PROJECT_ROOT/models/$(basename "$MODEL_PATH")-${MODE_TAG}-${STAMP}}"

PARTITION="${4:-nlprx-lab}"
QOS="${5:-short}"
GPU_TYPE="${6:-a40}"

if [[ "$PARTITION" != "nlprx-lab" && "$PARTITION" != "overcap" ]]; then
  echo "ERROR: PARTITION must be nlprx-lab or overcap"
  exit 1
fi

if [[ "$QOS" != "debug" && "$QOS" != "short" && "$QOS" != "long" ]]; then
  echo "ERROR: QOS must be debug, short, or long"
  exit 1
fi

ACCOUNT="nlprx-lab"
if [[ "$PARTITION" == "overcap" ]]; then
  ACCOUNT="overcap"
fi

GPU_GRES="gpu:1"
if [[ "$GPU_TYPE" != "none" ]]; then
  GPU_GRES="gpu:${GPU_TYPE}:1"
fi

TRAIN_WALLTIME="${TRAIN_WALLTIME:-36:00:00}"

mkdir -p "$PROJECT_ROOT/logs/slurm"

echo "========================================"
echo "Submitting 8B Stage-3 Training Only"
echo "========================================"
echo "Model path: $MODEL_PATH"
echo "Splits dir: $SPLITS_DIR"
echo "Output dir: $OUTPUT_DIR"
echo "Synthetic mode: ${SYNTHETIC_MODE:-real_only}"
if [[ -n "${SYNTHETIC_PROPORTION:-}" ]]; then
  echo "Synthetic proportion: ${SYNTHETIC_PROPORTION}"
else
  echo "Synthetic proportion: auto (use all available synthetic in mixed mode)"
fi
if [[ -n "${SYNTHETIC_STAGE1_WHITESPACE_TOKENS:-}" ]]; then
  echo "Stage-1 synthetic token budget: ${SYNTHETIC_STAGE1_WHITESPACE_TOKENS}"
fi
echo "Partition: $PARTITION"
echo "QOS: $QOS"
echo "Account: $ACCOUNT"
echo "GPU GRES: $GPU_GRES"
echo "Walltime: $TRAIN_WALLTIME"
echo "========================================"

JOB_ID=$(sbatch --parsable \
  --account="$ACCOUNT" \
  --partition="$PARTITION" \
  --qos="$QOS" \
  --gres="$GPU_GRES" \
  --time="$TRAIN_WALLTIME" \
  --job-name="guarani-train-only" \
  --output="$PROJECT_ROOT/logs/slurm/train-only-%j.out" \
  --error="$PROJECT_ROOT/logs/slurm/train-only-%j.err" \
  --export=ALL \
  "$PROJECT_ROOT/slurm/train_only.sbatch" \
  "$MODEL_PATH" \
  "$SPLITS_DIR" \
  "$OUTPUT_DIR")

echo "Submitted job: $JOB_ID"
echo "Monitor with: squeue -j $JOB_ID"
