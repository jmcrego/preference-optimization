#!/usr/bin/env bash
set -euo pipefail

# Jean Zay command log. Keep the paths, arguments, and order used for each run.
stage_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(dirname -- "$stage_dir")"

# 1. In your Jean Zay login shell, source the shared environment.
# source "$repo_dir/scripts/setup_environment.sh"

# 2. Stage 04 preference dataset command. Run separately once implemented.
# python3 "$repo_dir/04_preference_dataset/run.py"

# 3. Record the exact Stage 04 preference dataset path and the training run directory.
# Training config: 05_fine_tuning/style_dpo.yaml
# For a batch run, record the verified SLURM command for train_dpo.slurm.

python3 "$stage_dir/train_dpo.py"
