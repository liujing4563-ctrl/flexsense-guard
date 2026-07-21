from dataclasses import fields

import pytest

from flexsense_guard import (
    SCHEMA_VERSION,
    ClassificationOutput,
    ClassificationState,
    ConfidenceOutput,
    ConfidenceState,
    ModeDecision,
    ObserverEstimate,
    ObserverInput,
    OperationMode,
    PlantInputTrace,
    ReasonCode,
    SafetyActionLevel,
    SystemStateSnapshot,
)


def _field_names(dto: type) -> set[str]:
    return {field.name for field in fields(dto)}


def test_applied_torque_is_confined_to_plant_trace() -> None:
    assert "motor_torque_applied_nm" in _field_names(PlantInputTrace)
    assert "motor_torque_applied_nm" not in _field_names(ObserverInput)


def test_observer_input_contains_only_approved_fields() -> None:
    assert _field_names(ObserverInput) == {
        "schema_version",
        "timestamp_s",
        "motor_position_rad",
        "motor_velocity_rad_s",
        "motor_torque_feedback_nm",
        "encoder_valid",
        "current_valid",
        "timestamp_valid",
        "torque_valid",
        "torque_std_nm",
    }


def test_snapshot_rejects_misaligned_module_timestamps() -> None:
    observer = ObserverEstimate(
        SCHEMA_VERSION, 1.0, 0.1, 0.2, 0.01, 0.3, 0.5, True, False
    )
    confidence = ConfidenceOutput(
        SCHEMA_VERSION,
        1.0,
        0.9,
        True,
        ConfidenceState.VALID,
        (ReasonCode.NONE,),
    )
    classification = ClassificationOutput(
        SCHEMA_VERSION, 1.0, ClassificationState.NORMAL, 0.1, True
    )
    mode = ModeDecision(
        SCHEMA_VERSION,
        1.1,
        OperationMode.NORMAL_TRACKING,
        False,
        False,
        SafetyActionLevel.NONE,
        (ReasonCode.NONE,),
    )

    with pytest.raises(ValueError, match="same timestamp"):
        SystemStateSnapshot(
            SCHEMA_VERSION,
            1.0,
            observer,
            confidence,
            classification,
            mode,
        )


def test_calibration_contract_does_not_expose_plant_true_configuration(
    schema_documents: dict[str, dict[str, object]],
) -> None:
    candidate_fields = set(
        schema_documents["calibration_candidate.schema.json"]["properties"]
    )
    decision_fields = set(
        schema_documents["calibration_decision.schema.json"]["properties"]
    )
    plant_fields = set(
        schema_documents["immutable_plant_true_config.schema.json"]["properties"]
    )

    assert candidate_fields.isdisjoint(
        plant_fields - {"schema_version"}
    )
    assert decision_fields.isdisjoint(
        plant_fields - {"schema_version"}
    )
