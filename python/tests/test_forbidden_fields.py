import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIRECTORY = REPOSITORY_ROOT / "common" / "schemas"


def _schema_property_names(value: object) -> set[str]:
    if isinstance(value, dict):
        names = set(value.get("properties", {}))
        for child in value.values():
            names.update(_schema_property_names(child))
        return names
    if isinstance(value, list):
        names: set[str] = set()
        for child in value:
            names.update(_schema_property_names(child))
        return names
    return set()


def test_forbidden_public_fields_are_absent() -> None:
    property_names: set[str] = set()
    for schema_path in SCHEMA_DIRECTORY.glob("*.schema.json"):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        property_names.update(_schema_property_names(schema))

    assert "contact_probability" not in property_names
    assert "force_n" not in property_names
    assert "motor_torque_nm" not in property_names


def test_required_torque_fields_are_present() -> None:
    schema = json.loads(
        (SCHEMA_DIRECTORY / "motor_side_measurement.schema.json").read_text(
            encoding="utf-8"
        )
    )
    properties = set(schema["properties"])

    assert {
        "torque_command_nm",
        "motor_torque_applied_nm",
        "motor_torque_measured_nm",
    }.issubset(properties)
