#!/usr/bin/env bash
set -euo pipefail

# Jean Zay command log. Keep the paths, arguments, and order used for each run.
stage_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(dirname -- "$stage_dir")"

# 1. In your Jean Zay login shell, source the shared environment.
# source "$repo_dir/scripts/setup_environment.sh"

# 2. Stage 02 independent-styles experiment. Submit separately from the login shell.
# (cd -- "$repo_dir/02_candidate_generation" && bash run.sh independent-styles)
# Candidates: $SCRATCH_DIR/datasets/generated/enfr/reference_guided_independent_styles/reference_guided_independent_styles.jsonl

# 3. Candidate validation. Record the exact Stage 02 output path and judge
# settings here once validation is implemented.
# For a batch run, record the verified SLURM command for validate_candidates.slurm.

python3 "$stage_dir/validate_candidates.py"
