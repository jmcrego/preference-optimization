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

experiment="${2:-independent-styles}"
experiment_args=(--dtype bfloat16 --no-diagnostics)

if [[ "$experiment" == joint-styles ]]; then
    prompt="$stage_dir/prompts/reference_assisted_literal_then_idiomatic.txt"
    output_dir="$SCRATCH_DIR/datasets/generated/enfr/reference_assisted_literal_then_idiomatic"
    experiment_args+=(--joint-completion)
elif [[ "$experiment" == independent-styles ]]; then
    prompt="$stage_dir/prompts/reference_guided_independent_styles.txt"
    output_dir="$SCRATCH_DIR/datasets/generated/enfr/reference_guided_independent_styles"
elif [[ "$experiment" == draft-rewrite ]]; then
    prompt="$stage_dir/prompts/human_draft_style_rewrite.txt"
    output_dir="$SCRATCH_DIR/datasets/generated/enfr/human_draft_style_rewrite"
else
    printf 'Unknown experiment: %s. Choose joint-styles, independent-styles, or draft-rewrite.\n' "$experiment" >&2
    exit 2
fi

# Isolate the inference process from user-site packages and inherited Python paths.
srun --ntasks=1 python3 -I "$stage_dir/generate_candidates.py" \
    --dataset "$SCRATCH_DIR/datasets/prepared/enfr/train.jsonl" \
    --source-language en \
    --target-language fr \
    --prompt "$prompt" \
    --output-dir "$output_dir" \
    --model-path "$TRANSLATEGEMMA_MODEL_PATH" \
    "${experiment_args[@]}" \
    --batch-size 32 \
    --max-tokens 512 \
    --seed 0
