#!/usr/bin/env bash
#SBATCH --job-name=PO.analysis
#SBATCH --output=./logs/%u.%x.%j.out
#SBATCH --error=./logs/%u.%x.%j.log
# TODO: Confirm account, partition, time limit, CPU/memory requirements,
# module commands, and the virtual environment under SCRATCH_DIR.
# CPU stage.
printf '%s\n' 'Phase 1 SLURM stub. No workload is configured.' >&2
exit 1
