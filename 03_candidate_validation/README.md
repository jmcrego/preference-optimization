# 03 Candidate validation

Run quality estimation first, then run Qwen judging on the scored JSONL. Both passes preserve the Stage 02 fields and write a new JSONL with the same row order. Repeat the procedure for each Stage 02 experiment. Existing outputs are protected against overwrite.

## 1. Score each translation

`score_quality.py` accepts local COMETKiwi or xCOMET checkpoints through `unbabel-comet`. It scores each candidate against the English source using reference-free inputs. The output adds `quality_estimation.<metric>.candidates.literal` and `quality_estimation.<metric>.candidates.idiomatic`. Each contains a numeric score and error spans when the checkpoint provides them. A missing candidate has a null score entry. To add a second metric, pass the first score file as input and select a different output. Use compatible locally available encoder and tokenizer files or caches with the checkpoint. [COMET scoring API](https://github.com/Unbabel/COMET#scoring-within-python)

From inside `03_candidate_validation/`, create `logs/` once. Source the project environment from your login shell and set the checkpoint path before submitting. This example scores the draft-rewrite candidates.

```bash
source ../scripts/setup_environment.sh
mkdir -p logs
input="$SCRATCH_DIR/datasets/generated/enfr/human_draft_style_rewrite/human_draft_style_rewrite.jsonl"
scored="$SCRATCH_DIR/datasets/validated/enfr/human_draft_style_rewrite/cometkiwi.jsonl"

bash run.sh quality --input "$input" --output "$scored" \
    --metric cometkiwi --checkpoint "$COMETKIWI_CHECKPOINT"
```

Use `--metric xcomet` with a compatible local xCOMET checkpoint. Both CLIs accept `--limit` and `--batch-size` for calibration runs.

## 2. Judge with Qwen

After scoring has finished, pass the path of an existing shared Qwen model directory in `QWEN_MODEL_PATH`.

```bash
bash run.sh mqm --input "$scored" \
    --output "$SCRATCH_DIR/datasets/validated/enfr/human_draft_style_rewrite/mqm.jsonl" \
    --model-path "$QWEN_MODEL_PATH"
```

Qwen sees the source and randomized A/B candidates. Its prompt excludes the human reference, generator identity, intended styles, and metric scores. The `mqm_judgment` object records the order, raw response, mapped adequacy, grammar, and terminology errors with severity and evidence, and separate naturalness and source-closeness judgments. The script retains ties and uncertainty and marks missing candidates or invalid judge responses explicitly.

Judge calibration and acceptance thresholds remain open. These scripts annotate the corpus. They do not remove rows or substitute corrected translations.
