import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
REPORT_SCHEMA_PATH = (
    REPOSITORY_ROOT / "common" / "schemas" / "validation_report.schema.json"
)


def _load_report_schema() -> dict[str, object]:
    return json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))


def test_validation_decisions_match_project_terms() -> None:
    decisions = set(_load_report_schema()["properties"]["decision"]["enum"])

    assert decisions == {"PASS", "FAIL", "NOT_VERIFIED"}


def test_metric_fields_include_unit_suffixes() -> None:
    fields = set(_load_report_schema()["properties"])

    assert {
        "load_position_rmse_rad",
        "load_velocity_rmse_rad_s",
        "external_torque_rmse_nm",
        "vibration_velocity_rms_rad_s",
        "energy_proxy_j",
    }.issubset(fields)
    assert {
        "load_position_rmse",
        "load_velocity_rmse",
        "external_torque_rmse",
        "vibration_rms",
        "energy_proxy",
    }.isdisjoint(fields)
