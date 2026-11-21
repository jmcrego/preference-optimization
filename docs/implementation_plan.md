# Implementation plan — preference-optimization

> **Status: roadmap, not an instruction to implement everything now.** The first Codex task is to create the repository structure and minimal foundations. Details will be decided progressively as each stage is implemented.

## 1. Purpose and boundaries

Build a reproducible research framework for preference-based fine-tuning of machine translation models on Jean Zay. The initial backbone is `google/translategemma-12b-it`; the initial trainable method is a single LoRA adapter optimized with DPO. The initial preference feature is `style`, with `idiomatic` and `literal`. Future features may include `register`, `terminology`, and others, but **do not implement them yet**.

### Style semantics

- **Idiomatic:** Produce polished text that reads as if originally written in the target language. Reformulate vocabulary, syntax, and information structure when beneficial, while preserving meaning and technical precision.
- **Literal:** Stay as close as possible to source vocabulary, grammar, and information order, subject to correct and natural target-language grammar. Never introduce unnatural calques or sacrifice accuracy.
- **Both:** Preserve factual details, semantic adequacy, register constraints, and required domain terminology. Some sources legitimately have little or no style contrast; do not force a pair.

## 2. Execution and storage

All GPU-intensive jobs run on **Jean Zay** through SLURM, using **one H100** per GPU job. No local GPU execution is expected. CPU-only validation and unit tests should work without downloading model weights.

```bash
SCRATCH_DIR=/lustre/fsn1/projects/rech/eut/ujt99zo/josep/preference-optimization
```

Suggested artifact layout (created on demand, not committed):

```text
$SCRATCH_DIR/
├── venvs/
├── datasets/{raw,prepared,generated,validated,splits}/
├── experiments/{checkpoints,adapters,evaluations}/
├── caches/{huggingface,datasets,torch,triton}/
├── tmp/
└── models/                  # only for necessary staged/downloaded models
```

**Shared models first:** Many models are already installed on Jean Zay disks. Resolve their existing paths before any download. Configure `TRANSLATEGEMMA_MODEL_PATH` (and later teacher/judge paths); do not invent paths or copy weights into scratch without a reason. Missing paths must produce actionable errors, not implicit downloads. Keep the repository itself in persistent storage where possible; scratch may be subject to cleanup.

When environment setup is implemented, centralize cache exports such as `HF_HOME`, `HF_HUB_CACHE`, `HF_DATASETS_CACHE`, `XDG_CACHE_HOME`, `TORCH_HOME`, `TRITON_CACHE_DIR`, and `TMPDIR`, all under scratch. Job-specific temp directories should avoid collisions. SLURM account, partition, module commands, and GPU directives are site-specific TODOs, not assumed defaults.

## 3. Target repository structure

```text
preference-optimization/
├── AGENTS.md
├── README.md
├── .gitignore
├── .env.example
├── configs/
│   ├── base.yaml
│   ├── models/translategemma_12b.yaml
│   ├── features/style.yaml
│   └── datasets/style_dataset.yaml
├── 01_data_preparation/{README.md,run.sh,prepare_data.slurm,inspect_dataset.py,parallel_tsv.py}
├── 02_candidate_generation/{README.md,generate_candidates.py,run.sh,generate_candidates.slurm,teacher.example.yaml,prompts/}
├── 03_candidate_validation/{README.md,validate_candidates.py,run.sh,validate_candidates.slurm,score_quality.py,validation_io.py,mqm_judge.txt}
├── 04_preference_dataset/{README.md,run.py,run.sh,build_preferences.slurm}
├── 05_fine_tuning/{README.md,train_dpo.py,run.sh,train_dpo.slurm,style_dpo.yaml}
├── 06_evaluation/{README.md,evaluate.py,run.sh,evaluate.slurm,style_evaluation.yaml}
├── 07_analysis/{README.md,analyze.py,run.sh,analyze.slurm}
├── scripts/
│   ├── setup_environment.sh
│   ├── check_environment.py
│   └── scratch_paths.py
├── tests/
└── docs/
    ├── implementation_plan.md
    ├── architecture.md
    ├── jeanzay.md
    ├── data_formats.md
    ├── experiments.md
    └── adding_features.md
```

Numbered stage directories own their READMEs, entry points, and stage-specific settings. Shared configuration belongs under `configs/`. Each stage should eventually accept configuration, validate inputs, record provenance, and write versioned outputs without silent overwrites.

## 4. Pipeline roadmap

### 01 — Data preparation

Ingest **existing parallel corpora** (initially JSONL and TSV; optionally Hugging Face Datasets). Preserve original sources and references, corpus provenance, language pair, domain, and stable source IDs. Validate records, remove duplicates, and split reproducibly by source **before** constructing preferences. A human reference is not automatically labeled idiomatic or literal.

Example input record:

```json
{"id":"example-000001","source_language":"en","target_language":"fr","source":"The company made a decision to discontinue the service.","reference":"L'entreprise a décidé de mettre fin au service.","domain":"general"}
```

### 02 — Candidate generation

Implement configurable generation strategies, initially:

1. Base TranslateGemma output plus opposite-style teacher rewrite.
2. Two independently teacher-generated style candidates.
3. Controlled rewrite of a high-quality existing translation.

The **teacher model is configurable**, not hardcoded. Prefer a local Hugging Face-compatible backend first; optional API backends may be added later. Record generator model, revision, strategy, prompt, decoding parameters, and parent-candidate links. Do not assume generation prompts correctly label the actual style.

### 03 — Candidate validation

Keep validation independent of generation. Gate each candidate on semantic adequacy, grammaticality, and required terminology. Judge style **comparatively**: which candidate is more idiomatic, and which is more source-close? Permit ties; accept a pair only when the winners oppose one another and both translations are good. Blind judge to origin; randomize A/B ordering; store raw and parsed judgments and reasons. A configurable LLM judge is the initial approach; automated MT quality metrics are supplementary, not style classifiers. Provide human review export and calibration against human annotations.

### 04 — Preference dataset construction

For each accepted `(x, y_I, y_L)` create **two** DPO records, sharing the same source and candidate IDs:

```json
{"source_id":"example-000001","feature":"style","feature_value":"idiomatic","prompt":"<style-conditioned translation prompt>","chosen":"L'entreprise a décidé de mettre fin au service.","rejected":"L'entreprise a pris la décision de mettre fin au service."}
{"source_id":"example-000001","feature":"style","feature_value":"literal","prompt":"<style-conditioned translation prompt>","chosen":"L'entreprise a pris la décision de mettre fin au service.","rejected":"L'entreprise a décidé de mettre fin au service."}
```

The prompt above is a **placeholder**. Inspect TranslateGemma's actual chat template and tokenizer before implementation. The same formatter must be used for training and inference. Detect contradictory pairs, duplicates, and cross-split leakage. Maintain traceability to validation evidence.

### 05 — Fine-tuning

Use Transformers + PEFT + TRL, initially **DPO only**. Freeze `google/translategemma-12b-it`; train **one shared LoRA adapter** conditioned on style. Both reversed preference records update the same adapter. Keep the reference policy explicit and fixed per experiment, initially the original TranslateGemma. Evaluate single-H100 memory feasibility before choosing reference-model handling; consider reference log-probability precomputation or supported adapter-based strategies. Make BF16, LoRA settings, gradient accumulation, checkpointing, DPO beta, batch size, max sequence length, and optional quantization configurable. Do not claim memory compatibility until tested.

Baselines: unmodified TranslateGemma without style control, unmodified TranslateGemma with style prompts, and style-DPO LoRA. SFT and GRPO are future optional experiments, not initial implementations.

### 06 — Evaluation

On held-out sources, generate both style modes with base and adapted models under comparable decoding settings. Assess adequacy, grammar, terminology, idiomaticity, source closeness, pairwise style-switch success, identical-output frequency, and cases with no legitimate contrast. Use automated MT metrics **plus** a configurable LLM judge, with optional human annotations. Prioritize measuring whether style control improves **without degrading the original TranslateGemma's idiomatic naturalness**. Store per-item results, aggregates, failure cases, and uncertainty estimates where feasible.

### 07 — Analysis

Analyze acceptance/rejection rates, style contrast types, length and lexical-overlap shortcuts, domain/language effects, teacher-origin bias, terminology, and base-versus-adapted behavior. Produce simple reproducible tables and plots, not a web dashboard.

## 5. Configuration and provenance

Use YAML configs and a lightweight typed configuration layer. Keep model identifiers, **local shared paths**, teacher/judge models, corpus paths, feature definitions, training settings, evaluation settings, and SLURM parameters configurable. Preserve resolved config, dataset version, model revisions, generation and judge prompts, seeds, code revision, dependency versions, and job IDs with each run. Avoid overwriting prior runs. Do not commit credentials.

Example **unresolved** model config:

```yaml
model:
  id: google/translategemma-12b-it
  path_env: TRANSLATEGEMMA_MODEL_PATH
  local_files_only: true
```

No model loading or downloads should occur during config validation or CPU-only tests.

## 6. Jean Zay job design

Each stage keeps its SLURM template and its ordered `run.sh` command log beside the Python entry point. GPU stages request a single H100; CPU-only stages should not request a GPU. Jobs reuse the existing project virtual environment under `$SCRATCH_DIR/venvs/`, set caches and job-specific temp paths, validate inputs, and write logs to scratch. All site-specific directives are explicit TODOs until confirmed. Support offline operation and a separately authorized model-staging workflow if needed. Do not submit jobs automatically.

## 7. Extensible features

A feature should declare its values, instruction text, candidate-generation guidance, validation criteria, and preference-record construction. The common data handling, DPO training, and evaluation execution should not depend on hardcoded style branches. Implement `style` first; document how `register` or `terminology` could later plug in, without building them prematurely.

## 8. Tests and engineering standards

Use readable Python modules, CPU-only tests, and pinned compatible dependencies when the environment is established. CPU-only tests should cover schemas, source-level splits, reversed preference construction, prompt formatting, configuration and scratch path resolution, and serialization. Keep GPU integration tests opt-in. No unit test should download a model or need Jean Zay access.

## 9. Incremental implementation sequence

### Phase 1 — Structure only (**do this first**)

- Create the directory tree and stage READMEs.
- Add package skeleton and thin stage entry points, clearly marked as unimplemented.
- Add `.gitignore`, `.env.example`, and example YAML configs with TODOs for missing details.
- Add SLURM template files that **cannot accidentally submit meaningful GPU jobs** before site-specific configuration.
- Add minimal environment initialization and scratch-path helpers, without creating environments or downloading dependencies automatically.
- Add basic CPU-only tests for configuration and path handling, if feasible without external dependencies.
- Document what is scaffolded versus operational.

**Do not:** train, download/copy models, install dependencies, submit SLURM jobs, generate datasets, or fabricate site-specific settings.

### Phase 2 — Data and candidate generation

Implement corpus ingestion and candidate generation after confirming source corpora, language pairs, model paths, and teacher configuration.

### Phase 3 — Validation and preference records

Implement independent quality/style validation and bidirectional DPO record construction; calibrate the judge on human examples.

### Phase 4 — Training

Verify TranslateGemma prompt formatting and single-H100 memory strategy; implement and test DPO LoRA training.

### Phase 5 — Evaluation and analysis

Implement baseline/adapted comparisons, automated metrics, LLM judging, reports, and research analyses.

## 10. Open decisions — fill in only when needed

- Persistent Git repository path on Jean Zay
- Actual shared path and revision of TranslateGemma
- Jean Zay SLURM account, partition, GPU directives, and module setup
- Available Python/CUDA/PyTorch environment
- Initial language pair(s) and corpus locations
- Teacher model and local path
- Judge model and local path
- Evaluation metric versions and human annotation process
- Dataset sizes and acceptance thresholds
- LoRA/DPO hyperparameters and memory strategy

**Do not guess these values.** Keep placeholders and request a decision only when the corresponding stage is being implemented.

## 11. Phase 1 acceptance criteria

Codex's first deliverable is a coherent, navigable repository scaffold: distinct stage directories with documented responsibilities; an importable package skeleton; configuration templates; Jean Zay storage conventions; safe SLURM placeholders; and CPU-only tests. Nothing should pretend to perform real inference or training yet. End with a concise summary of created files, tests run, and unresolved decisions.
