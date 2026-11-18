#!/usr/bin/env bash
set -eu

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../slurm/setup_environment.sh"
mkdir -p -- "$SCRATCH_DIR/venvs" "$SCRATCH_DIR/datasets" \
    "$SCRATCH_DIR/experiments" "$SCRATCH_DIR/logs" \
    "$HF_HUB_CACHE" "$HF_DATASETS_CACHE" "$TORCH_HOME" "$TRITON_CACHE_DIR" "$TMPDIR"
