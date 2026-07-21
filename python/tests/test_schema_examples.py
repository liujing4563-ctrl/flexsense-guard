import json
import re
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def test_all_repository_json_files_parse() -> None:
    json_files = [
        path
        for path in REPOSITORY_ROOT.rglob("*.json")
        if ".git" not in path.parts
    ]

    assert json_files
    for path in json_files:
        json.loads(path.read_text(encoding="utf-8"))


def test_markdown_relative_links_exist() -> None:
    missing: list[str] = []
    for markdown_path in REPOSITORY_ROOT.rglob("*.md"):
        if ".git" in markdown_path.parts:
            continue
        for raw_target in MARKDOWN_LINK.findall(
            markdown_path.read_text(encoding="utf-8")
        ):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or "://" in target or target.startswith(("mailto:", "#")):
                continue
            resolved = (markdown_path.parent / target).resolve()
            if not resolved.exists():
                missing.append(f"{markdown_path.relative_to(REPOSITORY_ROOT)} -> {target}")

    assert not missing, "\n".join(missing)


def test_math_spec_keeps_gear_output_and_load_coordinates_distinct() -> None:
    architecture = (
        REPOSITORY_ROOT / "docs" / "02_architecture" / "system_architecture.md"
    ).read_text(encoding="utf-8")

    assert "theta_g = theta_m / N" in architecture
    assert "q = theta_g - theta_l" in architecture
    assert "theta_l = theta_m / N" not in architecture
