"""Add blinded MQM-style Qwen judgments to Stage 03 scored JSONL."""

import argparse
import hashlib
from itertools import islice
import json
import os
from pathlib import Path
import random

from validation_io import STYLES, has_text, offline, positive_int, read_rows, write_rows


def parse_judgment(text):
    data = json.loads(text)
    if not isinstance(data, dict) or set(data) != {"A", "B", "more_natural", "more_source_close", "style_reason"}:
        raise ValueError("unexpected judgment fields")
    for label in ("A", "B"):
        if not isinstance(data[label], list):
            raise ValueError("candidate errors must be lists")
        for error in data[label]:
            if (
                not isinstance(error, dict)
                or set(error) != {"category", "severity", "span", "reason"}
                or error["category"] not in ("adequacy", "grammar", "terminology")
                or error["severity"] not in ("minor", "major", "critical")
                or not isinstance(error["span"], str)
                or not has_text(error["reason"])
            ):
                raise ValueError("invalid MQM-style error")
    for key in ("more_natural", "more_source_close"):
        if data[key] not in ("A", "B", "tie", "uncertain"):
            raise ValueError("invalid style judgment")
    if not has_text(data["style_reason"]):
        raise ValueError("missing style reason")
    return data


def judge_rows(rows, engine, tokenizer, sampling, args, rubric):
    rng = random.Random(args.seed)
    provenance = {
        "model_path": str(args.model_path),
        "rubric_sha256": hashlib.sha256(rubric.encode("utf-8")).hexdigest(),
        "seed": args.seed,
        "dtype": "bfloat16",
        "temperature": 0.0,
        "max_tokens": args.max_tokens,
    }
    while batch := list(islice(rows, args.batch_size)):
        prompts = []
        pending = []
        for row in batch:
            if "mqm_judgment" in row:
                raise ValueError(f"Row {row.get('id')} already has an MQM-style judgment")
            if not all(has_text(row.get(style)) for style in STYLES):
                row["mqm_judgment"] = {"status": "missing_candidate"}
                continue
            order = list(STYLES)
            rng.shuffle(order)
            mapping = dict(zip(("A", "B"), order))
            payload = {
                "source_language": row.get("source_language"),
                "target_language": row.get("target_language"),
                "source": row["source"],
                **{label: row[style] for label, style in mapping.items()},
            }
            prompt = tokenizer.apply_chat_template(
                [{"role": "system", "content": rubric},
                 {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
                tokenize=True, add_generation_prompt=True, enable_thinking=False,
            )
            prompts.append({"prompt_token_ids": prompt})
            pending.append((row, mapping))
        if prompts:
            results = engine.generate(prompts, sampling)
            if len(results) != len(pending):
                raise RuntimeError("vLLM returned a different number of judgments than requested")
            for (row, mapping), result in zip(pending, results):
                output = result.outputs[0]
                record = {
                    **provenance, "candidate_order": mapping, "raw_response": output.text,
                    "finish_reason": output.finish_reason,
                }
                try:
                    if output.finish_reason == "length":
                        raise ValueError("truncated judge response")
                    data = parse_judgment(output.text)
                except ValueError as error:
                    record.update(status="invalid_response", reason=str(error))
                else:
                    record.update(
                        status="judged",
                        errors={style: data[label] for label, style in mapping.items()},
                        more_natural=mapping.get(data["more_natural"], data["more_natural"]),
                        more_source_close=mapping.get(data["more_source_close"], data["more_source_close"]),
                        style_reason=data["style_reason"],
                    )
                row["mqm_judgment"] = record
        yield from batch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model-path", type=Path, required=True)
    parser.add_argument("--batch-size", type=positive_int, default=8)
    parser.add_argument("--max-tokens", type=positive_int, default=768)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--limit", type=positive_int)
    args = parser.parse_args()
    args.model_path = args.model_path.expanduser().resolve()
    if not (args.model_path / "config.json").is_file():
        parser.error(f"Expected a local Qwen model directory with config.json: {args.model_path}")
    if args.output.exists():
        parser.error(f"Output already exists: {args.output}")

    try:
        offline()
        os.environ.pop("PYTHONPATH", None)
        os.environ["PYTHONNOUSERSITE"] = "1"
        from vllm import LLM, SamplingParams

        rubric = Path(__file__).with_name("mqm_judge.txt").read_text(encoding="utf-8")
        engine = LLM(model=str(args.model_path), dtype="bfloat16", tensor_parallel_size=1, seed=args.seed)
        sampling = SamplingParams(temperature=0.0, max_tokens=args.max_tokens, seed=args.seed)
        rows = islice(read_rows(args.input), args.limit)
        write_rows(args.output, judge_rows(rows, engine, engine.get_tokenizer(), sampling, args, rubric))
    except (OSError, ValueError, ImportError, RuntimeError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
