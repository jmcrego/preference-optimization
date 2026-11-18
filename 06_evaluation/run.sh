#!/usr/bin/env bash
set -euo pipefail

# Jean Zay command log. Keep the paths, arguments, and order used for each run.
stage_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(dirname -- "$stage_dir")"

# 1. In your Jean Zay login shell, source the shared environment.
# source "$repo_dir/scripts/setup_environment.sh"

# 2. Stage 05 fine-tuning command. Run separately once implemented.
# python3 "$repo_dir/05_fine_tuning/train_dpo.py"

# 3. Record the exact adapter path and evaluation output directory.
# Prepared test input: $SCRATCH_DIR/datasets/prepared/enfr/test.jsonl
# Evaluation config: 06_evaluation/style_evaluation.yaml
# For a batch run, record the verified SLURM command for evaluate.slurm.

python3 "$stage_dir/evaluate.py"
