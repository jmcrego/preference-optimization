#!/usr/bin/env bash
set -euo pipefail

# Jean Zay command log. Record the exact commands and settings in execution order.
stage_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

# 1. In your Jean Zay login shell, source scripts/setup_environment.sh from the checkout.

# 2. Record the final arguments and the manual invocation here.
# python "$stage_dir/run.py"
# For a batch run, record the verified SLURM command for train_dpo.sbatch here.

printf '%s\n' 'This stage is a stub. The command log is a template.' >&2
exit 1
