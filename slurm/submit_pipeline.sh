#!/bin/bash
#==============================================================================
# Submit a CPU-only Spanish->Guarani pipeline job with partition/QOS validation
# and interactive prompts for the requested worker count.
#
# Usage:
#   ./slurm/submit_pipeline.sh [MODE]
#
# Examples:
#   ./slurm/submit_pipeline.sh synthetic
#   ./slurm/submit_pipeline.sh corpus
#==============================================================================

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(realpath "$SCRIPT_DIR/..")"
STAMP="$(date +%y%m%d-%H%M%S)"

prompt_with_default() {
  local prompt_text="$1"
  local default_value="$2"
  local result_var="$3"
  local reply=""

  read -r -p "$prompt_text [$default_value]: " reply
  printf -v "$result_var" '%s' "${reply:-$default_value}"
}

MODE="${1:-}"
if [[ -z "$MODE" ]]; then
  prompt_with_default "Pipeline mode (synthetic/corpus)" "corpus" MODE
fi

if [[ "$MODE" != "synthetic" && "$MODE" != "corpus" ]]; then
  echo "ERROR: MODE must be synthetic or corpus"
  exit 1
fi

RUN_NAME_DEFAULT="${MODE}-$(date +%y%m%d-%H%M)"
prompt_with_default "Run name" "$RUN_NAME_DEFAULT" RUN_NAME

OUTPUT_DIR_DEFAULT="$PROJECT_ROOT/runs"
prompt_with_default "Output directory" "$OUTPUT_DIR_DEFAULT" OUTPUT_DIR

prompt_with_default "Requested CPU count" "8" CPUS
prompt_with_default "Partition" "nlprx-lab" PARTITION
prompt_with_default "QOS" "short" QOS
prompt_with_default "Memory" "48G" MEMORY
prompt_with_default "Walltime" "36:00:00" WALLTIME

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

PIPELINE_INPUT=""
PIPELINE_FORMAT_INPUT="0"
PIPELINE_FORMATTED_INPUT=""
PIPELINE_SEGMENT_MARKER="<NS>"
PIPELINE_MIN_WORDS="4"
PIPELINE_MAX_SENTENCES=""
PIPELINE_GRAMMAR_NAME="tenth-grammar"
PIPELINE_SUBJECT="all"
PIPELINE_CANDIDATE_COUNT="100000"
PIPELINE_MAX_TRANSLATIONS="1"
PIPELINE_SEED=""
PIPELINE_GRAMMAR_VERSION="v10"

if [[ "$MODE" == "synthetic" ]]; then
  prompt_with_default "Synthetic grammar name" "$PIPELINE_GRAMMAR_NAME" PIPELINE_GRAMMAR_NAME
  prompt_with_default "Synthetic subject profile" "$PIPELINE_SUBJECT" PIPELINE_SUBJECT
  prompt_with_default "Candidate count" "$PIPELINE_CANDIDATE_COUNT" PIPELINE_CANDIDATE_COUNT
  prompt_with_default "Max translations per tree" "$PIPELINE_MAX_TRANSLATIONS" PIPELINE_MAX_TRANSLATIONS
  read -r -p "Seed (blank for random): " PIPELINE_SEED || true
else
  prompt_with_default "Corpus input path" "$PROJECT_ROOT/data/cereal_formatted.txt" PIPELINE_INPUT
  prompt_with_default "Corpus grammar version" "$PIPELINE_GRAMMAR_VERSION" PIPELINE_GRAMMAR_VERSION
  read -r -p "Format raw input first with format-corpus? [y/N]: " FORMAT_REPLY || true
  if [[ "${FORMAT_REPLY:-N}" =~ ^[Yy]$ ]]; then
    PIPELINE_FORMAT_INPUT="1"
    INPUT_BASENAME="$(basename "$PIPELINE_INPUT")"
    INPUT_STEM="${INPUT_BASENAME%.*}"
    prompt_with_default \
      "Formatted corpus output path" \
      "$PROJECT_ROOT/data/${INPUT_STEM}_formatted.txt" \
      PIPELINE_FORMATTED_INPUT
    prompt_with_default "Formatter segment marker" "$PIPELINE_SEGMENT_MARKER" PIPELINE_SEGMENT_MARKER
    prompt_with_default "Formatter minimum words" "$PIPELINE_MIN_WORDS" PIPELINE_MIN_WORDS
  fi
  read -r -p "Max sentences (blank for full corpus): " PIPELINE_MAX_SENTENCES || true
fi

mkdir -p "$PROJECT_ROOT/logs/slurm"

CONFIG_DIR="$PROJECT_ROOT/logs/slurm/job-configs"
mkdir -p "$CONFIG_DIR"
CONFIG_FILE="$CONFIG_DIR/pipeline-${RUN_NAME}-${STAMP}.env"

{
  printf 'PIPELINE_MODE=%q\n' "$MODE"
  printf 'PIPELINE_RUN_NAME=%q\n' "$RUN_NAME"
  printf 'PIPELINE_OUTPUT_DIR=%q\n' "$OUTPUT_DIR"
  printf 'PIPELINE_INPUT=%q\n' "$PIPELINE_INPUT"
  printf 'PIPELINE_FORMAT_INPUT=%q\n' "$PIPELINE_FORMAT_INPUT"
  printf 'PIPELINE_FORMATTED_INPUT=%q\n' "$PIPELINE_FORMATTED_INPUT"
  printf 'PIPELINE_SEGMENT_MARKER=%q\n' "$PIPELINE_SEGMENT_MARKER"
  printf 'PIPELINE_MIN_WORDS=%q\n' "$PIPELINE_MIN_WORDS"
  printf 'PIPELINE_MAX_SENTENCES=%q\n' "$PIPELINE_MAX_SENTENCES"
  printf 'PIPELINE_GRAMMAR_NAME=%q\n' "$PIPELINE_GRAMMAR_NAME"
  printf 'PIPELINE_SUBJECT=%q\n' "$PIPELINE_SUBJECT"
  printf 'PIPELINE_CANDIDATE_COUNT=%q\n' "$PIPELINE_CANDIDATE_COUNT"
  printf 'PIPELINE_MAX_TRANSLATIONS=%q\n' "$PIPELINE_MAX_TRANSLATIONS"
  printf 'PIPELINE_SEED=%q\n' "$PIPELINE_SEED"
  printf 'PIPELINE_GRAMMAR_VERSION=%q\n' "$PIPELINE_GRAMMAR_VERSION"
} > "$CONFIG_FILE"

echo "========================================"
echo "Submitting SyntaxGrammar Pipeline Job"
echo "========================================"
echo "Mode: $MODE"
echo "Run name: $RUN_NAME"
echo "Output dir: $OUTPUT_DIR"
echo "CPUs / workers: $CPUS"
echo "Partition: $PARTITION"
echo "QOS: $QOS"
echo "Account: $ACCOUNT"
echo "Memory: $MEMORY"
echo "Walltime: $WALLTIME"
if [[ "$MODE" == "synthetic" ]]; then
  echo "Grammar name: $PIPELINE_GRAMMAR_NAME"
  echo "Subject: $PIPELINE_SUBJECT"
  echo "Candidate count: $PIPELINE_CANDIDATE_COUNT"
else
  echo "Input: $PIPELINE_INPUT"
  echo "Grammar version: $PIPELINE_GRAMMAR_VERSION"
  echo "Format first: $PIPELINE_FORMAT_INPUT"
  if [[ "$PIPELINE_FORMAT_INPUT" == "1" ]]; then
    echo "Formatted output: $PIPELINE_FORMATTED_INPUT"
  fi
fi
echo "Config file: $CONFIG_FILE"
echo "========================================"

JOB_ID=$(sbatch --parsable \
  --account="$ACCOUNT" \
  --partition="$PARTITION" \
  --qos="$QOS" \
  --time="$WALLTIME" \
  --cpus-per-task="$CPUS" \
  --mem="$MEMORY" \
  --job-name="syntaxgrammar-$MODE" \
  --output="$PROJECT_ROOT/logs/slurm/pipeline-%j.out" \
  --error="$PROJECT_ROOT/logs/slurm/pipeline-%j.err" \
  "$PROJECT_ROOT/slurm/run_pipeline.sbatch" \
  "$CONFIG_FILE")

echo "Submitted job: $JOB_ID"
echo "Monitor with: squeue -j $JOB_ID"
echo "Logs: $PROJECT_ROOT/logs/slurm/pipeline-$JOB_ID.out"