# 02 Candidate generation

The independent-styles pilot sends two independent TranslateGemma requests per source. One asks for a literal translation and the other asks for an idiomatic translation. Each request shows the source and the human reference, which is provided only to help disambiguate the source. The model is asked to produce its own translation and return only that text. vLLM batches the requests together. The prompt uses an experimental Gemma user/model turn format. [Gemma prompt format](https://ai.google.dev/gemma/docs/core/prompt-structure)

The draft-rewrite experiment sends two independent editing requests per source. Each receives the same human draft and the source. One asks for a source-close revision and the other asks for an idiomatic revision. The prompt allows the model to keep existing wording and return an unchanged draft when it already fits the requested style.

## Run on Jean Zay

From the Jean Zay login shell, source `scripts/setup_environment.sh` to use the default shared TranslateGemma path. Export `TRANSLATEGEMMA_MODEL_PATH` before sourcing if you need a different local copy. From inside `02_candidate_generation/`, create `logs/` once with `mkdir -p logs`, then run `bash run.sh` to submit the pilot. SLURM writes logs under `./logs/`.

The batch script loads the H100 modules, uses the project venv if present, and invokes `generate_candidates.py` with `srun`. It uses `python3 -I` so user-site packages do not shadow dependencies. vLLM must be available in the selected Python environment. The batch command in [generate_candidates.slurm](generate_candidates.slurm) takes the first three English-to-French training rows and writes under `datasets/generated/enfr/diagnostics/`. Edit the batch command to change the pilot or remove `--limit` for the full input.

The Python CLI accepts JSONL with `source` and either `reference` or `target`. Existing IDs are carried through. Prompt files must include `{source}`, `{reference}`, `{source_language}`, `{target_language}`, and `{style_instruction}`.

## Output

Each prompt produces a JSONL file with the same filename stem. The active [human_draft_style_rewrite.txt](prompts/human_draft_style_rewrite.txt) prompt produces `human_draft_style_rewrite.jsonl`. Each row contains the source, reference, language codes, `literal`, `idiomatic`, and generation metadata. The `completions` object records each style's instruction, raw text, and finish reason. An empty or truncated response sets only that style's candidate to null. Every completion records its token count, first 32 token IDs and their decoded text with special tokens visible, and stop reason. In the joint experiment these diagnostics are at the row level. In the two-request experiments they are under each style in `completions`. Stage 03 can review identical translations and decide whether they are ties. Existing output files are protected against overwrite.

## Recorded experiments

From this stage directory, run `bash run.sh` to submit the active `sbatch` line. Edit `run.sh` to switch experiments, leaving only one submission line active.

| Experiment | Recorded run |
| --- | --- |
| `draft-rewrite` | Two independent edits of the human draft per source, first three rows. This is the active call. |
| `independent-styles` | Two independent translations per source, first three rows. |
| `joint-styles` | Original two-label prompt, first three rows. |

The batch script selects the prompt and output directory for each experiment before running the shared command. The joint pilot uses `--joint-completion` and records one raw response and finish reason per source. Its prompt uses the four dataset placeholders and returns `LITERAL:` and `IDIOMATIC:` labels. To rerun an experiment whose JSONL already exists, change its output directory to preserve the earlier result.
