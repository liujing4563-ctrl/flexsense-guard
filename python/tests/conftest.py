import json
from pathlib import Path
from typing import Callable

import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIRECTORY = REPOSITORY_ROOT / "common" / "schemas"


@pytest.fixture(scope="session")
def schema_documents() -> dict[str, dict[str, object]]:
    return {
        path.name: json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(SCHEMA_DIRECTORY.glob("*.schema.json"))
    }


@pytest.fixture(scope="session")
def schema_registry(
    schema_documents: dict[str, dict[str, object]],
) -> Registry:
    return Registry().with_resources(
        (
            schema["$id"],
            Resource.from_contents(schema),
        )
        for schema in schema_documents.values()
    )


@pytest.fixture
def validator_for(
    schema_documents: dict[str, dict[str, object]],
    schema_registry: Registry,
) -> Callable[[str], Draft202012Validator]:
    def build(schema_name: str) -> Draft202012Validator:
        return Draft202012Validator(
            schema_documents[schema_name],
            registry=schema_registry,
        )

    return build
