#!/bin/bash
#==============================================================================
# SLURM Job Script: Spanish->Guarani Pipeline
#
# Reads a sourced config file written by slurm/submit_pipeline.sh and runs
# either the synthetic pipeline or the Ancora-style corpus pipeline. The job
# uses the same CPU allocation for Slurm and wrapper-level --workers.
#==============================================================================

#SBATCH --job-name=syntaxgrammar
#SBATCH --output=logs/slurm/pipeline-%j.out
#SBATCH --error=logs/slurm/pipeline-%j.err

# --- Resource Allocation ---
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=36:00:00

# --- Queue/Partition (set in submit_pipeline.sh) ---
##SBATCH --partition=nlprx-lab
##SBATCH --qos=short

set -euo pipefail

CONFIG_FILE="${1:?ERROR: expected config file path}"
source "$CONFIG_FILE"

echo "========================================"
echo "SyntaxGrammar Pipeline Job"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURMD_NODENAME"
echo "Start Time: $(date)"
echo "Config file: $CONFIG_FILE"
echo "Mode: $PIPELINE_MODE"
echo "Run name: $PIPELINE_RUN_NAME"
echo "Output dir: $PIPELINE_OUTPUT_DIR"
echo "Workers: ${SLURM_CPUS_PER_TASK:-1}"
echo "========================================"

cd "$SLURM_SUBMIT_DIR" || exit 1
mkdir -p logs/slurm

if [ -d "venv" ]; then
    source venv/bin/activate
    PYTHON_CMD=(python)
elif [ -d ".venv" ]; then
    source .venv/bin/activate
    PYTHON_CMD=(python)
elif command -v uv &> /dev/null; then
    uv sync
    PYTHON_CMD=(uv run python)
else
    echo "ERROR: No Python environment found. Create venv/ or .venv/, or install uv."
    exit 1
fi

WORKERS="${SLURM_CPUS_PER_TASK:-1}"

if [[ "$PIPELINE_MODE" == "synthetic" ]]; then
    CMD=(
      "${PYTHON_CMD[@]}"
      scripts/run_pipeline.py
      synthetic
      --grammar-name "$PIPELINE_GRAMMAR_NAME"
      --subject "$PIPELINE_SUBJECT"
      --candidate-count "$PIPELINE_CANDIDATE_COUNT"
      --max-translations "$PIPELINE_MAX_TRANSLATIONS"
      --workers "$WORKERS"
      --run-name "$PIPELINE_RUN_NAME"
      --output-dir "$PIPELINE_OUTPUT_DIR"
      --overwrite
    )
    if [[ -n "$PIPELINE_SEED" ]]; then
      CMD+=(--seed "$PIPELINE_SEED")
    fi
    "${CMD[@]}"
elif [[ "$PIPELINE_MODE" == "corpus" ]]; then
    INPUT_PATH="$PIPELINE_INPUT"
    if [[ "$PIPELINE_FORMAT_INPUT" == "1" ]]; then
      FORMAT_CMD=(
        "${PYTHON_CMD[@]}"
        scripts/run_pipeline.py
        format-corpus
        --input "$PIPELINE_INPUT"
        --output "$PIPELINE_FORMATTED_INPUT"
        --segment-marker "$PIPELINE_SEGMENT_MARKER"
        --min-words "$PIPELINE_MIN_WORDS"
      )
      "${FORMAT_CMD[@]}"
      INPUT_PATH="$PIPELINE_FORMATTED_INPUT"
    fi

    CMD=(
      "${PYTHON_CMD[@]}"
      scripts/run_pipeline.py
      corpus
      --input "$INPUT_PATH"
      --grammar-version "$PIPELINE_GRAMMAR_VERSION"
      --workers "$WORKERS"
      --run-name "$PIPELINE_RUN_NAME"
      --output-dir "$PIPELINE_OUTPUT_DIR"
      --overwrite
    )
    if [[ -n "$PIPELINE_MAX_SENTENCES" ]]; then
      CMD+=(--max-sentences "$PIPELINE_MAX_SENTENCES")
    fi
    "${CMD[@]}"
else
    echo "ERROR: Unsupported PIPELINE_MODE '$PIPELINE_MODE'"
    exit 1
fi

echo "========================================"
echo "Pipeline complete!"
echo "End Time: $(date)"
echo "========================================"