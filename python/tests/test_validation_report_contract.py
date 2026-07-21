import copy
import json
from collections.abc import Callable
from pathlib import Path

from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
REPORT_FIXTURE = REPOSITORY_ROOT / "configs" / "mock" / "validation_report_example.json"


def _p1_report() -> dict[str, object]:
    return json.loads(REPORT_FIXTURE.read_text(encoding="utf-8"))["payload"]


def test_p1_report_accepts_only_p1_payload(
    validator_for: Callable[[str], Draft202012Validator],
) -> None:
    report = _p1_report()
    validator = validator_for("validation_report.schema.json")

    assert not list(validator.iter_errors(report))

    invalid = copy.deepcopy(report)
    invalid["stage"] = "P2"
    assert list(validator.iter_errors(invalid))


def test_p2_report_rejects_p1_only_metrics(
    validator_for: Callable[[str], Draft202012Validator],
) -> None:
    report = _p1_report()
    report["stage"] = "P2"
    report["result"] = {
        "p2_vibration_decision": "NOT_VERIFIED",
        "p2_contact_decision": "NOT_VERIFIED",
        "false_alarm_count": 2,
        "missed_detection_count": 1,
    }
    validator = validator_for("validation_report.schema.json")

    assert not list(validator.iter_errors(report))

    report["result"]["load_position_rmse_rad"] = 0.04
    assert list(validator.iter_errors(report))


def test_report_decisions_match_project_terms(
    schema_documents: dict[str, dict[str, object]],
) -> None:
    decisions = schema_documents["contract_common.schema.json"]["$defs"][
        "verification_decision"
    ]["enum"]

    assert set(decisions) == {"PASS", "FAIL", "NOT_VERIFIED"}


def test_p1_schema_requires_median_iqr_and_seed_counts(
    schema_documents: dict[str, dict[str, object]],
) -> None:
    required = set(schema_documents["p1_validation_result.schema.json"]["required"])

    assert {
        "position_improvement_median_pct",
        "velocity_improvement_median_pct",
        "position_improvement_iqr_pct",
        "velocity_improvement_iqr_pct",
        "position_winning_seed_count",
        "velocity_winning_seed_count",
        "evaluated_seed_count",
    }.issubset(required)
