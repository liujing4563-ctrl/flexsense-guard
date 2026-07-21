import copy
import json
from collections.abc import Callable
from pathlib import Path

from jsonschema import Draft202012Validator

from flexsense_guard import (
    IntegrationValidationResult,
    ValidationReport,
    ValidationStage,
    VerificationDecision,
)


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


def test_integration_report_may_omit_non_applicable_envelope_fields(
    validator_for: Callable[[str], Draft202012Validator],
) -> None:
    report = _p1_report()
    report["stage"] = "INTEGRATION"
    for field_name in (
        "algorithm_version",
        "random_seed",
        "software_environment",
        "runtime_ms",
    ):
        report.pop(field_name)
    report["result"] = {
        "contract_replay_passed": False,
        "component_versions": {
            "python_contract": "2.0.0",
            "json_schema": "2.0.0",
        },
        "contract_violation_count": 1,
    }
    validator = validator_for("validation_report.schema.json")

    assert not list(validator.iter_errors(report))

    python_report = ValidationReport(
        schema_version="2.0.0",
        report_id="integration-contract-001",
        experiment_id="integration-exp-001",
        stage=ValidationStage.INTEGRATION,
        git_commit="0123456789abcdef",
        configuration_id="integration-config-v1",
        scenario_id="contract-replay",
        decision=VerificationDecision.NOT_VERIFIED,
        valid_flag=False,
        failure_reason_codes=("CONTRACT_VIOLATION",),
        artifact_index=(),
        result=IntegrationValidationResult(
            contract_replay_passed=False,
            component_versions={"python_contract": "2.0.0"},
            contract_violation_count=1,
        ),
    )

    assert python_report.algorithm_version is None
    assert python_report.random_seed is None
    assert python_report.software_environment is None
    assert python_report.runtime_ms is None


def test_optional_envelope_fields_reject_placeholder_values(
    validator_for: Callable[[str], Draft202012Validator],
) -> None:
    validator = validator_for("validation_report.schema.json")

    for field_name, placeholder in (
        ("algorithm_version", ""),
        ("software_environment", {}),
        ("software_environment", {"python": ""}),
        ("software_environment", {"": "3.12"}),
    ):
        report = _p1_report()
        report[field_name] = placeholder
        assert list(validator.iter_errors(report)), field_name


def test_report_decisions_match_project_terms(
    schema_documents: dict[str, dict[str, object]],
) -> None:
    decisions = schema_documents["contract_common.schema.json"]["$defs"][
        "verification_decision"
    ]["enum"]

    assert set(decisions) == {"PASS", "FAIL", "NOT_VERIFIED"}


def test_envelope_requires_only_cross_stage_metadata(
    schema_documents: dict[str, dict[str, object]],
) -> None:
    required = set(
        schema_documents["validation_report_envelope.schema.json"]["required"]
    )

    assert {
        "schema_version",
        "report_id",
        "experiment_id",
        "stage",
        "git_commit",
        "configuration_id",
        "scenario_id",
        "decision",
        "valid_flag",
        "failure_reason_codes",
        "artifact_index",
    } == required
    assert not {
        "algorithm_version",
        "random_seed",
        "software_environment",
        "runtime_ms",
    } & required


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
