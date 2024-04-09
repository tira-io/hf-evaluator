import pytest
from pathlib import Path
from pytest import TempPathFactory


@pytest.fixture(scope="session")
def csv_references(tmp_path_factory: TempPathFactory) -> Path:
    csv_references_path = tmp_path_factory.mktemp("data") / "csv_references"
    csv_references_path.write_text("\n".join(["label", "0", "0", "1", "1", "1"]))
    return csv_references_path


@pytest.fixture(scope="session")
def csv_predictions(tmp_path_factory: TempPathFactory) -> Path:
    csv_predictions_path = tmp_path_factory.mktemp("data") / "csv_predictions"
    csv_predictions_path.write_text("\n".join(["label", "0", "1", "0", "0", "1"]))
    return csv_predictions_path


@pytest.fixture(scope="session")
def json_references(tmp_path_factory: TempPathFactory) -> Path:
    json_references_path = tmp_path_factory.mktemp("data") / "json_references"
    json_references_path.write_text(
        '[{"label": "0"}, {"label": "0"}, {"label": "1"}, {"label": "1"}, {"label": "1"}]'
    )
    return json_references_path


@pytest.fixture(scope="session")
def json_predictions(tmp_path_factory: TempPathFactory) -> Path:
    json_predictions_path = tmp_path_factory.mktemp("data") / "json_predictions"
    json_predictions_path.write_text(
        '[{"label": "0"}, {"label": "1"}, {"label": "0"}, {"label": "0"}, {"label": "1"}]'
    )
    return json_predictions_path


@pytest.fixture(scope="session")
def iob_references(tmp_path_factory: TempPathFactory) -> Path:
    iob_references_path = tmp_path_factory.mktemp("data") / "iob_references"
    iob_references_path.write_text(
        "\n\n".join(
            (
                "\n".join(["O", "O", "B-MISC", "I-MISC", "I-MISC", "I-MISC", "O"]),
                "\n".join(["B-PER", "I-PER", "O"]),
            )
        )
    )
    return iob_references_path


@pytest.fixture(scope="session")
def iob_predictions(tmp_path_factory: TempPathFactory) -> Path:
    iob_predictions_path = tmp_path_factory.mktemp("data") / "iob_predictions"
    iob_predictions_path.write_text(
        "\n\n".join(
            (
                "\n".join(["O", "O", "B-MISC", "I-MISC", "I-MISC", "I-MISC", "O"]),
                "\n".join(["B-PER", "I-PER", "O"]),
            )
        )
    )
    return iob_predictions_path
