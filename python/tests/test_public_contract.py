from dataclasses import fields

from flexsense_guard import (
    ActuatorCommand,
    ArtifactIndexEntry,
    CalibrationCandidate,
    CalibrationDecision,
    ClassificationOutput,
    ConfidenceOutput,
    ControlCommand,
    ImmutablePlantTrueConfig,
    IntegrationValidationResult,
    ModeDecision,
    NominalParameterVersion,
    ObserverEstimate,
    ObserverInput,
    P1ValidationResult,
    P2ValidationResult,
    P3ValidationResult,
    PlantInputTrace,
    RawMotorMeasurement,
    SignalHealthStatus,
    SilValidationResult,
    SystemStateSnapshot,
    TorqueFeedback,
)


DTO_SCHEMAS = {
    ActuatorCommand: "actuator_command.schema.json",
    PlantInputTrace: "plant_input_trace.schema.json",
    RawMotorMeasurement: "raw_motor_measurement.schema.json",
    TorqueFeedback: "torque_feedback.schema.json",
    SignalHealthStatus: "signal_health_status.schema.json",
    ObserverInput: "observer_input.schema.json",
    ObserverEstimate: "observer_estimate.schema.json",
    ConfidenceOutput: "confidence_output.schema.json",
    ClassificationOutput: "classification_output.schema.json",
    ModeDecision: "mode_decision.schema.json",
    SystemStateSnapshot: "system_state_snapshot.schema.json",
    ControlCommand: "control_command.schema.json",
    ImmutablePlantTrueConfig: "immutable_plant_true_config.schema.json",
    NominalParameterVersion: "nominal_parameter_version.schema.json",
    CalibrationCandidate: "calibration_candidate.schema.json",
    CalibrationDecision: "calibration_decision.schema.json",
    ArtifactIndexEntry: "artifact_index_entry.schema.json",
    P1ValidationResult: "p1_validation_result.schema.json",
    P2ValidationResult: "p2_validation_result.schema.json",
    P3ValidationResult: "p3_validation_result.schema.json",
    SilValidationResult: "sil_validation_result.schema.json",
    IntegrationValidationResult: "integration_validation_result.schema.json",
}


def test_python_dataclass_fields_match_json_schemas(
    schema_documents: dict[str, dict[str, object]],
) -> None:
    for dto, schema_name in DTO_SCHEMAS.items():
        python_fields = {field.name for field in fields(dto)}
        schema_fields = set(schema_documents[schema_name]["properties"])

        assert python_fields == schema_fields, schema_name


def test_validation_report_fields_match_envelope_plus_result(
    schema_documents: dict[str, dict[str, object]],
) -> None:
    from flexsense_guard import ValidationReport

    python_fields = {field.name for field in fields(ValidationReport)}
    envelope_fields = set(
        schema_documents["validation_report_envelope.schema.json"]["properties"]
    )

    assert python_fields == envelope_fields | {"result"}
