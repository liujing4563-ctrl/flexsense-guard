import pytest

from flexsense_guard import (
    SCHEMA_VERSION,
    ActuatorCommand,
    ConfidenceOutput,
    ConfidenceState,
    ModeDecision,
    ObserverInput,
    OperationMode,
    ReasonCode,
    SafetyActionLevel,
)


def test_v2_contracts_can_be_imported_and_constructed() -> None:
    command = ActuatorCommand(SCHEMA_VERSION, 0.5, 1.2)
    observer_input = ObserverInput(
        SCHEMA_VERSION,
        0.5,
        0.12,
        0.3,
        1.01,
        True,
        True,
        True,
        True,
        0.04,
    )

    assert command.torque_command_nm == 1.2
    assert observer_input.motor_torque_feedback_nm == 1.01


def test_hard_invalid_contract_rejects_valid_flag() -> None:
    with pytest.raises(ValueError, match="HARD_INVALID"):
        ConfidenceOutput(
            SCHEMA_VERSION,
            1.0,
            0.1,
            True,
            ConfidenceState.HARD_INVALID,
            (ReasonCode.ENCODER_INVALID,),
        )


def test_latched_hazard_rejects_weak_action() -> None:
    with pytest.raises(ValueError, match="SLOWDOWN"):
        ModeDecision(
            SCHEMA_VERSION,
            1.0,
            OperationMode.LOW_CONFIDENCE_DEGRADED,
            True,
            True,
            SafetyActionLevel.LIMITED,
            (ReasonCode.CONTACT_HAZARD_LATCHED,),
        )
