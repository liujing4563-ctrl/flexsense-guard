from dataclasses import fields

import pytest

from flexsense_guard import (
    MotorSideMeasurement,
    OperationMode,
    ReasonCode,
    VirtualSensingEstimate,
)


def test_public_contract_can_be_imported_and_constructed() -> None:
    measurement = MotorSideMeasurement(
        timestamp_s=0.0,
        motor_position_rad=0.0,
        motor_velocity_rad_s=0.0,
        motor_current_a=0.0,
        motor_torque_nm=0.0,
        torque_command_nm=0.0,
        encoder_valid=True,
        current_valid=True,
        timestamp_valid=True,
        saturation_flag=False,
    )
    estimate = VirtualSensingEstimate(
        estimated_load_position_rad=0.0,
        estimated_load_velocity_rad_s=0.0,
        estimated_torsion_rad=0.0,
        estimated_external_torque_nm=0.0,
        innovation_norm=0.0,
        confidence_score=1.0,
        contact_score=0.0,
        operation_mode=OperationMode.NORMAL,
        valid_flag=True,
        reason_codes=(ReasonCode.NONE,),
    )

    assert measurement.encoder_valid
    assert estimate.operation_mode is OperationMode.NORMAL
    assert "contact_probability" not in {field.name for field in fields(estimate)}


def test_scores_are_bounded() -> None:
    with pytest.raises(ValueError, match="confidence_score"):
        VirtualSensingEstimate(
            0.0, 0.0, 0.0, 0.0, 0.0, 1.1, 0.0, OperationMode.NORMAL, True, ()
        )
