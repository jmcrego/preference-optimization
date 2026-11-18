"""Convert supplied parallel TSV splits to translation records."""

import argparse
import gzip
import json
from pathlib import Path


def convert_split(input_path, output_path, split, source_language, target_language):
    open_input = gzip.open if input_path.suffix == ".gz" else open
    with open_input(input_path, "rt", encoding="utf-8-sig") as source_file:
        with output_path.open("x", encoding="utf-8", newline="\n") as output_file:
            for line_number, line in enumerate(source_file, start=1):
                fields = line.removesuffix("\n").split("\t")
                if len(fields) != 2:
                    raise ValueError(f"{input_path}:{line_number}: expected two tab-separated fields")
                source, reference = fields
                record = {
                    "id": f"{split}-{line_number:06d}",
                    "source_language": source_language,
                    "target_language": target_language,
                    "source": source,
                    "reference": reference,
                }
                output_file.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Convert existing train and test TSVs to JSONL.")
    parser.add_argument("--train", required=True, type=Path, help="Training TSV or gzipped TSV")
    parser.add_argument("--test", required=True, type=Path, help="Test TSV or gzipped TSV")
    parser.add_argument("--source-language", required=True)
    parser.add_argument("--target-language", required=True)
    parser.add_argument("--output-dir", required=True, type=Path, help="New output directory")
    args = parser.parse_args()

    try:
        args.output_dir.mkdir(parents=True)
        try:
            for split, input_path in (("train", args.train), ("test", args.test)):
                convert_split(
                    input_path, args.output_dir / f"{split}.jsonl", split,
                    args.source_language, args.target_language,
                )
        except (OSError, EOFError, ValueError, KeyboardInterrupt):
            for split in ("train", "test"):
                (args.output_dir / f"{split}.jsonl").unlink(missing_ok=True)
            args.output_dir.rmdir()
            raise
    except (OSError, EOFError, ValueError) as error:
        parser.exit(1, f"{error}\n")
