from collections.abc import Callable

from jsonschema import Draft202012Validator


def test_all_schemas_pass_draft_2020_12_meta_schema(
    schema_documents: dict[str, dict[str, object]],
) -> None:
    for schema in schema_documents.values():
        Draft202012Validator.check_schema(schema)


def test_hard_invalid_confidence_requires_invalid_flag(
    validator_for: Callable[[str], Draft202012Validator],
) -> None:
    confidence = {
        "schema_version": "2.0.0",
        "timestamp_s": 1.0,
        "confidence_score": 0.1,
        "valid_flag": True,
        "confidence_state": "HARD_INVALID",
        "reason_codes": ["ENCODER_INVALID"],
    }

    assert list(
        validator_for("confidence_output.schema.json").iter_errors(confidence)
    )


def test_latched_hazard_rejects_weak_safety_action(
    validator_for: Callable[[str], Draft202012Validator],
) -> None:
    decision = {
        "schema_version": "2.0.0",
        "timestamp_s": 1.0,
        "operation_mode": "LOW_CONFIDENCE_DEGRADED",
        "contact_hazard_latched": True,
        "safety_action_required": True,
        "safety_action_level": "LIMITED",
        "reason_codes": ["CONTACT_HAZARD_LATCHED"],
    }

    assert list(validator_for("mode_decision.schema.json").iter_errors(decision))
