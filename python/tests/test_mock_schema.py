import json
from pathlib import Path

from jsonschema import Draft202012Validator

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MOCK_DIRECTORY = REPOSITORY_ROOT / "configs" / "mock"


def test_mock_metadata_and_payload_schema() -> None:
    fixtures = sorted(MOCK_DIRECTORY.glob("*.json"))

    assert fixtures
    for fixture_path in fixtures:
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        schema = json.loads(
            (REPOSITORY_ROOT / fixture["schema_path"]).read_text(encoding="utf-8")
        )

        assert fixture["fixture_type"] == "MOCK"
        assert fixture["data_source"] == "MOCK"
        assert fixture["valid_for_algorithm_evaluation"] is False
        assert not list(
            Draft202012Validator(schema).iter_errors(fixture["payload"])
        ), fixture_path


def test_required_system_state_mock_cases_exist() -> None:
    expected = {
        "system_state_normal.json",
        "system_state_vibration.json",
        "system_state_contact.json",
        "system_state_low_confidence.json",
        "validation_report_example.json",
    }

    assert expected.issubset({path.name for path in MOCK_DIRECTORY.glob("*.json")})
