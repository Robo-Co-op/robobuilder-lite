"""Frontmatter and content checks for the robobuilder-lite mega-skills.

Mirrors the Standard repo's conventions: English-only content, a phase/order tag
at the start of each description, required origin/upstream fields, and the merged
skill set being exactly the four Lite commands.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

SKILLS_DIR = Path(__file__).resolve().parents[2] / "skills"
EXPECTED = {"plan", "build", "improve", "ship"}


def _skill_files() -> list[Path]:
    return sorted(SKILLS_DIR.glob("*/SKILL.md"))


def _frontmatter(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert m, "SKILL.md must start with a YAML frontmatter block"
    return m.group(1)


def test_exactly_four_skills() -> None:
    names = {p.parent.name for p in _skill_files()}
    assert names == EXPECTED, f"expected {EXPECTED}, got {names}"


@pytest.mark.parametrize("skill", sorted(EXPECTED))
def test_frontmatter_fields(skill: str) -> None:
    text = (SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8")
    fm = _frontmatter(text)
    assert f"name: {skill}" in fm, f"{skill}: name field must match directory"
    assert "origin: robobuilder-lite" in fm, f"{skill}: missing origin"
    assert "upstream: https://github.com/Robo-Co-op/robobuilder-standard" in fm, (
        f"{skill}: missing upstream pointer to Standard"
    )
    assert "merged-from:" in fm, f"{skill}: missing merged-from provenance"


@pytest.mark.parametrize(
    "skill,tag",
    [("plan", "[Lite-1"), ("build", "[Lite-2"), ("improve", "[Lite-3"), ("ship", "[Lite-4")],
)
def test_description_starts_with_tag(skill: str, tag: str) -> None:
    fm = _frontmatter((SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8"))
    m = re.search(r'description:\s*"?([^"\n]+)', fm)
    assert m, f"{skill}: description field not found"
    assert m.group(1).lstrip().startswith(tag), (
        f"{skill}: description must start with {tag}"
    )


@pytest.mark.parametrize("skill", sorted(EXPECTED))
def test_no_japanese_content(skill: str) -> None:
    text = (SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8")
    # CJK Unified Ideographs / Hiragana / Katakana ranges — Lite is English-only.
    assert not re.search(r"[぀-ヿ一-鿿]", text), (
        f"{skill}: Japanese characters found; Lite content must be English-only"
    )


@pytest.mark.parametrize("skill", sorted(EXPECTED))
def test_has_pedagogical_sections(skill: str) -> None:
    text = (SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8")
    for section in ("## What", "## When", "## Why", "## How", "## Anti-pattern", "## See Also"):
        assert section in text, f"{skill}: missing section {section}"
