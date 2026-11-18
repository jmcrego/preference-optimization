# 01 Data preparation

Convert supplied train and test splits from UTF-8 TSV to JSONL with Python 3.9 or newer. Inputs ending in `.gz` are decompressed automatically. Each input is headerless, with one source and one reference per line separated by a single tab.

From the repository root, run:

```bash
python3 01_data_preparation/run.py \
  --train /path/to/train.enfr.gz \
  --test /path/to/test.enfr.gz \
  --source-language en \
  --target-language fr \
  --output-dir /path/to/new-output-directory
```

The output directory must be new. It receives `train.jsonl` and `test.jsonl`. Each row keeps its split, position, and text, including duplicates and surrounding spaces. IDs use the split and the one-based input line number.

```json
{"id":"train-000001","source_language":"en","target_language":"fr","source":"Hello","reference":"Bonjour"}
```

The converter checks the two-column layout so it can report malformed rows with their input path and line number. Corpus validation, deduplication, split assignment, and style labeling are outside this conversion.
