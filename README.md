# preference-optimization

Parameter-efficient fine-tuning of machine translation models using preference optimization. The initial experiment will use DPO to train a single shared LoRA adapter on `google/translategemma-12b-it` for idiomatic and literal translation.

## Phase 1 scaffold

| Stage | Entry point documentation |
| --- | --- |
| 01 | [Data preparation](01_data_preparation/README.md) |
| 02 | [Candidate generation](02_candidate_generation/README.md) |
| 03 | [Candidate validation](03_candidate_validation/README.md) |
| 04 | [Preference dataset](04_preference_dataset/README.md) |
| 05 | [Fine-tuning](05_fine_tuning/README.md) |
| 06 | [Evaluation](06_evaluation/README.md) |
| 07 | [Analysis](07_analysis/README.md) |

Each stage entry point exits with a Phase 1 stub message. The YAML files under `configs/` document planned settings. The package under `src/preference_optimization/` contains the scratch-path helper and namespaces for later phases.

From the repository root, run the CPU checks or display the resolved scratch root with the Python standard library.

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 scripts/check_environment.py
```

See the [roadmap](docs/implementation_plan.md), [architecture](docs/architecture.md), and [Jean Zay setup notes](docs/jeanzay.md) for open decisions and operational scope.
