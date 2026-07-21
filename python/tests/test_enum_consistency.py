import json
from pathlib import Path

from flexsense_guard import ClassificationState, OperationMode, ReasonCode

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIRECTORY = REPOSITORY_ROOT / "common" / "schemas"


def _load_schema(name: str) -> dict[str, object]:
    return json.loads((SCHEMA_DIRECTORY / name).read_text(encoding="utf-8"))


def test_state_enums_match_python_contract() -> None:
    properties = _load_schema("system_state.schema.json")["properties"]

    assert set(properties["classification_state"]["enum"]) == {
        item.value for item in ClassificationState
    }
    assert set(properties["operation_mode"]["enum"]) == {
        item.value for item in OperationMode
    }
    assert set(properties["reason_codes"]["items"]["enum"]) == {
        item.value for item in ReasonCode
    }


def test_score_and_status_contracts_are_bounded() -> None:
    state_properties = _load_schema("system_state.schema.json")["properties"]
    report_properties = _load_schema("validation_report.schema.json")["properties"]

    for field in ("confidence_score", "contact_score"):
        assert state_properties[field]["minimum"] == 0
        assert state_properties[field]["maximum"] == 1
    assert state_properties["reason_codes"]["type"] == "array"
    assert state_properties["reason_codes"]["items"]["type"] == "string"
    assert state_properties["valid_flag"]["type"] == "boolean"
    assert set(report_properties["decision"]["enum"]) == {
        "PASS",
        "FAIL",
        "NOT_VERIFIED",
    }
