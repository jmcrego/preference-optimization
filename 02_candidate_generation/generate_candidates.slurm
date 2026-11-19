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

# vLLM appends a UUID to this path. Keep its Unix sockets on the compute node.
rpc_dir="$(mktemp -d /tmp/po-vllm.XXXXXXXX)"
trap 'rm -rf -- "$rpc_dir"' EXIT
export VLLM_RPC_BASE_PATH="$rpc_dir"

# Isolate the inference process from user-site packages and inherited Python paths.
srun --ntasks=1 python3 -I "$stage_dir/generate_candidates.py" \
    --dataset "$SCRATCH_DIR/datasets/prepared/enfr/train.jsonl" \
    --source-language en \
    --target-language fr \
    --prompt "$stage_dir/prompts/reference_guided_independent_styles.txt" \
    --output-dir "$SCRATCH_DIR/datasets/generated/enfr/diagnostics/reference_guided_independent_styles" \
    --model-path "$TRANSLATEGEMMA_MODEL_PATH" \
    --limit 3 \
    --batch-size 32 \
    --max-tokens 512 \
    --seed 0
