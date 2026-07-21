"""跨模块公共类型契约；本模块不实现 Plant、Observer 或控制算法。"""

from dataclasses import dataclass, fields
from enum import StrEnum
from math import isfinite


class ClassificationState(StrEnum):
    """跨语言统一的分类状态。"""

    NORMAL = "NORMAL"
    FLEXIBLE_VIBRATION = "FLEXIBLE_VIBRATION"
    EXTERNAL_CONTACT = "EXTERNAL_CONTACT"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"


class OperationMode(StrEnum):
    """跨语言统一的运行模式。"""

    NORMAL_TRACKING = "NORMAL_TRACKING"
    VIBRATION_SUPPRESSION = "VIBRATION_SUPPRESSION"
    SAFE_SLOWDOWN = "SAFE_SLOWDOWN"
    LOW_CONFIDENCE_DEGRADED = "LOW_CONFIDENCE_DEGRADED"


class ReasonCode(StrEnum):
    """估计有效或降级的可追溯原因。"""

    NONE = "NONE"
    INVALID_TIMESTAMP = "INVALID_TIMESTAMP"
    INVALID_ENCODER = "INVALID_ENCODER"
    INVALID_CURRENT = "INVALID_CURRENT"
    TORQUE_SATURATED = "TORQUE_SATURATED"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"


def _validate_finite_values(instance: object, names: tuple[str, ...]) -> None:
    for name in names:
        if not isfinite(getattr(instance, name)):
            raise ValueError(f"{name} must be finite")


@dataclass(frozen=True, slots=True)
class MotorSideMeasurement:
    """仅包含电机侧可测量信息的运行时输入。"""

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
        numeric_fields = tuple(
            field.name
            for field in fields(self)
            if field.name
            not in {
                "encoder_valid",
                "current_valid",
                "timestamp_valid",
                "saturation_flag",
            }
        )
        _validate_finite_values(self, numeric_fields)
        if self.timestamp_s < 0:
            raise ValueError("timestamp_s must be non-negative")


@dataclass(frozen=True, slots=True)
class VirtualSensingEstimate:
    """虚拟感知公共输出；评分字段是工程评分，不是概率。"""

    timestamp_s: float
    estimated_load_position_rad: float
    estimated_load_velocity_rad_s: float
    estimated_torsion_rad: float
    estimated_external_torque_nm: float
    innovation_norm: float
    confidence_score: float
    contact_score: float
    classification_state: ClassificationState
    operation_mode: OperationMode
    valid_flag: bool
    reason_codes: tuple[ReasonCode, ...]

    def __post_init__(self) -> None:
        numeric_fields = (
            "timestamp_s",
            "estimated_load_position_rad",
            "estimated_load_velocity_rad_s",
            "estimated_torsion_rad",
            "estimated_external_torque_nm",
            "innovation_norm",
            "confidence_score",
            "contact_score",
        )
        _validate_finite_values(self, numeric_fields)
        if self.timestamp_s < 0:
            raise ValueError("timestamp_s must be non-negative")
        if self.innovation_norm < 0:
            raise ValueError("innovation_norm must be non-negative")
        for name in ("confidence_score", "contact_score"):
            score = getattr(self, name)
            if not 0.0 <= score <= 1.0:
                raise ValueError(f"{name} must be within [0, 1]")
