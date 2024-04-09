from pathlib import Path

import google.protobuf.text_format as txtf

from hf_evaluator.evaluation import main

from .tira_messages_pb2 import Evaluation


def test_csv(tmp_path: Path, csv_references: Path, csv_predictions: Path) -> None:
    """Test CSV evaluation."""
    output_path = tmp_path / "evaluation.prototext"
    args = [
        "--references",
        str(csv_references),
        "--predictions",
        str(csv_predictions),
        "--output-prototext",
        str(output_path),
        "--metrics",
        "accuracy",
        "precision",
        "recall",
        "f1",
        "--data-format",
        "csv",
    ]
    main(args)

    evaluation = Evaluation()
    measures = txtf.Parse(output_path.read_text(), evaluation).measure
    for measure in measures:
        if measure.key == "Accuracy":
            assert float(measure.value) == 0.4
        elif measure.key == "Precision":
            assert float(measure.value) == 0.5
        elif measure.key == "Recall":
            assert float(measure.value) == 1 / 3
        elif measure.key == "F1":
            assert float(measure.value) == 0.4
        else:
            raise ValueError(f"Unknown measure: {measure.key}")


def test_json(tmp_path: Path, json_references: Path, json_predictions: Path) -> None:
    output_path = tmp_path / "evaluation.prototext"
    args = [
        "--references",
        str(json_references),
        "--predictions",
        str(json_predictions),
        "--output-prototext",
        str(output_path),
        "--metrics",
        "accuracy",
        "precision",
        "recall",
        "f1",
        "--data-format",
        "json",
        "--index-column",
        "id",
        "--label-column",
        "label",
    ]
    main(args)

    evaluation = Evaluation()
    measures = txtf.Parse(output_path.read_text(), evaluation).measure
    for measure in measures:
        if measure.key == "Accuracy":
            assert float(measure.value) == 0.4
        elif measure.key == "Precision":
            assert float(measure.value) == 0.5
        elif measure.key == "Recall":
            assert float(measure.value) == 1 / 3
        elif measure.key == "F1":
            assert float(measure.value) == 0.4
        else:
            raise ValueError(f"Unknown measure: {measure.key}")


def test_seqeval(tmp_path: Path, iob_references: Path, iob_predictions: Path) -> None:
    """Test IOB evaluation."""
    output_path = tmp_path / "evaluation.prototext"
    args = [
        "--references",
        str(iob_references),
        "--predictions",
        str(iob_predictions),
        "--output-prototext",
        str(output_path),
        "--metrics",
        "seqeval",
        "--data-format",
        "IOB1",
    ]
    main(args)

    evaluation = Evaluation()
    measures = txtf.Parse(output_path.read_text(), evaluation).measure
    labels = ["Misc", "Per", "Overall"]
    metrics = ["Precision", "Recall", "F1", "Accuracy", "Number"]
    for measure in measures:
        label, metric = measure.key.split(" ")
        assert label in labels
        assert metric in metrics
        assert float(measure.value) == 1


def test_ner_eval(tmp_path: Path, iob_references: Path, iob_predictions: Path) -> None:
    """Test IOB evaluation."""
    output_path = tmp_path / "evaluation.prototext"
    args = [
        "--references",
        str(iob_references),
        "--predictions",
        str(iob_predictions),
        "--output-prototext",
        str(output_path),
        "--metrics",
        "fschlatt/ner_eval",
        "--data-format",
        "IOB1",
        "--kwargs",
        '{"modes": ["partial", "exact"]}',
    ]
    main(args)

    evaluation = Evaluation()
    measures = txtf.Parse(output_path.read_text(), evaluation).measure
    labels = ["Misc", "Per", "Overall"]
    modes = ["Partial", "Exact"]
    metrics = ["Precision", "Recall", "F1"]
    for measure in measures:
        label, mode, metric = measure.key.split(" ")
        assert label in labels
        assert mode in modes
        assert metric in metrics
        assert float(measure.value) == 1
