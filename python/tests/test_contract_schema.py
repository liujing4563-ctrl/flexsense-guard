from dataclasses import fields
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from flexsense_guard import (
    ClassificationState,
    OperationMode,
    ReasonCode,
    VirtualSensingEstimate,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPOSITORY_ROOT / "common" / "schemas" / "system_state.schema.json"


def _load_schema() -> dict[str, object]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _valid_state() -> dict[str, object]:
    return {
        "timestamp_s": 0.0,
        "estimated_load_position_rad": 0.0,
        "estimated_load_velocity_rad_s": 0.0,
        "estimated_torsion_rad": 0.0,
        "estimated_external_torque_nm": 0.0,
        "innovation_norm": 0.0,
        "confidence_score": 1.0,
        "contact_score": 0.0,
        "classification_state": "NORMAL",
        "operation_mode": "NORMAL_TRACKING",
        "valid_flag": True,
        "reason_codes": ["NONE"],
    }


def test_public_enums_match_schema() -> None:
    schema = _load_schema()
    properties = schema["properties"]

    assert {state.value for state in ClassificationState} == set(
        properties["classification_state"]["enum"]
    )
    assert {mode.value for mode in OperationMode} == set(
        properties["operation_mode"]["enum"]
    )
    assert {reason.value for reason in ReasonCode} == set(
        properties["reason_codes"]["items"]["enum"]
    )


def test_python_output_fields_match_schema() -> None:
    schema_fields = set(_load_schema()["properties"])
    python_fields = {field.name for field in fields(VirtualSensingEstimate)}

    assert python_fields == schema_fields
    assert "contact_probability" not in schema_fields
    assert {
        "true_load_position",
        "true_load_velocity",
        "true_external_torque",
    }.isdisjoint(schema_fields)


def test_valid_example_matches_schema() -> None:
    validator = Draft202012Validator(_load_schema())

    assert not list(validator.iter_errors(_valid_state()))


def test_contact_probability_is_rejected() -> None:
    validator = Draft202012Validator(_load_schema())
    invalid_state = _valid_state()
    invalid_state["contact_probability"] = 0.5

    assert list(validator.iter_errors(invalid_state))
