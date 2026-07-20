"""Typed boundary contracts; no plant or observer algorithm is implemented here."""

from dataclasses import dataclass
from enum import StrEnum


class OperationMode(StrEnum):
    """Supported high-level operating modes."""

    NORMAL = "normal"
    VIBRATION_SUPPRESSION = "vibration_suppression"
    SAFE_SLOWDOWN = "safe_slowdown"
    DEGRADED = "degraded"


class ReasonCode(StrEnum):
    """Traceable reasons for a valid or degraded estimate."""

    NONE = "none"
    INVALID_TIMESTAMP = "invalid_timestamp"
    INVALID_ENCODER = "invalid_encoder"
    INVALID_CURRENT = "invalid_current"
    TORQUE_SATURATED = "torque_saturated"
    LOW_CONFIDENCE = "low_confidence"


@dataclass(frozen=True, slots=True)
class MotorSideMeasurement:
    """Observer input measured at the motor side only."""

    timestamp_s: float
    motor_position_rad: float
    motor_velocity_rad_s: float
    motor_current_a: float
    motor_torque_nm: float
    torque_command_nm: float
    encoder_valid: bool
    current_valid: bool
    timestamp_valid: bool
    saturation_flag: bool

    def __post_init__(self) -> None:
        if self.timestamp_s < 0:
            raise ValueError("timestamp_s must be non-negative")


@dataclass(frozen=True, slots=True)
class VirtualSensingEstimate:
    """Virtual-sensing output; score fields are engineering scores, not probabilities."""

    estimated_load_position_rad: float
    estimated_load_velocity_rad_s: float
    estimated_torsion_rad: float
    estimated_external_torque_nm: float
    innovation_norm: float
    confidence_score: float
    contact_score: float
    operation_mode: OperationMode
    valid_flag: bool
    reason_codes: tuple[ReasonCode, ...]

    def __post_init__(self) -> None:
        if self.innovation_norm < 0:
            raise ValueError("innovation_norm must be non-negative")
        for name, score in (
            ("confidence_score", self.confidence_score),
            ("contact_score", self.contact_score),
        ):
            if not 0.0 <= score <= 1.0:
                raise ValueError(f"{name} must be within [0, 1]")
