# 02 Candidate generation

The pilot sends two independent TranslateGemma requests per source. One asks for a literal translation and the other asks for an idiomatic translation. Each request shows the source and the human reference, which is provided only to help disambiguate the source. The model is asked to produce its own translation and return only that text. vLLM batches the requests together. The prompt uses an experimental Gemma user/model turn format. [Gemma prompt format](https://ai.google.dev/gemma/docs/core/prompt-structure)

## Run on Jean Zay

From the Jean Zay login shell, source `scripts/setup_environment.sh` to use the default shared TranslateGemma path. Export `TRANSLATEGEMMA_MODEL_PATH` before sourcing if you need a different local copy. From inside `02_candidate_generation/`, create `logs/` once with `mkdir -p logs`, then run `bash run.sh` to submit the pilot. SLURM writes logs under `./logs/`.

The batch script loads the H100 modules, uses the project venv if present, and invokes `generate_candidates.py` with `srun`. It uses `python3 -I` so user-site packages do not shadow dependencies. vLLM must be available in the selected Python environment. The batch command in [generate_candidates.slurm](generate_candidates.slurm) takes the first three English-to-French training rows and writes under `datasets/generated/enfr/diagnostics/`. Edit the batch command to change the pilot or remove `--limit` for the full input.

The Python CLI accepts JSONL with `source` and either `reference` or `target`. Existing IDs are carried through. Prompt files must include `{source}`, `{reference}`, `{source_language}`, `{target_language}`, and `{style_instruction}`.

## Output

The prompt [reference_guided_independent_styles.txt](prompts/reference_guided_independent_styles.txt) produces `reference_guided_independent_styles.jsonl`. Each row contains the source, reference, language codes, `literal`, `idiomatic`, and generation metadata. The `completions` object records each style's instruction, raw text, and finish reason. An empty or truncated response sets only that style's candidate to null. Empty responses also record token diagnostics. Stage 03 can review identical translations and decide whether they are ties. Existing output files are protected against overwrite.
