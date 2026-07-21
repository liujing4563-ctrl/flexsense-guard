from flexsense_guard import (
    ClassificationState,
    OperationMode,
    ReasonCode,
    SafetyActionLevel,
    TorqueSource,
    VerificationDecision,
)


def _enum_values(enum_type: type) -> set[str]:
    return {item.value for item in enum_type}


def test_common_schema_enums_match_python(
    schema_documents: dict[str, dict[str, object]],
) -> None:
    definitions = schema_documents["contract_common.schema.json"]["$defs"]

    assert set(definitions["classification_state"]["enum"]) == _enum_values(
        ClassificationState
    )
    assert set(definitions["operation_mode"]["enum"]) == _enum_values(OperationMode)
    assert set(definitions["torque_source"]["enum"]) == _enum_values(TorqueSource)
    assert set(definitions["safety_action_level"]["enum"]) == _enum_values(
        SafetyActionLevel
    )
    assert set(definitions["reason_code"]["enum"]) == _enum_values(ReasonCode)
    assert set(definitions["verification_decision"]["enum"]) == _enum_values(
        VerificationDecision
    )


def test_scores_are_bounded_in_schemas(
    schema_documents: dict[str, dict[str, object]],
) -> None:
    confidence = schema_documents["confidence_output.schema.json"]["properties"]
    classification = schema_documents["classification_output.schema.json"]["properties"]

    for score in (confidence["confidence_score"], classification["contact_score"]):
        assert score["minimum"] == 0
        assert score["maximum"] == 1
