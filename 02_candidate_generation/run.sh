#!/usr/bin/env bash
set -euo pipefail

# Jean Zay command log. Keep the paths, arguments, and order used for each run.
stage_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

# 1. In your Jean Zay login shell, source the shared environment.
# source "$stage_dir/../scripts/setup_environment.sh"

# 2. Stage 01 command that produces the prepared inputs for this run.
# Run separately if the prepared split files need to be created.
# python3 "$stage_dir/../01_data_preparation/parallel_tsv.py" \
#     --train "$SCRATCH_DIR/datasets/raw/train.enfr.gz" \
#     --test "$SCRATCH_DIR/datasets/raw/test.enfr.gz" \
#     --source-language en \
#     --target-language fr \
#     --output-dir "$SCRATCH_DIR/datasets/prepared/enfr"

# 3. Submit the reference-assisted pilot to Jean Zay.
: "${SCRATCH_DIR:?Source scripts/setup_environment.sh first}"
: "${TRANSLATEGEMMA_MODEL_PATH:?Set the shared local TranslateGemma model path}"

if [[ ! -f "$TRANSLATEGEMMA_MODEL_PATH/config.json" ]]; then
    printf 'Expected a local TranslateGemma directory with config.json: %s\n' \
        "$TRANSLATEGEMMA_MODEL_PATH" >&2
    exit 1
fi

sbatch generate_candidates.slurm "$stage_dir"
