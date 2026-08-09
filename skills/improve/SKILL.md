---
name: improve
description: "[Lite-3 Improve] Review and refactor the current changes: default 3-agent diff review, --deep round-based review, --security audit, --refactor tiny-commit plan. Use before merging, for a hard security pass, or to plan paying down tech debt."
origin: robobuilder-lite
upstream: https://github.com/Robo-Co-op/robobuilder-standard
merged-from: diff-review, cross-review, grill, cso, improve-codebase-architecture, request-refactor-plan
allowed-tools: [Read, Glob, Grep, Bash, Agent]
---

# Improve

## What

The review-and-refactor command. One default mode plus three flags cover the whole
"make it better before it lands" surface:

- **default** — daily diff review (3 subagents in parallel → one prioritized verdict)
- **`--deep`** — round-based review that iterates until findings hit zero
- **`--security`** — a focused security audit
- **`--refactor`** — an architecture pass that produces a tiny-commit refactor plan

This is the Lite bundle of `diff-review`, `cross-review`, `grill`, `cso`,
`improve-codebase-architecture`, and `request-refactor-plan` from Standard.

## When

Use `/robobuilder-lite:improve` when:
- You're about to merge and want a review → default
- It's an important merge (auth, payments, data model) → `--deep`
- You want a dedicated security pass → `--security`
- Tech debt is slowing you down and you want a safe plan to pay it → `--refactor`

## Why

Self-review misses what you were too close to see. Running independent perspectives
in parallel — simplification, tests, security — surfaces more in one pass than any
single reviewer, and the adversarial mindset (assume it's broken, prove it) catches
the failures that a "looks good to me" read never will.

## How

### Default — daily diff review

1. Get an overview: `git diff main...HEAD --stat` then `git diff main...HEAD`.
2. Invoke **3 subagents in parallel** (multiple Agent calls in one message):
   - `code-simplifier` — redundancy, over-abstraction, naming
   - `test-writer` — missing test coverage
   - `security-auditor` — OWASP perspective
3. Apply the **grill mindset** yourself while merging their output: enumerate the
   code's implicit assumptions (environment, inputs, state) and 5+ failure modes
   (concurrency, network failure, partial failure, retries, null/undefined, empty
   collections, exceeding limits). No flattery — if you want to say "mostly fine,"
   dig one level deeper.
4. Merge into one prioritized verdict:

```
## Merged verdict
### Must fix (before merge)
### Should fix (recommended in this PR)
### Nice to have (can defer)
## One-liner: SHIP / FIX FIRST
```

### `--deep` — round-based review (before important merges)

The heavyweight version: **keep running rounds until there are zero findings.**

- Round 0: `git diff main...HEAD --stat`, confirm the affected files and scale.
- Rounds 1–N: invoke `code-simplifier`, `test-writer`, `security-auditor`, and (for
  UI changes) `e2e-tester` in parallel. Fix **Critical** and **Medium** findings
  immediately, then start the next round. Record **Minor** findings.
- Exit when 0 critical AND 0 medium for **2 consecutive rounds**, or once a round
  stops surfacing anything **new**. Five rounds is the usual place that happens, but
  it's a prompt to check rather than a hard stop — divergence is rounds repeating
  themselves, not rounds accumulating.
- Report: total rounds, total findings (Critical/Medium/Minor), final verdict, and
  learnings (failure patterns that repeated — apply them next time).

Don't treat round or finding counts as KPIs — fewer is better. If **the same finding**
persists for 3+ rounds, suspect a reviewer-side false positive — but that is different
from **the same area** yielding a *new* real defect each round, which means the area is
hard and wants more attention, not less. Read the findings side by side before
dismissing any of them. This mode is
expensive; use it only before important merges.

### `--security` — security audit

A focused pass distilled from the CSO skill:

1. **Secrets** — scan the diff and repo for hardcoded keys, tokens, passwords,
   connection strings. Confirm none are committed and none are logged.
2. **Dependencies / supply chain** — new or changed dependencies, lockfile
   integrity, install scripts, unpinned refs.
3. **OWASP Top 10 essentials** — injection, broken access control, auth/session
   handling, SSRF, insecure deserialization, security misconfiguration.
4. **Verdict with confidence gating** — only report a finding you can point to
   concrete code for (file + line + why). Don't pad the report with speculation.

### `--refactor` — architecture pass + tiny-commit plan

1. **Find deepening opportunities** — where a shallow module (thin logic, wide
   interface, changes often) could become a deep one (lots of functionality behind
   a small, stable, testable interface). Note friction points as you explore.
2. **Interview** the user on the target: the problem, options they've considered,
   exact scope (what changes and what explicitly does not). Check test coverage of
   the area first; if it's thin, agree a testing plan before touching code.
3. **Produce a tiny-commit plan** — break the work into the smallest commits
   possible, each leaving the codebase working (Fowler). Write commits in plain
   English, no file paths.
4. **File it as a GitHub issue** with: Problem, Solution, Commits (plain English),
   Decision Document, Testing Decisions, Out of Scope.

## Example

> **User:** improve   *(before merging the saved-search PR)*
>
> **improve (default):** 3 agents in parallel. `security-auditor`: the search
> query is interpolated into SQL — injection risk [Critical]. `test-writer`: no
> test for empty-filter replay. `code-simplifier`: `SavedSearch#replay` duplicates
> `SearchBar#apply`.
> Merged verdict — **Must fix:** parameterize the query. **Should fix:** empty-filter
> test. **Nice to have:** extract shared apply logic. **One-liner: FIX FIRST.**

## Anti-pattern

- **Sequential agents.** Run the three reviewers in parallel (one message, multiple
  Agent calls), not one after another.
- **Flattery review.** "Looks great, ship it." If you didn't try to break it, you
  didn't review it.
- **Reporting unverifiable findings in `--security`.** A finding you can't point to
  concrete code for is noise — gate on confidence.
- **A refactor "big bang" commit.** Each commit must leave the codebase working.
  If it doesn't, the step is too big.

## See Also

- `/robobuilder-lite:plan` — decide what to build
- `/robobuilder-lite:build` — implement it with TDD
- `/robobuilder-lite:ship` — package and land the reviewed change
- For the unbundled originals (`diff-review`, `cross-review`, `grill`, `cso`,
  `improve-codebase-architecture`, `request-refactor-plan`), see **Robo Builder
  Standard**.
