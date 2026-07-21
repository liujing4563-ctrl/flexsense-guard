from dataclasses import fields

from flexsense_guard import (
    ClassificationOutput,
    ConfidenceOutput,
    ControlCommand,
    ModeDecision,
    ObserverEstimate,
    ObserverInput,
)


FORBIDDEN_RUNTIME_FIELDS = {
    "motor_torque_measured_nm",
    "motor_torque_nm",
    "true_load_position_rad",
    "true_load_velocity_rad_s",
    "true_external_torque_nm",
    "contact_probability",
    "force_n",
}


def test_forbidden_public_fields_are_absent_from_all_schemas(
    schema_documents: dict[str, dict[str, object]],
) -> None:
    serialized = repr(schema_documents)

    for field_name in FORBIDDEN_RUNTIME_FIELDS:
        assert field_name not in serialized


def test_observer_input_excludes_command_applied_truth_and_parameters() -> None:
    observer_fields = {field.name for field in fields(ObserverInput)}
    forbidden = FORBIDDEN_RUNTIME_FIELDS | {
        "torque_command_nm",
        "motor_torque_applied_nm",
        "motor_inertia_kg_m2",
        "load_inertia_kg_m2",
        "shaft_stiffness_nm_rad",
        "shaft_damping_nms_rad",
        "gear_ratio",
    }

    assert observer_fields.isdisjoint(forbidden)
    assert "motor_torque_feedback_nm" in observer_fields
    assert "torque_std_nm" in observer_fields


def test_runtime_outputs_exclude_plant_truth() -> None:
    for dto in (
        ObserverEstimate,
        ConfidenceOutput,
        ClassificationOutput,
        ModeDecision,
        ControlCommand,
    ):
        assert {field.name for field in fields(dto)}.isdisjoint(
            FORBIDDEN_RUNTIME_FIELDS | {"motor_torque_applied_nm"}
        )
