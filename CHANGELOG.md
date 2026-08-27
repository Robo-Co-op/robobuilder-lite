# Changelog

All notable changes to robobuilder-lite.

## [1.3.0] — 2026-08-27

`improve` is the whole review surface here, and it is also the review step Pro's
`dev-loop` invokes in Phase 2 of every slice it ships. Its default mode dispatched
three agents, none of which can drive a browser, and `--deep` reached for
`e2e-tester` only "(for UI changes)". So the routine answer to "does this render
correctly" was a verdict about a page nobody had opened — and because `dev-loop`
delegates here, that gap reached every autonomous loop downstream.

### Changed
- The browser check now fires on a **fact about the diff** rather than a judgement
  about it. "(for UI changes)" asked whoever wrote the change whether it counted as
  UI, which is the judgement the independent check exists to replace — the same bug
  `build` carried until `tdd-pair`'s trigger became observable in 1.1.1. Asked of the
  person who just wrote it, the answer is nearly always "not really". Both modes now
  settle it by running the diff through a grep for renderable extensions; `--deep`
  runs the check once in Round 0 and dispatches every round after.
- An unrunnable check is a reported result, not a non-event. No dev server, no
  reachable URL, no browser → `UNVERIFIED` goes into the verdict under a **Not
  checked** heading, and in `--deep` it carries across rounds rather than ageing out.
  Exiting on "0 critical, 0 medium" with an `UNVERIFIED` render line still standing
  means the loop ended on a question nobody answered.

### Fixed
- `--deep` referenced "Round 0's `RENDERS` check" before Round 0 ran one — a dangling
  reference to a step that did not exist. Round 0 now runs it.

### Added
- `scripts/tests/test_browser_verification.py` — `improve` can reach a browser, the
  trigger is observable, and an unrunnable check surfaces. A dispatch counts only when
  the agent is the subject of a list item: naming it in prose is not wiring it, a
  distinction that came from falsifying the Standard version of this guard and finding
  it still green after the real call had been deleted.

## [1.2.0] — 2026-08-17

### Changed
- `improve` now treats a diff that adds or changes a **defence** — a guard, hook,
  validator, permission check, auth rule, RLS policy, rate limit, sanitiser — as an
  automatic `--deep` case, and requires the reviewer to attack it with 20+ concrete
  bypass attempts before reporting. The attempt list has to be built independently of
  the implementation, cover the allow side as well as the block side, and end up in the
  test suite as regressions. `--deep` re-runs and extends that list every round, since
  fixing one bypass routinely opens another.

  This came out of a real session. A PreToolUse hook was written to stop an autonomous
  loop from reaching live-trading modules, shipped with 37 passing tests, and reviewed
  by three subagents. An independently built list of 26 bypass attempts then walked
  through 13 of them — `python -c` for arbitrary execution, `py` and `python.exe` as
  alternative launchers, uppercase paths, shell redirection onto protected files, and
  `rm` on the hook file itself. The tests were green because they encoded the same
  paths the implementation already handled: the suite and the code shared one blind
  spot. Two anti-patterns are named for this — treating a green suite as proof a
  defence holds, and shipping a defence you never watched fail.

## [1.1.1] — 2026-08-11

### Fixed
- Two of the six bundled agents shipped with no skill calling them. `tdd-pair` is now
  dispatched by `build` at the point where red gets skipped — the per-cycle checklist is
  self-assessment, and the agent writing the code is the agent deciding whether it wrote
  a test first, which is the one judgement it has an incentive to get wrong. The merge of
  Standard's `tdd` into `build` had dropped the only dispatch, and with it the
  maker-≠-checker safeguard
- `codebase-explorer` is now dispatched by `plan`'s Stage 1 map, which is its whole job

### Added
- Test: every agent in `agents/` must be dispatched by some skill. It strips fenced
  blocks and blockquotes first, since an agent named only in example output is not wired

## [1.1.0] — 2026-08-09

The four commands now serve existing code as well as new features. `plan` was
greenfield-only by construction, so the skills answering "what should I work on and
why" had been pushed into `build` — which is why `build` carried four bundled skills
to `plan`'s three, and why `build --health` ended its own section by telling you to
run a different command.

### Changed
- `plan` runs three stages from either starting point: **orient** (map an unfamiliar
  area, grill an open design decision — the two compose, they are not a fork),
  **write it down** (PRD, or a health dashboard), **slice** (issues, shared). Bundles
  `zoom-out` and `health` in addition to `grill-me` / `to-prd` / `to-issues`
- Stage 3 slices a PRD vertically but health findings by **blast radius** — "fix 100
  type errors" cuts through no layers
- `build` keeps `diagnose`, which its own `## Why` names as load-bearing, and loses
  `health`, which serves neither of its failure modes. `build --health` still works as
  a forwarding alias to `plan --health`
- `build`'s bug branch moved above the TDD loop, so reading top to bottom no longer
  implies you diagnose after writing tests

### Fixed
- `plan --health`'s composite could not reach 10: the five weights sum to 0.90, so
  dividing by the raw total capped a clean repo at 9.0, and the skip rule never said
  what a `SKIPPED` tool redistributes into. Now `Σ(score × weight) ÷ Σ(weight of the
  categories that ran)`
- `ship` assumed a `VERSION` file this repo does not have, so it could not ship the
  repo it lives in. Stage 2.1 now detects where the version lives
- `improve` had no answer for a subagent that returns a progress note instead of a
  report, and no step telling you to check a finding before acting on it
- `improve --deep` inherited two stopping rules from `cross-review` that this
  project's own review history disproves: a 5-round cap that would have shipped four
  real defects found in rounds 6-9, and a "same finding 3+ rounds = false positive"
  heuristic that would have dismissed six consecutive genuine findings

### Added
- Tests: `merged-from` must match README's command table, and any skill that
  aggregates per-item measurements must state what it divides by and what happens to
  an input it could not measure
- CI: the suite runs on push and pull request instead of only by hand

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
