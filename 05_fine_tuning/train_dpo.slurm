#!/usr/bin/env bash
#SBATCH --job-name=PO.train
#SBATCH --output=./logs/%u.%x.%j.out
#SBATCH --error=./logs/%u.%x.%j.log
# Jean Zay H100 settings supplied for this project.
# Enable the directives and module commands when the stage has a workload.
# #SBATCH --gres=gpu:1
# #SBATCH --nodes=1
# #SBATCH --cpus-per-task=10
# #SBATCH --time=20:00:00
# #SBATCH -C h100
# #SBATCH -A eut@h100

set -euo pipefail

# module purge
# module load arch/h100
# module load pytorch-gpu/py3/2.6.0
# Source scripts/setup_environment.sh from the repository checkout after
# loading the modules to activate the shared project environment.

printf '%s\n' 'Phase 1 SLURM stub. No workload is configured.' >&2
exit 1
