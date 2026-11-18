# 02 Candidate generation

The first experiment uses one TranslateGemma completion per source to produce a literal translation followed by an idiomatic rewrite. The prompt gives the model both the source and the human reference. It uses an experimental Gemma user/model turn format for the two-output instruction. [Gemma prompt format](https://ai.google.dev/gemma/docs/core/prompt-structure)

## Run on Jean Zay

From the Jean Zay login shell, source `scripts/setup_environment.sh` and export `TRANSLATEGEMMA_MODEL_PATH` with the existing shared model directory. From inside `02_candidate_generation/`, create `logs/` once with `mkdir -p logs`, then run `bash run.sh` to submit the pilot. SLURM writes logs under `./logs/`.

The batch script loads the H100 modules, activates the existing project environment, and invokes `generate_candidates.py` with `srun`. The environment must have a working vLLM installation. The Python command and exact pilot arguments are in [generate_candidates.slurm](generate_candidates.slurm). It takes the first 50 rows of the English-to-French training split. Edit the batch command to change the pilot or remove `--limit` for the full input.

The Python CLI accepts Stage 01 JSONL with `source` and `reference` fields. It also accepts `target` as the reference field. Existing IDs are carried through. Pass a prompt file with `{source}`, `{reference}`, `{source_language}`, and `{target_language}` placeholders. Completions should start with `LITERAL:` and then place `IDIOMATIC:` on its own line.

## Output

The prompt [reference_assisted_literal_then_idiomatic.txt](prompts/reference_assisted_literal_then_idiomatic.txt) produces `reference_assisted_literal_then_idiomatic.jsonl` in the requested directory. Each row contains the source and reference, language codes, `literal`, `idiomatic`, raw completion, finish reason, and generation metadata. A malformed or truncated completion retains its raw text and has null candidate fields. Identical translations remain available for Stage 03 to assess. Existing output files are protected against overwrite.
