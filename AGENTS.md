# Codex repository instructions

## Mission

This repository, `preference-optimization`, is a research framework for preference-based, parameter-efficient fine-tuning of machine translation models. The initial experiment controls translation **style** (`idiomatic` versus `literal`), while the architecture should allow later preference features such as register and terminology. The initial base model is **`google/translategemma-12b-it`**. Use one shared LoRA adapter for both style modes.

## Current scope: scaffold first

**Only create the project structure and lightweight foundations unless explicitly asked to implement a pipeline stage.** The user will fill in unspecified details incrementally. Do not treat open decisions as blockers to scaffolding; use documented placeholders and TODOs. Do not implement the full pipeline, launch jobs, install packages, download models, or process real data as part of the initial scaffold.

Read `docs/implementation_plan.md` for the full roadmap. Work in small, reviewable phases. Before substantial changes, summarize the intended files and changes; after changes, report what is implemented, what is only a stub, and what remains undecided.

## Architecture

Keep distinct, numbered stage directories with their own README and thin entry point:

1. `01_data_preparation/`
2. `02_candidate_generation/`
3. `03_candidate_validation/`
4. `04_preference_dataset/`
5. `05_fine_tuning/`
6. `06_evaluation/`
7. `07_analysis/`

Put reusable implementation in `src/preference_optimization/`; do not duplicate logic in stage entry points. Use `configs/` for YAML configuration, `slurm/` for Jean Zay batch templates, `scripts/` for environment utilities, `tests/` for CPU-only tests, and `docs/` for design notes. Keep feature-specific behavior isolated so that future preference dimensions can be added without changing the shared training core. Implement **style only** when implementation begins.

## Jean Zay and storage

GPU work will run on **Jean Zay**, with **one H100 per GPU job**, using SLURM. Do not assume partition, account, modules, time limits, or GPU directives; leave site-specific settings configurable and clearly marked.

Use this storage root for generated data, environments, caches, and artifacts:

```bash
SCRATCH_DIR=/lustre/fsn1/projects/rech/eut/ujt99zo/josep/preference-optimization
```

- Virtual environments: `$SCRATCH_DIR/venvs/`
- Datasets: `$SCRATCH_DIR/datasets/`
- Training artifacts: `$SCRATCH_DIR/experiments/`
- Logs: `$SCRATCH_DIR/logs/`
- Caches and temporary files: `$SCRATCH_DIR/caches/`, `$SCRATCH_DIR/tmp/`
- Downloaded model copies **only when necessary**: `$SCRATCH_DIR/models/`

**Models are often already present on Jean Zay shared disks. Prefer existing shared model paths and never duplicate them by default.** Model paths must be configurable (for example, via `TRANSLATEGEMMA_MODEL_PATH`). Do not download a model automatically, including when a configured path is missing. Do not assume the actual shared model path until confirmed. Support offline/local-only loading once implemented.

```bash
TRAINSLATEGEMMA_MODEL_PATH=/lustre/fsmisc/dataset/HuggingFace_Models/google/translategemma-12b-it
```

Keep Git-tracked source code, docs, and configuration templates outside scratch when a persistent project location is available. Never commit datasets, model weights, environments, checkpoints, caches, or secrets.

## Technology and research rules

- Prefer Python, PyTorch, Transformers, PEFT, TRL, Accelerate, Hugging Face Datasets, YAML, and pytest. Pin compatible versions when the environment is actually established; do not invent verified compatibility.
- The initial algorithm is **DPO**, using a **single** LoRA adapter. Do not create separate adapters for idiomatic and literal outputs.
- Candidate generation, candidate validation, preference-record construction, training, and evaluation must remain separate stages.
- Both style candidates must be semantically adequate, grammatical, and terminology-compliant. The idiomatic candidate should be more natural; the literal candidate should be closer to source structure without unnatural calques. Allow ties and reject ambiguous pairs.
- For each validated source pair, construct **two** reversed, style-conditioned DPO records. Split by source before expanding records to avoid leakage.
- Inspect TranslateGemma's real tokenizer/chat template before implementing style-conditioned prompting. Do not assume inserting `style:` into source text will work.
- Preserve provenance, seeds, configs, model revisions, and evaluation outputs. Avoid silent overwrites.
- Tests should run on CPU without model downloads. Do not run GPU workloads unless specifically requested.

## Missing information

Do not guess: Jean Zay account/partition/module settings, shared model paths, teacher model, language pairs, corpus paths, evaluation judge, or final training hyperparameters. Represent these as configurable TODOs. Ask only when a specific implementation step genuinely needs a value.

## Initial acceptance criteria

A useful first contribution consists of the directory tree, stage READMEs, lightweight Python package skeleton, example configuration files with placeholders, `.gitignore`, environment/SLURM templates that are explicitly non-operational until configured, and basic CPU-only structure/config tests. Clearly label any stub; no false claims that training or model loading works.
