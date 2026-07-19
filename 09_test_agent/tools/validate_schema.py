#!/usr/bin/env python3
"""Validate JSON data files against FlexSense-Guard JSON schemas.

This tool validates that a JSON data file conforms to the corresponding
schema definition. It supports all three schemas defined in common/schemas/.

Usage:
    python validate_schema.py --schema scenario_config --data path/to/data.json
"""

import argparse
import json
import sys
from pathlib import Path

import jsonschema


# Schema registry
SCHEMA_DIR = Path(__file__).resolve().parent.parent.parent / "common" / "schemas"

SCHEMA_FILES: dict[str, str] = {
    "scenario_config": "scenario_config.schema.json",
    "system_state": "system_state.schema.json",
    "validation_report": "validation_report.schema.json",
}


def load_schema(schema_name: str) -> dict:
    """Load a JSON schema by name.

    Args:
        schema_name: One of 'scenario_config', 'system_state', 'validation_report'.

    Returns:
        Parsed JSON schema dictionary.

    Raises:
        ValueError: If the schema name is unknown.
        FileNotFoundError: If the schema file does not exist.
    """
    if schema_name not in SCHEMA_FILES:
        raise ValueError(
            f"Unknown schema '{schema_name}'. "
            f"Available: {list(SCHEMA_FILES.keys())}"
        )

    schema_path = SCHEMA_DIR / SCHEMA_FILES[schema_name]
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    with open(schema_path) as f:
        return json.load(f)


def validate_file(schema_name: str, data_path: Path) -> bool:
    """Validate a JSON data file against the named schema.

    Args:
        schema_name: Schema name to validate against.
        data_path: Path to the JSON data file.

    Returns:
        True if validation passes, False otherwise.
    """
    schema = load_schema(schema_name)

    with open(data_path) as f:
        data = json.load(f)

    try:
        jsonschema.validate(instance=data, schema=schema)
        print(f"[PASS] '{data_path}' conforms to '{schema_name}' schema.")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"[FAIL] '{data_path}' does NOT conform to '{schema_name}' schema:")
        print(f"       {e.message}")
        return False


def main() -> int:
    """Entry point for the schema validation tool."""
    parser = argparse.ArgumentParser(
        description="Validate JSON data against FlexSense-Guard schemas."
    )
    parser.add_argument(
        "--schema",
        type=str,
        required=True,
        choices=list(SCHEMA_FILES.keys()),
        help="Schema name to validate against.",
    )
    parser.add_argument(
        "--data",
        type=Path,
        required=True,
        help="Path to the JSON data file to validate.",
    )
    args = parser.parse_args()

    if not args.data.exists():
        print(f"[ERROR] Data file not found: {args.data}", file=sys.stderr)
        return 1

    success = validate_file(args.schema, args.data)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
