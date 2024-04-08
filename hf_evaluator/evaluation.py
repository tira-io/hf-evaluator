#!/usr/bin/env python3

import argparse
from pathlib import Path
from typing import Any, Dict, List, Literal
import json
import os

import evaluate
from evaluate.utils.file_utils import DownloadConfig
import pandas as pd

OFFLINE = os.environ.get("OFFLINE", False)
if OFFLINE:
    evaluate.config.HF_EVALUATE_OFFLINE = True


def to_prototext(m: List[Dict[str, Any]], upper_k: str = "") -> str:
    ret = ""

    def _to_prototext(d: Dict[str, Any], upper_k: str = "") -> str:
        ret = ""
        for k, v in d.items():
            new_k = upper_k
            if not new_k:
                new_k = k
            elif not new_k.endswith(k):
                new_k = upper_k + "_" + k
            if isinstance(v, dict):
                ret += _to_prototext(v, upper_k=new_k)
            else:
                ret += (
                    'measure{\n  key: "'
                    + str(new_k.replace("_", " ").title())
                    + '"\n  value: "'
                    + str(v)
                    + '"\n}\n'
                )
        return ret

    for d in m:
        ret += _to_prototext(d, upper_k=upper_k)

    return ret


def load_data(
    path: Path,
    data_format: Literal[
        "csv",
        "tsv",
        "json",
        "jsonl",
        "IOB1",
        "IOB2",
        "IOE1",
        "IOE2",
        "IOBES",
        "BILOU",
    ],
    label_column: str | int | None,
) -> List:
    df = None
    if data_format == "csv":
        df = pd.read_csv(path, sep=",")
    if data_format == "tsv":
        df = pd.read_csv(path, sep="\t")
    if data_format == "json":
        df = pd.read_json(path)
    if data_format == "jsonl":
        df = pd.read_json(path, lines=True)
    if df is not None:
        if isinstance(label_column, str):
            return df[label_column].tolist()
        elif isinstance(label_column, int):
            return df.iloc[:, label_column].tolist()
        return df.iloc[:, -1].tolist()
    if data_format in ("IOB1", "IOB2", "IOE1", "IOE2", "IOBES", "BILOU"):
        data = path.read_text().strip().split("\n\n")
        data = [x.split("\n") for x in data]
        return data
    else:
        raise ValueError("Unknown data format: " + data_format)


def evaluate_metrics(
    predictions: List, references: List, metrics: List[str], **kwargs
) -> List[Dict[str, Any]]:
    results = []

    download_config = None
    if OFFLINE:
        download_config = DownloadConfig(local_files_only=True)

    for metric in metrics:
        results.append(
            evaluate.load(metric, download_config=download_config).compute(
                predictions=predictions, references=references, **kwargs
            )
        )

    return results


def main(args=None):
    parser = argparse.ArgumentParser()

    parser.add_argument("--metrics", type=str, nargs="+", required=True)
    parser.add_argument(
        "--data-format",
        type=str,
        choices=[
            "csv",
            "tsv",
            "json",
            "jsonl",
            "IOB1",
            "IOB2",
            "IOE1",
            "IOE2",
            "IOBES",
            "BILOU",
        ],
        required=True,
    )
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--references", type=Path, required=True)
    parser.add_argument("--output-prototext", type=Path, required=True)
    parser.add_argument("--label-column", type=str, default=None)
    parser.add_argument("--kwargs", type=json.loads, default=None)

    args = parser.parse_args(args)

    kwargs = args.kwargs
    if kwargs is None:
        kwargs = {}

    predictions = load_data(args.predictions, args.data_format, args.label_column)
    references = load_data(args.references, args.data_format, args.label_column)
    results = evaluate_metrics(predictions, references, args.metrics, **kwargs)

    with open(args.output_prototext, "w") as f:
        f.write(to_prototext(results).strip())


if __name__ == "__main__":
    main()
