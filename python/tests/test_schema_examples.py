import json
from pathlib import Path

from jsonschema import Draft202012Validator

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MOCK_DIRECTORY = REPOSITORY_ROOT / "configs" / "mock"


def test_all_mock_payloads_match_declared_schema() -> None:
    fixtures = sorted(MOCK_DIRECTORY.glob("*.json"))

    assert fixtures
    for fixture_path in fixtures:
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        schema_path = REPOSITORY_ROOT / fixture["schema_path"]
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        assert fixture["fixture_type"] == "MOCK"
        assert "不是" in fixture["purpose"] or "不代表" in fixture["purpose"]
        assert not list(
            Draft202012Validator(schema).iter_errors(fixture["payload"])
        ), fixture_path
