#!/usr/bin/env bash
set -euo pipefail

# Jean Zay command log. Keep the paths, arguments, and order used for each run.
stage_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(dirname -- "$stage_dir")"

# 1. In your Jean Zay login shell, source the shared environment.
# source "$repo_dir/scripts/setup_environment.sh"

# 2. Stage 06 evaluation command. Run separately once implemented.
# python3 "$repo_dir/06_evaluation/evaluate.py"

# 3. Record the exact Stage 06 results path and analysis output directory.
# For a batch run, record the verified SLURM command for analyze.slurm.

python3 "$stage_dir/analyze.py"
