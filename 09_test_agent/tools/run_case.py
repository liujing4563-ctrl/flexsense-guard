#!/usr/bin/env python3
"""Run a single test case for the FlexSense-Guard probe.

This tool loads a scenario configuration, simulates the plant, runs the
observer, and produces output files for analysis.

Usage:
    python run_case.py --config path/to/config.json --output path/to/output.json
"""

import argparse
import json
import sys
from pathlib import Path


def run_case(config_path: Path, output_path: Path) -> dict:
    """Run a single test case.

    Args:
        config_path: Path to scenario configuration JSON.
        output_path: Path to write output results JSON.

    Returns:
        Summary dictionary with pass/fail status.
    """
    # Load configuration
    with open(config_path) as f:
        config = json.load(f)

    scenario_id = config.get("scenario_id", "unknown")
    sample_time = config.get("sample_time_s", 0.001)
    duration = config.get("duration_s", 10.0)

    print(f"[INFO] Running case: {scenario_id}")
    print(f"[INFO]  Sample time: {sample_time}s, Duration: {duration}s")

    # TODO: In future iterations, call MATLAB or C simulation here.
    # For now, generate a placeholder output.
    result = {
        "scenario_id": scenario_id,
        "schema_version": config.get("schema_version", "0.1.0"),
        "status": "completed",
        "message": "Placeholder: simulation not yet implemented in Python standalone.",
    }

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"[INFO] Results written to {output_path}")
    return result


def main() -> int:
    """Entry point for the run_case tool."""
    parser = argparse.ArgumentParser(
        description="Run a single FlexSense-Guard test case."
    )
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to scenario configuration JSON file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path to write output results JSON file.",
    )
    args = parser.parse_args()

    if not args.config.exists():
        print(f"[ERROR] Config file not found: {args.config}", file=sys.stderr)
        return 1

    try:
        result = run_case(args.config, args.output)
        print(f"[INFO] Case completed: {result['status']}")
        return 0
    except Exception as e:
        print(f"[ERROR] Case failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
