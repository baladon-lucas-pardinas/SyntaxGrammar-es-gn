#!/bin/bash
#==============================================================================
# SLURM Job Script: 2x2LS Training Only
#
# Use this script when you already have:
#   1. Extended tokenizer (in tokenizers/)
#   2. Initialized model (in models/)
#
# This is useful for:
#   - Resuming training from a checkpoint
#   - Re-running training with different hyperparameters
#   - Running on a different split selection
#
# Usage:
#   sbatch slurm/train_only.sbatch <MODEL_PATH> [SPLITS_DIR] [OUTPUT_DIR]
#
# Example:
#   sbatch slurm/train_only.sbatch models/Qwen3-0.6B-guarani-initialized data/splits
#
#==============================================================================

#SBATCH --job-name=guarani-train
#SBATCH --output=logs/slurm/train-%j.out
#SBATCH --error=logs/slurm/train-%j.err

# --- Resource Allocation ---
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --mem=48G
#SBATCH --time=36:00:00

# --- Queue/Partition (uncomment and modify as needed) ---
##SBATCH --partition=gpu
##SBATCH --qos=normal

#==============================================================================
# Configuration
#==============================================================================

MODEL_PATH="${1:?ERROR: Please provide MODEL_PATH as first argument}"
SPLITS_DIR="${2:-data/splits}"
OUTPUT_DIR="${3:-${MODEL_PATH}-tuned}"

TRAIN_ON="${TRAIN_ON:-train}"
EVAL_ON="${EVAL_ON:-none}"
SYNTHETIC_MODE="${SYNTHETIC_MODE:-real_only}"
SYNTHETIC_PROPORTION="${SYNTHETIC_PROPORTION:-}"
SYNTHETIC_STAGE1_WHITESPACE_TOKENS="${SYNTHETIC_STAGE1_WHITESPACE_TOKENS:-}"

# Training hyperparameters
NUM_EPOCHS=${NUM_EPOCHS:-2}
BATCH_SIZE=${BATCH_SIZE:-4}
GRADIENT_ACCUMULATION_STEPS=${GRADIENT_ACCUMULATION_STEPS:-2}
LEARNING_RATE=${LEARNING_RATE:-1e-4}
MAX_SEQ_LENGTH=${MAX_SEQ_LENGTH:-512}
WARMUP_RATIO=${WARMUP_RATIO:-0.05}

# HuggingFace caches (cluster: put all heavy I/O on flash, not $HOME/.cache)
export HF_HOME="${HF_HOME:-/nethome/alucas63/flash/huggingface}"
export HF_DATASETS_CACHE="${HF_DATASETS_CACHE:-/nethome/alucas63/flash/huggingface/datasets}"
export TRANSFORMERS_CACHE="${TRANSFORMERS_CACHE:-/nethome/alucas63/flash/huggingface/transformers}"

# Enable TF32
export NVIDIA_TF32_OVERRIDE=1

#==============================================================================
# Setup
#==============================================================================

echo "========================================"
echo "2x2LS Training Job"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURMD_NODENAME"
echo "Start Time: $(date)"
echo "========================================"
echo ""
echo "Configuration:"
echo "  Model path:  $MODEL_PATH"
echo "  Splits dir:  $SPLITS_DIR"
echo "  Train-on:    $TRAIN_ON"
echo "  Eval-on:     $EVAL_ON"
echo "  Synthetic mode: $SYNTHETIC_MODE"
if [ -n "$SYNTHETIC_PROPORTION" ]; then
  echo "  Synthetic proportion: $SYNTHETIC_PROPORTION"
else
  echo "  Synthetic proportion: auto (use all available synthetic in mixed mode)"
fi
if [ -n "$SYNTHETIC_STAGE1_WHITESPACE_TOKENS" ]; then
  echo "  Stage-1 synthetic token budget: $SYNTHETIC_STAGE1_WHITESPACE_TOKENS"
fi
echo "  Output:      $OUTPUT_DIR"
echo "  Epochs:      $NUM_EPOCHS"
echo "  Batch size:  $BATCH_SIZE"
echo "  LR:          $LEARNING_RATE"
echo "========================================"
echo ""

cd "$SLURM_SUBMIT_DIR" || exit 1
mkdir -p logs/slurm
mkdir -p "$OUTPUT_DIR"

# Setup Python environment
if command -v uv &> /dev/null; then
    uv sync
    PYTHON_CMD="uv run python"
elif [ -d ".venv" ]; then
    source .venv/bin/activate
    PYTHON_CMD="python"
else
    echo "ERROR: No Python environment found!"
    exit 1
fi

# Verify GPU
$PYTHON_CMD -c "import torch; print(f'GPU: {torch.cuda.get_device_name(0)}' if torch.cuda.is_available() else 'WARNING: No GPU!')"

#==============================================================================
# Training
#==============================================================================

TRAIN_CMD="$PYTHON_CMD -m guarani_llm.train_2x2ls \
    --model-path \"$MODEL_PATH\" \
    --splits-dir \"$SPLITS_DIR\" \
    --train-on $TRAIN_ON \
    --output-dir \"$OUTPUT_DIR\" \
    --num-epochs \"$NUM_EPOCHS\" \
    --batch-size \"$BATCH_SIZE\" \
    --gradient-accumulation-steps \"$GRADIENT_ACCUMULATION_STEPS\" \
    --learning-rate \"$LEARNING_RATE\" \
    --warmup-ratio \"$WARMUP_RATIO\" \
    --max-seq-length \"$MAX_SEQ_LENGTH\" \
    --synthetic-mode \"$SYNTHETIC_MODE\""

if [ -n "$SYNTHETIC_PROPORTION" ]; then
    TRAIN_CMD="$TRAIN_CMD --synthetic-proportion \"$SYNTHETIC_PROPORTION\""
fi

if [ "$EVAL_ON" != "none" ] && [ -n "$EVAL_ON" ]; then
    TRAIN_CMD="$TRAIN_CMD --eval-on $EVAL_ON"
fi
if [ -n "$SYNTHETIC_STAGE1_WHITESPACE_TOKENS" ]; then
    TRAIN_CMD="$TRAIN_CMD --synthetic-stage1-whitespace-tokens $SYNTHETIC_STAGE1_WHITESPACE_TOKENS"
fi

eval $TRAIN_CMD

echo ""
echo "========================================"
echo "Training complete!"
echo "Model saved to: $OUTPUT_DIR"
echo "End Time: $(date)"
echo "========================================"
