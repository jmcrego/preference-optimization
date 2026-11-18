#!/usr/bin/env bash
# Source from Bash to apply the storage and offline environment settings.
# TODO: Confirm Jean Zay module commands and the virtual environment path.
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    printf '%s\n' 'Source scripts/setup_environment.sh from Bash.' >&2
    exit 1
fi

if [[ "${SCRATCH_DIR:-/}" != /* ]]; then
    printf '%s\n' 'SCRATCH_DIR must be an absolute path.' >&2
    return 1
fi

export SCRATCH_DIR="${SCRATCH_DIR:-/lustre/fsn1/projects/rech/eut/ujt99zo/josep/preference-optimization}"
export HF_HOME="$SCRATCH_DIR/caches/huggingface"
export HF_HUB_CACHE="$HF_HOME/hub"
export HF_DATASETS_CACHE="$SCRATCH_DIR/caches/datasets"
export XDG_CACHE_HOME="$SCRATCH_DIR/caches"
export TORCH_HOME="$SCRATCH_DIR/caches/torch"
export TRITON_CACHE_DIR="$SCRATCH_DIR/caches/triton"
export TMPDIR="$SCRATCH_DIR/tmp"
export HF_HUB_OFFLINE=1
export HF_DATASETS_OFFLINE=1
# TODO: Create a unique temporary directory per job when job execution is implemented.

mkdir -p -- "$SCRATCH_DIR/venvs" \
    "$SCRATCH_DIR"/datasets/{raw,prepared,generated,validated,splits} \
    "$SCRATCH_DIR"/experiments/{checkpoints,adapters,evaluations} \
    "$HF_HUB_CACHE" "$HF_DATASETS_CACHE" "$TORCH_HOME" "$TRITON_CACHE_DIR" "$TMPDIR" || return 1

export PROJECT_VENV="${PROJECT_VENV:-$SCRATCH_DIR/venvs/preference-optimization}"
if [[ -f "$PROJECT_VENV/bin/activate" ]]; then
    source "$PROJECT_VENV/bin/activate" || return 1
    printf 'Activated project virtual environment at %s\n' "$PROJECT_VENV"
else
    printf 'Project virtual environment not found at %s. Continuing with the current Python.\n' \
        "$PROJECT_VENV" >&2
fi
printf 'Project scratch is ready at %s\n' "$SCRATCH_DIR"
