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


def test_merged_from_matches_readme_table() -> None:
    """Each skill's `merged-from` provenance must match README's command table.

    The table is the surface a user reads to decide which command to reach for,
    so a bundle that moves in the frontmatter but not the table sends people to
    the wrong command. This drift shipped repeatedly in the sibling Pro repo
    before it was guarded.
    """
    readme = (SKILLS_DIR.parent / "README.md").read_text(encoding="utf-8")
    for skill in ("plan", "build", "improve", "ship"):
        fm = _frontmatter((SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8"))
        m = re.search(r"merged-from:\s*(.+)", fm)
        assert m, f"{skill}: missing merged-from"
        declared = [x.strip() for x in m.group(1).split(",")]
        row = re.search(
            rf"\|\s*`/robobuilder-lite:{skill}`.*?\|.*?\|\s*(.+?)\s*\|", readme
        )
        assert row, f"README has no command-table row for {skill}"
        listed = [x.strip() for x in row.group(1).split(",")]
        assert declared == listed, (
            f"{skill}: merged-from {declared} but README's table says {listed}"
        )


# --- Scoring rubrics: the absent-measurement bug class -----------------------
#
# `plan --health` inherited a composite formula from Standard that could not
# reach 10: the five weights sum to 0.90, so dividing by the raw total capped
# a clean repo at 9.0, and "a SKIPPED tool redistributes its weight" never
# said what it redistributes into. One dataset produced three different
# composites depending on how a reader resolved that.
#
# It was found by running the skill, not by reading it, and it was one of four
# defects of the same shape across the three repos: a measurement that never
# happened counted as a pass. So this guards the class. Any skill that
# aggregates per-item measurements must state both:
#
#   1. what it divides by  — an unstated denominator is where 0.90-vs-1.0 hid
#   2. what happens to an item with no measurement — it must drop out, not
#      score 0 (penalises absent tooling) and not score 10 (inflates)
#
# The registry is closed on purpose: a new scoring skill fails until someone
# adds it, which is the point at which they have to answer both.

SCORING_SIGNATURE = re.compile(r"(composite|Σ\(|quality[_ ]score|overall score)", re.IGNORECASE)

STATES_DENOMINATOR = re.compile(
    # Deliberately narrow: it must name a division, not merely describe which
    # inputs counted. "the categories that actually ran" states the skip rule,
    # not the denominator, and letting it satisfy both is how a falsification
    # run found this test passing a rubric whose divisor had been removed.
    r"(÷|divid(?:e|ed|ing) by|number of \w+ scored|\bN of M\b)",
    re.IGNORECASE,
)

STATES_MISSING_INPUT_RULE = re.compile(
    r"(\bn/a\b|SKIPPED|drops? out|did not run|never ran)", re.IGNORECASE
)

SCORING_SKILLS = {"plan"}


def test_scoring_skill_registry_matches_disk() -> None:
    """A skill that aggregates scores must be registered, and vice versa."""
    on_disk = {
        p.parent.name
        for p in _skill_files()
        if SCORING_SIGNATURE.search(p.read_text(encoding="utf-8"))
    }
    unregistered = on_disk - SCORING_SKILLS
    assert not unregistered, (
        f"these skills aggregate scores but are not in SCORING_SKILLS: {sorted(unregistered)}. "
        "Add them, and make sure each states its denominator and its skip rule."
    )
    stale = SCORING_SKILLS - on_disk
    assert not stale, f"SCORING_SKILLS lists skills that no longer score: {sorted(stale)}"


@pytest.mark.parametrize("skill", sorted(SCORING_SKILLS))
def test_scoring_skill_states_its_denominator(skill: str) -> None:
    text = (SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8")
    assert STATES_DENOMINATOR.search(text), (
        f"{skill} produces a composite but never says what it divides by. "
        "An unstated denominator is how weights summing to 0.90 went unnoticed."
    )


@pytest.mark.parametrize("skill", sorted(SCORING_SKILLS))
def test_scoring_skill_states_its_missing_input_rule(skill: str) -> None:
    text = (SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8")
    assert STATES_MISSING_INPUT_RULE.search(text), (
        f"{skill} produces a composite but never says what happens to a tool that "
        "did not run. A SKIPPED tool must drop out, not score 0 or 10."
    )


def test_plugin_json_version_matches_changelog_latest() -> None:
    """A behavior change shipped under an unchanged version is invisible.

    This repo did exactly that: `plan` grew from 105 to 240 lines and `health`
    moved out of `build`, while plugin.json stayed at 1.0.0 with no CHANGELOG
    entry. Pro has carried this guard for a while and was the only one of the
    three repos whose version was right, which is the whole argument for it.
    """
    import json

    root = SKILLS_DIR.parent
    manifest = json.loads((root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    m = re.search(r"^##\s*\[(\d+\.\d+\.\d+)\]", changelog, re.MULTILINE)
    assert m, "could not find a version heading in CHANGELOG.md"
    assert manifest["version"] == m.group(1), (
        f"plugin.json version {manifest['version']!r} does not match "
        f"CHANGELOG's latest entry {m.group(1)!r}"
    )
