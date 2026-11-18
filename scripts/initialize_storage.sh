#!/usr/bin/env bash
set -eu

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../slurm/setup_environment.sh"
mkdir -p -- "$SCRATCH_DIR/venvs" "$SCRATCH_DIR/logs" \
    "$SCRATCH_DIR"/datasets/{raw,prepared,generated,validated,splits} \
    "$SCRATCH_DIR"/experiments/{checkpoints,adapters,evaluations} \
    "$HF_HUB_CACHE" "$HF_DATASETS_CACHE" "$TORCH_HOME" "$TRITON_CACHE_DIR" "$TMPDIR"
printf 'Initialized project storage under %s\n' "$SCRATCH_DIR"
