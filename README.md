# preference-optimization

Parameter-efficient fine-tuning of machine translation models using preference optimization. The initial experiment will use DPO to train a single shared LoRA adapter on `google/translategemma-12b-it` for idiomatic and literal translation.

## Pipeline stages

| Stage | Entry point documentation |
| --- | --- |
| 01 | [Data preparation](01_data_preparation/README.md) |
| 02 | [Candidate generation](02_candidate_generation/README.md) |
| 03 | [Candidate validation](03_candidate_validation/README.md) |
| 04 | [Preference dataset](04_preference_dataset/README.md) |
| 05 | [Fine-tuning](05_fine_tuning/README.md) |
| 06 | [Evaluation](06_evaluation/README.md) |
| 07 | [Analysis](07_analysis/README.md) |

Stage 01 converts existing train and test TSVs into JSONL. Stages 02–07 are Phase 1 stubs. Each stage keeps its Python entry point, SLURM template, and Jean Zay `run.sh` command log together. Stages that need dependencies reuse the same project virtual environment. Each stage keeps its own configuration templates. The `configs/` directory holds settings shared across stages, including storage, the base model, style, and the dataset contract. The `scripts/` directory contains the Jean Zay environment and scratch-storage utilities.

From the repository root, run the CPU checks or display the resolved scratch root with the Python standard library.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_environment.py
```

See the [roadmap](docs/implementation_plan.md), [architecture](docs/architecture.md), and [Jean Zay setup notes](docs/jeanzay.md) for open decisions and operational scope.
