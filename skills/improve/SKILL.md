---
name: improve
description: "[Lite-3 Improve] Review and refactor the current changes: default parallel diff review, --deep round-based review, --security audit, --refactor tiny-commit plan. Use before merging, for a hard security pass, or to plan paying down tech debt."
origin: robobuilder-lite
upstream: https://github.com/Robo-Co-op/robobuilder-standard
merged-from: diff-review, cross-review, grill, cso, improve-codebase-architecture, request-refactor-plan
allowed-tools: [Read, Glob, Grep, Bash, Agent]
---

# Improve

## What

The review-and-refactor command. One default mode plus three flags cover the whole
"make it better before it lands" surface:

- **default** — daily diff review (subagents in parallel → one prioritized verdict)
- **`--deep`** — round-based review that iterates until findings hit zero
- **`--security`** — a focused security audit
- **`--refactor`** — an architecture pass that produces a tiny-commit refactor plan

This is the Lite bundle of `diff-review`, `cross-review`, `grill`, `cso`,
`improve-codebase-architecture`, and `request-refactor-plan` from Standard.

## When

Use `/robobuilder-lite:improve` when:
- You're about to merge and want a review → default
- It's an important merge (auth, payments, data model) → `--deep`
- **The diff adds or changes a defence** — a guard, hook, validator, permission check,
  auth rule, RLS policy, rate limit, sanitiser → **`--deep`, always**. A defence is the
  one kind of code whose bugs are invisible in normal use: it looks like it works
  precisely because nothing is attacking it yet.
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
2. **Ask the diff whether this change renders.** Run it — don't decide from what the
   work felt like:

   ```sh
   git diff main...HEAD --name-only \
     | grep -qE '\.(html|css|scss|sass|less|tsx|jsx|vue|svelte|astro)$' && echo RENDERS
   ```

3. Invoke the subagents **in parallel** (multiple Agent calls in one message):
   - `code-simplifier` — redundancy, over-abstraction, naming
   - `test-writer` — missing test coverage
   - `security-auditor` — OWASP perspective
   - `e2e-tester` — **whenever step 2 printed `RENDERS`.** The other three read the
     change; this is the only one that opens it.

   The trigger is a fact about the diff rather than a call on whether the change
   "counts as UI", because that call belongs to whoever wrote it, and the honest
   answer from the person who just wrote it is nearly always "not really". A review
   that skips it still prints a verdict — about a page it never rendered.

   If it fires and cannot run — no dev server, no reachable URL, no browser — that is
   a result. Carry `UNVERIFIED: rendered behaviour not checked (<reason>)` into the
   verdict in step 7. A render check that vanishes quietly is an unmeasured thing
   counted as a pass.

   Expect some to come back with a progress note rather than a report — "now let me
   check X" — instead of findings. That is a non-answer, not a clean result. Send it
   back asking for the final report from what it already has, and say plainly that
   finding nothing is a valid outcome; otherwise you get invented findings on the
   retry. Tell each agent up front to budget its calls so it finishes.
4. **Check a finding before you act on it.** A subagent's claim about the code is
   evidence, not a verdict — open the file and confirm the behaviour it describes.
   Wrong fixes applied confidently are worse than the defect, and a finding that
   survives your own check is one you can defend. Report what you verified.
5. Apply the **grill mindset** yourself while merging their output: enumerate the
   code's implicit assumptions (environment, inputs, state) and 5+ failure modes
   (concurrency, network failure, partial failure, retries, null/undefined, empty
   collections, exceeding limits). No flattery — if you want to say "mostly fine,"
   dig one level deeper.
6. **If the diff adds or changes a defence, attack it yourself before you report.**
   Subagents review the code you wrote; they do not systematically enumerate the
   inputs you failed to imagine. Write a throwaway script that runs the defence
   against **20+ concrete bypass attempts** and prints block/pass for each. Cover at
   minimum: casing, whitespace and quoting variants, alternative spellings of the
   same tool (`python` / `python3` / `python.exe` / `py`), absolute vs relative paths,
   path traversal, command chaining (`&&`, `;`, `|`), indirection (`sh -c`, `-c`/`-m`,
   env-var expansion), copy-then-use, and **disabling the defence itself** (deleting,
   renaming or overwriting it). Then run the allow-side too — a defence that blocks
   legitimate work is a failure, not a win. Paste the block/pass table into your
   report and lock every attempt into the test suite as a regression.

   A passing test suite is not evidence here. Tests you wrote encode the paths you
   thought of, so they share the blind spot with the implementation — the suite goes
   green and the hole stays open. Only an attempt list built independently of the
   implementation tells you anything.

7. Merge into one prioritized verdict:

```
## Merged verdict
### Must fix (before merge)
### Should fix (recommended in this PR)
### Nice to have (can defer)
### Not checked
- UNVERIFIED: <what nobody measured, and why> — omit this heading only when it is empty
## One-liner: SHIP / FIX FIRST
```

`SHIP` on a diff that renders, with an `UNVERIFIED` render line still standing, is a
verdict about a page nobody opened. Say so in the one-liner.

### `--deep` — round-based review (before important merges)

The heavyweight version: **keep running rounds until there are zero findings.**

- Round 0: `git diff main...HEAD --stat`, confirm the affected files and scale, and
  settle once whether this change renders — by running the same check the default mode
  runs, not by recalling the answer:

  ```sh
  git diff main...HEAD --name-only \
    | grep -qE '\.(html|css|scss|sass|less|tsx|jsx|vue|svelte|astro)$' && echo RENDERS
  ```
- Rounds 1–N: invoke `code-simplifier`, `test-writer`, `security-auditor` in parallel,
  plus `e2e-tester` **in every round once Round 0's `RENDERS` check fired** — the same
  observable trigger as the default mode, not a fresh judgement call each round. Fix
  **Critical** and **Medium** findings immediately, then start the next round. Record
  **Minor** findings.
- An `UNVERIFIED` render line carries across every round and does not age out. It is
  not a Minor finding and rounds do not clear it: an unrun check is not a clean one,
  and exiting on "0 critical, 0 medium" while it still stands means the loop ended
  on a question nobody answered.
- Exit when 0 critical AND 0 medium for **2 consecutive rounds**, or once a round
  stops surfacing anything **new**. Five rounds is the usual place that happens, but
  it's a prompt to check rather than a hard stop — divergence is rounds repeating
  themselves, not rounds accumulating.
- **Every round that touches a defence, re-run the bypass list from step 6** — and
  extend it with anything the round's findings suggest. Fixing one bypass often opens
  another, and a defence hardened against last round's list is not hardened against
  this round's. The list only ratchets up.
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
- **Treating a green suite as proof that a defence holds.** The tests were written by
  whoever wrote the guard, so they cover the same imagined paths and miss the same
  real ones. Measured case: a hook shipped with 37 passing tests; an independently
  built list of 26 bypass attempts walked straight through 13 of them — including
  deleting the hook file itself. Attack it, then trust it.
- **Shipping a defence you never watched fail.** If you cannot name a specific input
  you tried that the guard blocked, and one it correctly let through, you have not
  tested it — you have described it.
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
