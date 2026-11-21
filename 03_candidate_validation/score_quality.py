"""Add local COMETKiwi or xCOMET quality scores to Stage 02 JSONL."""

import argparse
from itertools import islice
from pathlib import Path

from validation_io import STYLES, has_text, offline, positive_int, read_rows, write_rows


def score_rows(rows, model, args):
    while batch := list(islice(rows, args.batch_size)):
        samples = []
        destinations = []
        for row in batch:
            metrics = row.setdefault("quality_estimation", {})
            if args.metric in metrics:
                raise ValueError(f"Row {row.get('id')} already has scores for {args.metric}")
            scores = dict.fromkeys(STYLES)
            metrics[args.metric] = {"checkpoint": str(args.checkpoint), "candidates": scores}
            for style in STYLES:
                if has_text(row.get(style)):
                    samples.append({"src": row["source"], "mt": row[style]})
                    destinations.append((scores, style))
        if samples:
            prediction = model.predict(samples, batch_size=args.batch_size, gpus=args.gpus)
            scores = prediction.scores
            spans = getattr(getattr(prediction, "metadata", None), "error_spans", None)
            if len(scores) != len(samples) or (spans is not None and len(spans) != len(samples)):
                raise RuntimeError("COMET returned a different number of predictions than requested")
            for index, (candidates, style) in enumerate(destinations):
                candidates[style] = {"score": float(scores[index])}
                if spans is not None:
                    candidates[style]["error_spans"] = spans[index]
        yield from batch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metric", choices=("cometkiwi", "xcomet"), required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--gpus", type=int, choices=(0, 1), default=1)
    parser.add_argument("--batch-size", type=positive_int, default=8)
    parser.add_argument("--limit", type=positive_int)
    args = parser.parse_args()
    args.checkpoint = args.checkpoint.expanduser().resolve()
    if not args.checkpoint.is_file():
        parser.error(f"Expected a local COMET checkpoint file: {args.checkpoint}")
    if args.output.exists():
        parser.error(f"Output already exists: {args.output}")

    try:
        offline()
        from comet import load_from_checkpoint

        model = load_from_checkpoint(str(args.checkpoint), local_files_only=True)
        rows = islice(read_rows(args.input), args.limit)
        write_rows(args.output, score_rows(rows, model, args))
    except (OSError, ValueError, ImportError, RuntimeError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
