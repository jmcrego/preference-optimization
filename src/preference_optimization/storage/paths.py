"""Resolve scratch paths without touching the filesystem."""

import os
from pathlib import Path

DEFAULT_SCRATCH_DIR = Path(
    "/lustre/fsn1/projects/rech/eut/ujt99zo/josep/preference-optimization"
)


def scratch_dir() -> Path:
    """Use SCRATCH_DIR when set, falling back to the Jean Zay project root."""
    value = os.environ.get("SCRATCH_DIR")
    path = Path(value) if value else DEFAULT_SCRATCH_DIR
    if not path.is_absolute():
        raise ValueError("SCRATCH_DIR must be an absolute path.")
    return path
