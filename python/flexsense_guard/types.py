"""FlexSense-Guard v2 公共数据契约；不包含任何主体算法。"""

from dataclasses import dataclass, fields
from enum import StrEnum
from math import isfinite
from typing import TypeAlias


SCHEMA_VERSION = "2.0.0"


class ClassificationState(StrEnum):
    NORMAL = "NORMAL"
    FLEXIBLE_VIBRATION = "FLEXIBLE_VIBRATION"
    EXTERNAL_CONTACT = "EXTERNAL_CONTACT"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"


class OperationMode(StrEnum):
    NORMAL_TRACKING = "NORMAL_TRACKING"
    VIBRATION_SUPPRESSION = "VIBRATION_SUPPRESSION"
    SAFE_SLOWDOWN = "SAFE_SLOWDOWN"
    LOW_CONFIDENCE_DEGRADED = "LOW_CONFIDENCE_DEGRADED"


class TorqueSource(StrEnum):
    CURRENT_ESTIMATE = "CURRENT_ESTIMATE"
    TORQUE_SENSOR = "TORQUE_SENSOR"
    ACTUATOR_MODEL = "ACTUATOR_MODEL"
    UNKNOWN = "UNKNOWN"


class ConfidenceState(StrEnum):
    VALID = "VALID"
    SOFT_DEGRADED = "SOFT_DEGRADED"
    HARD_INVALID = "HARD_INVALID"


class SafetyActionLevel(StrEnum):
    NONE = "NONE"
    LIMITED = "LIMITED"
    SLOWDOWN = "SLOWDOWN"
    STOP_REQUEST = "STOP_REQUEST"


class ReasonCode(StrEnum):
    NONE = "NONE"
    ENCODER_INVALID = "ENCODER_INVALID"
    CURRENT_INVALID = "CURRENT_INVALID"
    TIMESTAMP_INVALID = "TIMESTAMP_INVALID"
    TORQUE_INVALID = "TORQUE_INVALID"
    DATA_STALE = "DATA_STALE"
    ACTUATOR_SATURATED = "ACTUATOR_SATURATED"
    INNOVATION_EXCESSIVE = "INNOVATION_EXCESSIVE"
    MODEL_MISMATCH_SUSPECTED = "MODEL_MISMATCH_SUSPECTED"
    EXTERNAL_DYNAMIC_SUSPECTED = "EXTERNAL_DYNAMIC_SUSPECTED"
    PHYSICAL_LIMIT_VIOLATION = "PHYSICAL_LIMIT_VIOLATION"
    OBSERVER_DIVERGENCE = "OBSERVER_DIVERGENCE"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    CONTACT_HAZARD_LATCHED = "CONTACT_HAZARD_LATCHED"
    UNKNOWN_REASON = "UNKNOWN_REASON"


class CalibrationDecisionType(StrEnum):
    UPDATE = "UPDATE"
    HOLD = "HOLD"
    ROLLBACK = "ROLLBACK"


class VerificationDecision(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_VERIFIED = "NOT_VERIFIED"


class ValidationStage(StrEnum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    SIL = "SIL"
    INTEGRATION = "INTEGRATION"


def _validate_version(version: str) -> None:
    if version != SCHEMA_VERSION:
        raise ValueError(f"schema_version must be {SCHEMA_VERSION}")


def _validate_finite_values(instance: object, names: tuple[str, ...]) -> None:
    for name in names:
        if not isfinite(getattr(instance, name)):
            raise ValueError(f"{name} must be finite")


def _validate_timestamp(timestamp_s: float) -> None:
    if not isfinite(timestamp_s) or timestamp_s < 0:
        raise ValueError("timestamp_s must be finite and non-negative")


def _validate_reason_codes(reason_codes: tuple[ReasonCode, ...]) -> None:
    if not reason_codes or len(reason_codes) != len(set(reason_codes)):
        raise ValueError("reason_codes must be non-empty and unique")
    if ReasonCode.NONE in reason_codes and len(reason_codes) != 1:
        raise ValueError("NONE cannot be combined with another reason code")


def _validate_nonempty_text(value: str, name: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _validate_checksum(checksum_sha256: str) -> None:
    if len(checksum_sha256) != 64 or any(
        character not in "0123456789abcdef" for character in checksum_sha256
    ):
        raise ValueError("checksum_sha256 must be 64 lowercase hexadecimal characters")


def _validate_parameter_values(parameter_values: dict[str, float]) -> None:
    if not parameter_values:
        raise ValueError("parameter_values must be non-empty")
    if any(not name.strip() or not isfinite(value) for name, value in parameter_values.items()):
        raise ValueError("parameter_values must have non-empty names and finite values")


@dataclass(frozen=True, slots=True)
class ActuatorCommand:
    schema_version: str
    timestamp_s: float
    torque_command_nm: float

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        _validate_timestamp(self.timestamp_s)
        _validate_finite_values(self, ("torque_command_nm",))


@dataclass(frozen=True, slots=True)
class PlantInputTrace:
    """仿真 Plant 输入追踪值，禁止作为 Observer 输入。"""

    schema_version: str
    timestamp_s: float
    motor_torque_applied_nm: float
    saturation_active: bool
    actuator_limit_nm: float

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        _validate_timestamp(self.timestamp_s)
        _validate_finite_values(self, ("motor_torque_applied_nm", "actuator_limit_nm"))
        if self.actuator_limit_nm <= 0:
            raise ValueError("actuator_limit_nm must be positive")


@dataclass(frozen=True, slots=True)
class RawMotorMeasurement:
    schema_version: str
    timestamp_s: float
    motor_position_rad: float
    motor_velocity_rad_s: float
    motor_current_a: float
    encoder_valid: bool
    current_valid: bool
    timestamp_valid: bool

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        _validate_timestamp(self.timestamp_s)
        _validate_finite_values(
            self, ("motor_position_rad", "motor_velocity_rad_s", "motor_current_a")
        )


@dataclass(frozen=True, slots=True)
class TorqueFeedback:
    schema_version: str
    timestamp_s: float
    motor_torque_feedback_nm: float
    torque_source: TorqueSource
    torque_valid: bool
    torque_std_nm: float

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        _validate_timestamp(self.timestamp_s)
        _validate_finite_values(self, ("motor_torque_feedback_nm", "torque_std_nm"))
        if self.torque_std_nm < 0:
            raise ValueError("torque_std_nm must be non-negative")


@dataclass(frozen=True, slots=True)
class SignalHealthStatus:
    schema_version: str
    timestamp_s: float
    encoder_valid: bool
    current_valid: bool
    timestamp_valid: bool
    torque_valid: bool
    data_stale: bool
    saturation_active: bool
    reason_codes: tuple[ReasonCode, ...]

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        _validate_timestamp(self.timestamp_s)
        _validate_reason_codes(self.reason_codes)


@dataclass(frozen=True, slots=True)
class ObserverInput:
    """Observer 唯一合法输入，不含命令、applied torque 或 Plant 真值。"""

    schema_version: str
    timestamp_s: float
    motor_position_rad: float
    motor_velocity_rad_s: float
    motor_torque_feedback_nm: float
    encoder_valid: bool
    current_valid: bool
    timestamp_valid: bool
    torque_valid: bool
    torque_std_nm: float

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        _validate_timestamp(self.timestamp_s)
        _validate_finite_values(
            self,
            (
                "motor_position_rad",
                "motor_velocity_rad_s",
                "motor_torque_feedback_nm",
                "torque_std_nm",
            ),
        )
        if self.torque_std_nm < 0:
            raise ValueError("torque_std_nm must be non-negative")


@dataclass(frozen=True, slots=True)
class ObserverEstimate:
    schema_version: str
    timestamp_s: float
    estimated_load_position_rad: float
    estimated_load_velocity_rad_s: float
    estimated_torsion_rad: float
    estimated_external_torque_nm: float
    normalized_innovation_squared: float
    estimate_finite: bool
    observer_diverged: bool

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        _validate_timestamp(self.timestamp_s)
        names = tuple(
            field.name
            for field in fields(self)
            if field.name
            not in {"schema_version", "timestamp_s", "estimate_finite", "observer_diverged"}
        )
        _validate_finite_values(self, names)
        if self.normalized_innovation_squared < 0:
            raise ValueError("normalized_innovation_squared must be non-negative")


@dataclass(frozen=True, slots=True)
class ConfidenceOutput:
    schema_version: str
    timestamp_s: float
    confidence_score: float
    valid_flag: bool
    confidence_state: ConfidenceState
    reason_codes: tuple[ReasonCode, ...]

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        _validate_timestamp(self.timestamp_s)
        if not isfinite(self.confidence_score) or not 0 <= self.confidence_score <= 1:
            raise ValueError("confidence_score must be within [0, 1]")
        _validate_reason_codes(self.reason_codes)
        if self.confidence_state is ConfidenceState.HARD_INVALID and self.valid_flag:
            raise ValueError("HARD_INVALID requires valid_flag=false")
        if self.confidence_state is not ConfidenceState.HARD_INVALID and not self.valid_flag:
            raise ValueError("only HARD_INVALID may set valid_flag=false")


@dataclass(frozen=True, slots=True)
class ClassificationOutput:
    schema_version: str
    timestamp_s: float
    classification_state: ClassificationState
    contact_score: float
    valid_flag: bool

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        _validate_timestamp(self.timestamp_s)
        if not isfinite(self.contact_score) or not 0 <= self.contact_score <= 1:
            raise ValueError("contact_score must be within [0, 1]")


@dataclass(frozen=True, slots=True)
class ModeDecision:
    schema_version: str
    timestamp_s: float
    operation_mode: OperationMode
    contact_hazard_latched: bool
    safety_action_required: bool
    safety_action_level: SafetyActionLevel
    reason_codes: tuple[ReasonCode, ...]

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        _validate_timestamp(self.timestamp_s)
        _validate_reason_codes(self.reason_codes)
        if self.contact_hazard_latched and self.safety_action_level in {
            SafetyActionLevel.NONE,
            SafetyActionLevel.LIMITED,
        }:
            raise ValueError("latched contact hazard requires SLOWDOWN or STOP_REQUEST")
        if (
            self.contact_hazard_latched
            and ReasonCode.CONTACT_HAZARD_LATCHED not in self.reason_codes
        ):
            raise ValueError("latched contact hazard requires CONTACT_HAZARD_LATCHED")
        action_is_required = self.safety_action_level is not SafetyActionLevel.NONE
        if self.safety_action_required != action_is_required:
            raise ValueError("safety_action_required must match safety_action_level")


@dataclass(frozen=True, slots=True)
class SystemStateSnapshot:
    schema_version: str
    timestamp_s: float
    observer_estimate: ObserverEstimate
    confidence_output: ConfidenceOutput
    classification_output: ClassificationOutput
    mode_decision: ModeDecision

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        _validate_timestamp(self.timestamp_s)
        timestamps = {
            self.observer_estimate.timestamp_s,
            self.confidence_output.timestamp_s,
            self.classification_output.timestamp_s,
            self.mode_decision.timestamp_s,
            self.timestamp_s,
        }
        if len(timestamps) != 1:
            raise ValueError("snapshot members must share the same timestamp")


@dataclass(frozen=True, slots=True)
class ControlCommand:
    schema_version: str
    timestamp_s: float
    requested_torque_nm: float
    limited_torque_nm: float
    safety_action_level: SafetyActionLevel
    operation_mode: OperationMode
    valid_until_s: float
    reason_codes: tuple[ReasonCode, ...]

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        _validate_timestamp(self.timestamp_s)
        _validate_finite_values(
            self, ("requested_torque_nm", "limited_torque_nm", "valid_until_s")
        )
        if self.valid_until_s < self.timestamp_s:
            raise ValueError("valid_until_s cannot precede timestamp_s")
        _validate_reason_codes(self.reason_codes)


@dataclass(frozen=True, slots=True)
class ImmutablePlantTrueConfig:
    schema_version: str
    configuration_id: str
    motor_inertia_kg_m2: float
    load_inertia_kg_m2: float
    shaft_stiffness_nm_rad: float
    shaft_damping_nms_rad: float
    gear_ratio: float
    actuator_limit_nm: float

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        _validate_nonempty_text(self.configuration_id, "configuration_id")
        positive_fields = tuple(
            field.name
            for field in fields(self)
            if field.name not in {"schema_version", "configuration_id", "shaft_damping_nms_rad"}
        )
        _validate_finite_values(self, positive_fields + ("shaft_damping_nms_rad",))
        if any(getattr(self, name) <= 0 for name in positive_fields):
            raise ValueError("inertias, stiffness, gear ratio and actuator limit must be positive")
        if self.shaft_damping_nms_rad < 0:
            raise ValueError("shaft_damping_nms_rad must be non-negative")


@dataclass(frozen=True, slots=True)
class NominalParameterVersion:
    schema_version: str
    parameter_version: str
    base_parameter_version: str | None
    parameter_values: dict[str, float]
    created_reason: str
    checksum_sha256: str

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        _validate_nonempty_text(self.parameter_version, "parameter_version")
        if self.base_parameter_version is not None:
            _validate_nonempty_text(self.base_parameter_version, "base_parameter_version")
        _validate_parameter_values(self.parameter_values)
        _validate_nonempty_text(self.created_reason, "created_reason")
        _validate_checksum(self.checksum_sha256)


@dataclass(frozen=True, slots=True)
class CalibrationCandidate:
    schema_version: str
    candidate_id: str
    base_parameter_version: str
    candidate_parameter_version: str
    parameter_values: dict[str, float]
    generation_reason: str
    acceptance_window_id: str

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        for name in (
            "candidate_id",
            "base_parameter_version",
            "candidate_parameter_version",
            "generation_reason",
            "acceptance_window_id",
        ):
            _validate_nonempty_text(getattr(self, name), name)
        _validate_parameter_values(self.parameter_values)
        if self.base_parameter_version == self.candidate_parameter_version:
            raise ValueError("candidate version must differ from base version")


@dataclass(frozen=True, slots=True)
class CalibrationDecision:
    schema_version: str
    candidate_id: str
    decision: CalibrationDecisionType
    decision_reason_codes: tuple[ReasonCode, ...]
    rollback_target_version: str | None

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        _validate_nonempty_text(self.candidate_id, "candidate_id")
        _validate_reason_codes(self.decision_reason_codes)
        if self.decision is CalibrationDecisionType.ROLLBACK:
            if self.rollback_target_version is None:
                raise ValueError("ROLLBACK requires rollback_target_version")
            _validate_nonempty_text(self.rollback_target_version, "rollback_target_version")
        elif self.rollback_target_version is not None:
            raise ValueError("only ROLLBACK may set rollback_target_version")


@dataclass(frozen=True, slots=True)
class ArtifactIndexEntry:
    schema_version: str
    artifact_id: str
    artifact_type: str
    uri: str
    checksum_sha256: str
    size_bytes: int
    owner: str
    available: bool

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        for name in ("artifact_id", "artifact_type", "uri", "owner"):
            _validate_nonempty_text(getattr(self, name), name)
        _validate_checksum(self.checksum_sha256)
        if self.size_bytes < 0:
            raise ValueError("size_bytes must be non-negative")


@dataclass(frozen=True, slots=True)
class P1ValidationResult:
    payload_level: str
    p1_viability_decision: VerificationDecision
    p1_advantage_decision: VerificationDecision
    load_position_rmse_rad: float
    load_velocity_rmse_rad_s: float
    load_position_max_abs_error_rad: float
    load_velocity_max_abs_error_rad_s: float
    baseline_load_position_rmse_rad: float
    baseline_load_velocity_rmse_rad_s: float
    position_improvement_median_pct: float
    velocity_improvement_median_pct: float
    position_improvement_iqr_pct: float
    velocity_improvement_iqr_pct: float
    position_winning_seed_count: int
    velocity_winning_seed_count: int
    evaluated_seed_count: int
    estimate_finite: bool
    observer_diverged: bool
    external_torque_rmse_nm: float | None = None

    def __post_init__(self) -> None:
        if self.payload_level not in {"light", "medium", "heavy"}:
            raise ValueError("payload_level is invalid")
        nonnegative = (
            "load_position_rmse_rad",
            "load_velocity_rmse_rad_s",
            "load_position_max_abs_error_rad",
            "load_velocity_max_abs_error_rad_s",
            "baseline_load_position_rmse_rad",
            "baseline_load_velocity_rmse_rad_s",
            "position_improvement_iqr_pct",
            "velocity_improvement_iqr_pct",
        )
        _validate_finite_values(
            self,
            nonnegative
            + ("position_improvement_median_pct", "velocity_improvement_median_pct"),
        )
        if any(getattr(self, name) < 0 for name in nonnegative):
            raise ValueError("P1 error and IQR fields must be non-negative")
        if self.evaluated_seed_count < 1:
            raise ValueError("evaluated_seed_count must be positive")
        if not 0 <= self.position_winning_seed_count <= self.evaluated_seed_count:
            raise ValueError("position_winning_seed_count is invalid")
        if not 0 <= self.velocity_winning_seed_count <= self.evaluated_seed_count:
            raise ValueError("velocity_winning_seed_count is invalid")
        if self.external_torque_rmse_nm is not None:
            if not isfinite(self.external_torque_rmse_nm) or self.external_torque_rmse_nm < 0:
                raise ValueError("external_torque_rmse_nm must be non-negative")


@dataclass(frozen=True, slots=True)
class P2ValidationResult:
    p2_vibration_decision: VerificationDecision
    p2_contact_decision: VerificationDecision
    false_alarm_count: int
    missed_detection_count: int
    detection_delay_s: float | None = None
    vibration_velocity_rms_rad_s: float | None = None
    external_torque_rmse_nm: float | None = None

    def __post_init__(self) -> None:
        if self.false_alarm_count < 0 or self.missed_detection_count < 0:
            raise ValueError("P2 event counts must be non-negative")
        for name in ("detection_delay_s", "vibration_velocity_rms_rad_s", "external_torque_rmse_nm"):
            value = getattr(self, name)
            if value is not None and (not isfinite(value) or value < 0):
                raise ValueError(f"{name} must be non-negative")


@dataclass(frozen=True, slots=True)
class P3ValidationResult:
    p3_degrade_decision: VerificationDecision
    p3_action_decision: VerificationDecision
    p3_recovery_decision: VerificationDecision
    confidence_drop: float
    safety_action_level: SafetyActionLevel
    false_degrade_count: int
    missed_degrade_count: int
    recovery_time_s: float | None = None

    def __post_init__(self) -> None:
        if not isfinite(self.confidence_drop) or not 0 <= self.confidence_drop <= 1:
            raise ValueError("confidence_drop must be within [0, 1]")
        if self.false_degrade_count < 0 or self.missed_degrade_count < 0:
            raise ValueError("P3 event counts must be non-negative")
        if self.recovery_time_s is not None and (
            not isfinite(self.recovery_time_s) or self.recovery_time_s < 0
        ):
            raise ValueError("recovery_time_s must be non-negative")


@dataclass(frozen=True, slots=True)
class SilValidationResult:
    numerical_consistency_max_error: float
    step_runtime_ms_p95: float
    memory_bytes_peak: int
    exception_protection_passed: bool

    def __post_init__(self) -> None:
        _validate_finite_values(self, ("numerical_consistency_max_error", "step_runtime_ms_p95"))
        if self.numerical_consistency_max_error < 0 or self.step_runtime_ms_p95 < 0:
            raise ValueError("SIL error and runtime must be non-negative")
        if self.memory_bytes_peak < 0:
            raise ValueError("memory_bytes_peak must be non-negative")


@dataclass(frozen=True, slots=True)
class IntegrationValidationResult:
    contract_replay_passed: bool
    component_versions: dict[str, str]
    contract_violation_count: int

    def __post_init__(self) -> None:
        if not self.component_versions or any(
            not name.strip() or not version.strip()
            for name, version in self.component_versions.items()
        ):
            raise ValueError("component_versions must be non-empty")
        if self.contract_violation_count < 0:
            raise ValueError("contract_violation_count must be non-negative")


ValidationResult: TypeAlias = (
    P1ValidationResult
    | P2ValidationResult
    | P3ValidationResult
    | SilValidationResult
    | IntegrationValidationResult
)


@dataclass(frozen=True, slots=True)
class ValidationReport:
    schema_version: str
    report_id: str
    experiment_id: str
    stage: ValidationStage
    git_commit: str
    algorithm_version: str
    configuration_id: str
    scenario_id: str
    random_seed: int
    software_environment: dict[str, str]
    decision: VerificationDecision
    valid_flag: bool
    failure_reason_codes: tuple[str, ...]
    artifact_index: tuple[ArtifactIndexEntry, ...]
    runtime_ms: float
    result: ValidationResult

    def __post_init__(self) -> None:
        _validate_version(self.schema_version)
        for name in (
            "report_id",
            "experiment_id",
            "git_commit",
            "algorithm_version",
            "configuration_id",
            "scenario_id",
        ):
            _validate_nonempty_text(getattr(self, name), name)
        if self.random_seed < 0:
            raise ValueError("random_seed must be non-negative")
        if not self.software_environment or any(
            not key.strip() or not value.strip()
            for key, value in self.software_environment.items()
        ):
            raise ValueError("software_environment must be non-empty")
        if not isfinite(self.runtime_ms) or self.runtime_ms < 0:
            raise ValueError("runtime_ms must be non-negative")
        expected_type = {
            ValidationStage.P1: P1ValidationResult,
            ValidationStage.P2: P2ValidationResult,
            ValidationStage.P3: P3ValidationResult,
            ValidationStage.SIL: SilValidationResult,
            ValidationStage.INTEGRATION: IntegrationValidationResult,
        }[self.stage]
        if not isinstance(self.result, expected_type):
            raise ValueError("result type must match validation stage")
