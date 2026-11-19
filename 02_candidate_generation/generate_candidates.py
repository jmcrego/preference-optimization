"""Generate reference-assisted translation pairs with offline vLLM."""

import argparse
import hashlib
from itertools import islice
import json
import os
from pathlib import Path
import re
from tempfile import NamedTemporaryFile


LABEL = re.compile(r"^[ \t]*(LITERAL|IDIOMATIC):[ \t]*", re.MULTILINE)


def parse_pair(text):
    labels = list(LABEL.finditer(text))
    if [label.group(1) for label in labels] != ["LITERAL", "IDIOMATIC"]:
        return None, None
    first, second = labels
    literal = text[first.end():second.start()].strip()
    idiomatic = text[second.end():].strip()
    if text[:first.start()].strip() or not literal or not idiomatic:
        return None, None
    return literal, idiomatic


def read_dataset(path, source_language, target_language):
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise ValueError("expected a JSON object")
                if "reference" not in row and "target" in row:
                    row["reference"] = row["target"]
                for key in ("source", "reference"):
                    if not isinstance(row.get(key), str) or not row[key].strip():
                        raise ValueError(f"expected nonempty {key} text")
                for key, expected in (
                    ("source_language", source_language),
                    ("target_language", target_language),
                ):
                    if key in row and row[key] != expected:
                        raise ValueError(f"{key} conflicts with requested language {expected}")
            except ValueError as error:
                raise ValueError(f"{path}:{line_number}: {error}") from error
            yield {
                "id": row.get("id", f"row-{line_number:06d}"),
                "source_language": source_language,
                "target_language": target_language,
                "source": row["source"],
                "reference": row["reference"],
            }


def generate(args):
    destination = args.output_dir / f"{args.prompt.stem}.jsonl"
    if destination.exists():
        raise FileExistsError(f"Output already exists: {destination}")
    template = args.prompt.read_text(encoding="utf-8")
    fields = ("source", "reference", "source_language", "target_language")
    if any("{" + field + "}" not in template for field in fields):
        raise ValueError(f"Prompt must contain these placeholders: {', '.join(fields)}")
    template.format(**dict.fromkeys(fields, ""))
    model_path = Path(args.model_path).expanduser().resolve()
    if not (model_path / "config.json").is_file():
        raise ValueError(f"Expected a local TranslateGemma directory with config.json: {model_path}")

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    # vLLM's inspection subprocess starts Python without the parent's -I flag.
    os.environ.pop("PYTHONPATH", None)
    os.environ["PYTHONNOUSERSITE"] = "1"
    os.environ["PYTHONSAFEPATH"] = "1"
    from vllm import LLM, SamplingParams

    decoding = {"temperature": 0.0, "max_tokens": args.max_tokens, "seed": args.seed}
    # This text-only experiment does not need vLLM to profile dummy images.
    llm = LLM(
        model=str(model_path),
        tensor_parallel_size=1,
        seed=args.seed,
        limit_mm_per_prompt={"image": 0},
    )
    tokenizer = llm.get_tokenizer()
    start_token = "<start_of_turn>"
    end_token = "<end_of_turn>"
    vocab = tokenizer.get_vocab()
    if tokenizer.bos_token_id is None or not {start_token, end_token} <= vocab.keys():
        raise ValueError("Local tokenizer is missing Gemma conversation tokens")
    sampling = SamplingParams(**decoding, stop_token_ids=[vocab[end_token]])
    provenance = {
        "prompt_name": args.prompt.stem,
        "prompt_sha256": hashlib.sha256(template.encode("utf-8")).hexdigest(),
        "model_path": str(model_path),
        "decoding": decoding,
    }

    rows = read_dataset(args.dataset, args.source_language, args.target_language)
    if args.limit is not None:
        rows = islice(rows, args.limit)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(mode="w", encoding="utf-8", dir=args.output_dir) as output:
        while batch := list(islice(rows, args.batch_size)):
            prompts = []
            for row in batch:
                instruction = template.format(**row).rstrip()
                prompt = f"{start_token}user\n{instruction}{end_token}\n{start_token}model\n"
                tokens = tokenizer.encode(prompt, add_special_tokens=False)
                prompts.append({"prompt_token_ids": [tokenizer.bos_token_id, *tokens]})
            results = llm.generate(prompts, sampling)
            if len(results) != len(batch):
                raise RuntimeError("vLLM returned an unexpected number of completions")
            for row, result in zip(batch, results):
                completion = result.outputs[0]
                literal, idiomatic = parse_pair(completion.text)
                if completion.finish_reason == "length":
                    literal, idiomatic = None, None
                record = {
                    **row,
                    **provenance,
                    "literal": literal,
                    "idiomatic": idiomatic,
                    "raw_completion": completion.text,
                    "finish_reason": completion.finish_reason,
                }
                if not completion.text.strip():
                    token_ids = list(completion.token_ids)
                    record["completion_diagnostics"] = {
                        "generated_token_count": len(token_ids),
                        "first_token_ids": token_ids[:32],
                        "first_tokens_decoded": tokenizer.decode(
                            token_ids[:32], skip_special_tokens=False,
                        ),
                        "stop_reason": completion.stop_reason,
                    }
                output.write(json.dumps(record, ensure_ascii=False) + "\n")
        output.flush()
        os.link(output.name, destination)
    return destination


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", required=True, type=Path, help="JSONL with source and reference (or target)")
    parser.add_argument("--source-language", required=True)
    parser.add_argument("--target-language", required=True)
    parser.add_argument("--prompt", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--model-path", default=os.environ.get("TRANSLATEGEMMA_MODEL_PATH"))
    parser.add_argument("--limit", type=positive_int)
    parser.add_argument("--batch-size", type=positive_int, default=32)
    parser.add_argument("--max-tokens", type=positive_int, default=512)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    if not args.model_path:
        parser.error("provide --model-path or set TRANSLATEGEMMA_MODEL_PATH to the shared local model")
    try:
        print(generate(args))
    except (OSError, ValueError, RuntimeError, ImportError, KeyError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
