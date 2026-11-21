"""Streaming JSONL helpers for candidate validation."""

import json
import os
from tempfile import NamedTemporaryFile


STYLES = ("literal", "idiomatic")


def positive_int(value):
    number = int(value)
    if number < 1:
        raise ValueError("expected a positive integer")
    return number


def has_text(value):
    return isinstance(value, str) and bool(value.strip())


def read_rows(path):
    with path.open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            try:
                row = json.loads(line)
                if not isinstance(row, dict) or not has_text(row.get("source")):
                    raise ValueError("expected a JSON object with nonempty source text")
            except ValueError as error:
                raise ValueError(f"{path}:{number}: {error}") from error
            yield row


def write_rows(path, rows):
    if path.exists():
        raise FileExistsError(f"Output already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent) as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
        stream.flush()
        os.link(stream.name, path)


def offline():
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
