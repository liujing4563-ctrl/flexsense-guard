#!/usr/bin/env python3
"""Collect and aggregate metrics from FlexSense-Guard validation runs.

This tool reads validation output files and produces a summary report.

Usage:
    python collect_metrics.py --input-dir path/to/results --output path/to/summary.json
"""

import argparse
import json
import sys
from pathlib import Path


def collect_metrics(input_dir: Path) -> dict:
    """Collect metrics from all JSON files in the input directory.

    Args:
        input_dir: Directory containing validation result JSON files.

    Returns:
        Aggregated metrics dictionary.
    """
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    all_metrics: list[dict] = []
    for file_path in sorted(input_dir.glob("*.json")):
        with open(file_path) as f:
            data = json.load(f)
            all_metrics.append(data)

    # Aggregate (placeholder - simple count for now)
    summary = {
        "total_runs": len(all_metrics),
        "passed": sum(1 for m in all_metrics if m.get("status") == "passed"),
        "failed": sum(1 for m in all_metrics if m.get("status") == "failed"),
        "files_processed": [str(p.name) for p in sorted(input_dir.glob("*.json"))],
    }

    return summary


def main() -> int:
    """Entry point for the metrics collection tool."""
    parser = argparse.ArgumentParser(
        description="Collect and aggregate FlexSense-Guard validation metrics."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        required=True,
        help="Directory containing validation result JSON files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path to write aggregated summary JSON file.",
    )
    args = parser.parse_args()

    try:
        summary = collect_metrics(args.input_dir)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"[INFO] Summary written to {args.output}")
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
