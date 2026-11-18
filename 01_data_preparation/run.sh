#!/usr/bin/env bash
set -euo pipefail

# Jean Zay command log. Keep the paths and commands used for each run.
stage_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

# 1. In your Jean Zay login shell, source scripts/setup_environment.sh from the checkout.

# 2. Convert the supplied splits. Edit the paths and codes here for each run.
: "${SCRATCH_DIR:?Source scripts/setup_environment.sh before running Stage 01}"

python3 "$stage_dir/parallel_tsv.py" \
    --train "$SCRATCH_DIR/datasets/raw/train.enfr.gz" \
    --test "$SCRATCH_DIR/datasets/raw/test.enfr.gz" \
    --source-language en \
    --target-language fr \
    --output-dir "$SCRATCH_DIR/datasets/prepared/enfr"
