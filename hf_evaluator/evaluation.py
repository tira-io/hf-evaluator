#!/usr/bin/env python3

import argparse
from pathlib import Path
from typing import Any, Dict, List

import evaluate
from evaluate.utils.file_utils import DownloadConfig
import pandas as pd


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


def load_data(path: Path, data_format: str) -> List:
    if data_format == "csv":
        return pd.read_csv(path, sep=",").iloc[:, -1].tolist()
    if data_format == "tsv":
        return pd.read_csv(path, sep="\t").iloc[:, -1].tolist()
    if data_format in ("IOB1", "IOB2", "IOE1", "IOE2", "IOBES", "BILOU"):
        data = path.read_text().strip().split("\n\n")
        data = [x.split("\n") for x in data]
        return data
    else:
        raise ValueError("Unknown data format: " + data_format)


def evaluate_metrics(
    predictions: List, references: List, metrics: List[str]
) -> List[Dict[str, Any]]:
    results = []

    for metric in metrics:
        results.append(
            evaluate.load(
                metric, download_config=DownloadConfig(local_files_only=True)
            ).compute(predictions=predictions, references=references)
        )

    return results


def main(args=None):
    parser = argparse.ArgumentParser()

    parser.add_argument("--metrics", type=str, nargs="+", required=True)
    parser.add_argument(
        "--data-format",
        type=str,
        choices=["csv", "tsv", "IOB1", "IOB2", "IOE1", "IOE2", "IOBES", "BILOU"],
        required=True,
    )
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--references", type=Path, required=True)
    parser.add_argument("--output-prototext", type=Path, required=True)

    args = parser.parse_args(args)

    predictions = load_data(args.predictions, args.data_format)
    references = load_data(args.references, args.data_format)
    results = evaluate_metrics(predictions, references, args.metrics)

    with open(args.output_prototext, "w") as f:
        f.write(to_prototext(results).strip())


if __name__ == "__main__":
    main()
