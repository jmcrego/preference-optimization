#!/usr/bin/env bash
#SBATCH --job-name=PO.validation
#SBATCH --output=./logs/%u.%x.%j.out
#SBATCH --error=./logs/%u.%x.%j.log
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=10
#SBATCH --time=20:00:00
#SBATCH -C h100
#SBATCH -A eut@h100

set -euo pipefail

stage_dir="${1:?Pass the absolute Stage 03 directory via run.sh}"
case "${2:-}" in
    quality) script=score_quality.py ;;
    mqm) script=validate_candidates.py ;;
    *) printf 'Expected quality or mqm as the validation pass.\n' >&2; exit 2 ;;
esac
shift 2

module purge
module load arch/h100
module load pytorch-gpu/py3/2.6.0
source "$stage_dir/../scripts/setup_environment.sh"
unset PYTHONPATH
export PYTHONNOUSERSITE=1

if [[ "$script" == validate_candidates.py ]]; then
    rpc_dir="$(mktemp -d /tmp/po-vllm.XXXXXXXX)"
    trap 'rm -rf -- "$rpc_dir"' EXIT
    export VLLM_RPC_BASE_PATH="$rpc_dir"
fi

srun --ntasks=1 python3 "$stage_dir/$script" "$@"
