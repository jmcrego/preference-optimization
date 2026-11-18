#!/usr/bin/env bash
#SBATCH --job-name=PO.candidates
#SBATCH --output=./logs/%u.%x.%j.out
#SBATCH --error=./logs/%u.%x.%j.log
# Jean Zay H100 settings supplied for this project.
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=10
#SBATCH --time=20:00:00
#SBATCH -C h100
#SBATCH -A eut@h100

set -euo pipefail

# The submitter passes the stage directory because SLURM copies this script.
stage_dir="${1:?Pass the absolute Stage 02 directory via run.sh}"

module purge
module load arch/h100
module load pytorch-gpu/py3/2.6.0
source "$stage_dir/../scripts/setup_environment.sh"
: "${TRANSLATEGEMMA_MODEL_PATH:?Set the shared local TranslateGemma model path}"

srun --ntasks=1 python3 "$stage_dir/generate_candidates.py" \
    --dataset "$SCRATCH_DIR/datasets/prepared/enfr/train.jsonl" \
    --source-language en \
    --target-language fr \
    --prompt "$stage_dir/prompts/reference_assisted_literal_then_idiomatic.txt" \
    --output-dir "$SCRATCH_DIR/datasets/generated/enfr/reference_assisted_literal_then_idiomatic" \
    --model-path "$TRANSLATEGEMMA_MODEL_PATH" \
    --limit 50 \
    --batch-size 32 \
    --max-tokens 512 \
    --seed 0
