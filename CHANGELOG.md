# Changelog

All notable changes to robobuilder-lite.

## [1.0.0] — 2026-07-03

First release. The beginner edition of Robo Builder.

### Added
- Four merged mega-skills covering the full dev workflow:
  - `plan` — grill-me → to-prd → to-issues
  - `build` — triage → tdd, with diagnose and `--health` branches
  - `improve` — diff-review default, `--deep` / `--security` / `--refactor` flags
  - `ship` — ship → land-and-deploy
- The 6 lifecycle hooks and bundled hook scripts from Standard (secret-blocking,
  auto-format, notifications, memory consolidation)
- 6 review agents used by the skills (code-simplifier, test-writer,
  security-auditor, e2e-tester, tdd-pair, codebase-explorer)
- Frontmatter test suite (`scripts/tests/test_skill_frontmatter.py`): English-only
  content, `[Lite-n]` description tags, required origin/upstream fields, exactly
  four skills
- README with the three-editions table and per-command bundling map
- LICENSE with per-skill derivation attribution to Matt Pocock / Garry Tan / Jin Kim
