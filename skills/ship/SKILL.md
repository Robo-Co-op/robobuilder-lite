---
name: ship
description: "[Lite-4 Ship] One flow from green tests to deployed: pre-flight, package (version/CHANGELOG/commit/PR), land (merge, wait for CI), verify (deploy health/canary). Use when code is ready to ship, create a PR, merge, or deploy."
origin: robobuilder-lite
upstream: https://github.com/Robo-Co-op/robobuilder-standard
merged-from: ship, land-and-deploy
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob, Agent, AskUserQuestion]
---

# Ship

## What

The release command. It carries a reviewed change from green tests all the way to a
verified deploy in one flow:

1. **Pre-flight** — branch check, merge the base, run the full test suite
2. **Package** — bump the version, update CHANGELOG, commit, push, open a PR
3. **Land** — pre-merge readiness gate, merge, wait for CI until green
4. **Verify** — detect the deploy, check production health / canary

This is the Lite bundle of `ship` and `land-and-deploy` from Standard. It runs
straight through and only stops when a human decision is genuinely required.

## When

Use `/robobuilder-lite:ship` when the code is ready: "ship it", "create a PR",
"push to main", "merge and deploy". Invoke this skill rather than pushing or
creating a PR by hand — it runs the pre-flight and review gates you'd otherwise
skip.

## Why

Shipping by hand skips steps under time pressure — the untested path, the missing
CHANGELOG entry, the merge that lands before CI goes green. Ship makes the safe
sequence automatic so "ready" reliably becomes "deployed and verified," and makes
re-running safe so a hiccup halfway through doesn't force you to redo the parts that
already succeeded.

## How

### Stage 1 — Pre-flight

1. **Detect platform and base branch** from the git remote (GitHub via `gh`, or
   git-native fallback to the default branch — `main`/`master`).
2. **Abort if on the base branch** — ship from a feature branch.
3. **Merge the base first** (`git fetch` + `git merge origin/<base> --no-edit`) so
   tests run against the merged state. Stop on complex conflicts; auto-resolve
   trivial ones (the version file, CHANGELOG ordering).
4. **Run the full test suite.** If a test fails, classify it: an **in-branch**
   failure stops ship (it's yours to fix); a clearly **pre-existing** failure is
   triaged (fix now / TODO / skip), not auto-blocking. When ambiguous, treat it as
   in-branch and stop.

### Stage 2 — Package

1. **Bump the version** — auto-pick PATCH/MICRO; **ask only on a MAJOR** bump.
   Find where the version lives before assuming a `VERSION` file: check `VERSION`,
   then `.claude-plugin/plugin.json`, `package.json`, `pyproject.toml`, `Cargo.toml`,
   in that order, and take the first that exists. A repo can keep it somewhere else
   again tomorrow — detect, don't hardcode. (All three robobuilder repos keep theirs
   in `plugin.json` and have no `VERSION` file at all, so a hardcoded filename stalls
   this stage on the very repos this skill ships in.) If a repo has no version
   anywhere, say so and skip the bump rather than inventing a file.
2. **Update CHANGELOG** — auto-generate the entry from the diff.
3. **Commit** — include uncommitted changes; write a clear message (imperative,
   Japanese verb-first per house style if the repo uses it).
4. **Push** and **create the PR** with a body summarizing what shipped and the test
   result.

### Stage 3 — Land

1. **Pre-merge readiness gate** — reviews run (`/robobuilder-lite:improve`), tests
   green, docs updated. Stop if the gate fails.
2. **Merge the PR.**
3. **Wait for CI** — poll until it goes green. If CI fails, stop and surface the
   failure (this is where `--deep` review would have caught it).

### Stage 4 — Verify

1. **Detect the deploy target** (Vercel / Fly / Railway / etc. from config or CI).
2. **Wait for the deploy** to complete.
3. **Health / canary check** — hit the production URL, check for console errors,
   failed requests, and obvious performance regressions. Report the result.

### Stops only for

- On the base branch (abort)
- Unresolvable merge conflicts
- In-branch test failures
- A MAJOR version bump
- Readiness-gate failures (reviews/tests not clear)
- CI failure after merge

### Never stops for

- Uncommitted changes (always included)
- PATCH/MICRO version choice (auto-picked)
- CHANGELOG content (auto-generated)
- Commit message approval (auto-committed)

### Re-run behavior (idempotent)

Re-running ship re-runs every **verification** step (tests, readiness, CI, health)
but skips completed **actions**: if the version is already bumped, skip the bump; if
already pushed, skip the push; if the PR exists, update its body instead of creating
a new one; if already merged, skip the merge and go to verify.

**Done — consider running `/robobuilder-lite:improve --refactor` when tech debt
accumulates.**

## Example

> **User:** ship it
>
> **ship (Pre-flight):** on `feat/saved-search`. Merged `origin/main`, no conflicts.
> Tests: 47/47 pass.
> **ship (Package):** version 1.3.1 → 1.3.2 (PATCH, auto — found in `plugin.json`, no
> `VERSION` file in this repo). CHANGELOG updated.
> Committed, pushed, PR #212 opened.
> **ship (Land):** readiness gate clear (improve ran). Merged #212. CI… green.
> **ship (Verify):** Vercel deploy live. Health check: 200, no console errors. Done.

## Anti-pattern

- **Merging before CI is green.** The whole point of Stage 3 is to wait. Don't
  merge-and-hope.
- **Pushing/PR-ing by hand instead of invoking ship.** You skip the pre-flight and
  readiness gates.
- **Treating an ambiguous test failure as pre-existing.** When unsure, it's
  in-branch — stop and look.
- **A second ship run creating a duplicate PR.** Re-runs update the existing PR;
  they don't create a new one.

## See Also

- `/robobuilder-lite:plan` — decide what to build
- `/robobuilder-lite:build` — implement it
- `/robobuilder-lite:improve` — review before this skill lands it
- For the unbundled originals (`ship`, `land-and-deploy`, plus `canary` and
  `handoff`), see **Robo Builder Standard**.
