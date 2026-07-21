from dataclasses import fields
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from flexsense_guard import MotorSideMeasurement

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
INPUT_SCHEMA_PATH = (
    REPOSITORY_ROOT / "common" / "schemas" / "motor_side_measurement.schema.json"
)


def _load_input_schema() -> dict[str, object]:
    return json.loads(INPUT_SCHEMA_PATH.read_text(encoding="utf-8"))


def test_python_input_fields_match_schema() -> None:
    schema_fields = set(_load_input_schema()["properties"])
    python_fields = {field.name for field in fields(MotorSideMeasurement)}

    assert python_fields == schema_fields
    assert "motor_torque_nm" not in schema_fields
    assert {
        "torque_command_nm",
        "motor_torque_applied_nm",
        "motor_torque_measured_nm",
    }.issubset(schema_fields)
    assert {
        "true_load_position_rad",
        "true_load_velocity_rad_s",
        "true_external_torque_nm",
    }.isdisjoint(schema_fields)


def test_legacy_torque_field_is_rejected() -> None:
    validator = Draft202012Validator(_load_input_schema())
    invalid_measurement = {
        "timestamp_s": 0.0,
        "motor_position_rad": 0.0,
        "motor_velocity_rad_s": 0.0,
        "motor_current_a": 0.0,
        "motor_torque_nm": 0.0,
        "torque_command_nm": 0.0,
        "encoder_valid": True,
        "current_valid": True,
        "timestamp_valid": True,
        "saturation_flag": False,
    }

    assert list(validator.iter_errors(invalid_measurement))
