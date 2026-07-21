import json
from collections.abc import Callable
from pathlib import Path

from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MOCK_DIRECTORY = REPOSITORY_ROOT / "configs" / "mock"


def test_mock_metadata_and_payload_schemas(
    validator_for: Callable[[str], Draft202012Validator],
) -> None:
    fixtures = sorted(MOCK_DIRECTORY.glob("*.json"))

    assert fixtures
    for fixture_path in fixtures:
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        schema_name = Path(fixture["schema_path"]).name

        assert fixture["fixture_type"] == "MOCK"
        assert fixture["data_source"] == "MOCK"
        assert fixture["valid_for_algorithm_evaluation"] is False
        assert "不是" in fixture["purpose"] or "不代表" in fixture["purpose"]
        assert not list(
            validator_for(schema_name).iter_errors(fixture["payload"])
        ), fixture_path


def test_required_v2_mock_cases_exist() -> None:
    expected = {
        "actuator_command_example.json",
        "plant_input_trace_example.json",
        "raw_motor_measurement_example.json",
        "torque_feedback_example.json",
        "signal_health_status_example.json",
        "observer_input_example.json",
        "system_state_normal.json",
        "system_state_vibration.json",
        "system_state_contact.json",
        "system_state_low_confidence.json",
        "control_command_example.json",
        "nominal_parameter_version_example.json",
        "calibration_candidate_example.json",
        "calibration_decision_example.json",
        "artifact_index_entry_example.json",
        "validation_report_example.json",
    }

    assert expected.issubset({path.name for path in MOCK_DIRECTORY.glob("*.json")})


def test_validation_mock_omits_not_applicable_zero_fields() -> None:
    fixture = json.loads(
        (MOCK_DIRECTORY / "validation_report_example.json").read_text(encoding="utf-8")
    )
    result = fixture["payload"]["result"]
    not_applicable = {
        "false_alarm_count",
        "missed_detection_count",
        "detection_delay_s",
        "p2_vibration_decision",
        "p2_contact_decision",
        "confidence_drop",
        "p3_degrade_decision",
        "p3_action_decision",
        "p3_recovery_decision",
        "recovery_time_s",
    }

    assert set(result).isdisjoint(not_applicable)
    assert all(value != 0.0 for value in result.values() if isinstance(value, float))
