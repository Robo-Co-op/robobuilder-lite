---
name: plan
description: "[Lite-1 Plan] Get from a starting point to a set of ready-to-build issues, whether that start is a new idea or a codebase you have to work on. New feature: grill the design, write a PRD, slice it vertically. Existing code: map the area, measure its health, slice by blast radius. Both end in issues small enough to pick up one at a time. Use when starting a feature, turning an idea into a spec, picking up unfamiliar code, or deciding what to fix next."
origin: robobuilder-lite
upstream: https://github.com/Robo-Co-op/robobuilder-standard
merged-from: grill-me, to-prd, to-issues, zoom-out, health
---

# Plan

## What

One command that carries you from a starting point to a set of ready-to-build issues.
There are two starting points, and they run the same three stages:

| Stage | New feature | Existing code |
|---|---|---|
| 1. **Orient** | **Grill** — interview you until the design is decided | **Map** — the modules and callers of the area you're touching |
| 2. **Write it down** | **PRD** — the shared understanding as a doc | **Health** — a scored dashboard and ranked findings |
| 3. **Slice** | Issues | Issues |

Stage 3 is shared: both paths end in the same tracker, in the same shape, ready for
`build` to pick up.

This is the Lite bundle of five Standard skills (`grill-me`, `to-prd`, `to-issues`,
`zoom-out`, `health`). It keeps the discipline and drops the ceremony.

## When

Use `/robobuilder-lite:plan` when:
- You have an idea and want to think it through before writing code
- You have a decision to make and want to be pushed on it, not flattered
- You're about to work in code you don't know well and need the shape of it
- You want to know what's worth fixing → `/robobuilder-lite:plan --health`
- You already have a spec or PRD and just need it broken into tickets

You can enter at any stage. If you already have a written PRD, say so — plan skips
grilling and goes straight to issues.

## Why

Work goes wrong before the first line of code, and it goes wrong in two different
ways depending on where you started.

On a **new feature**, the design has an unresolved branch nobody noticed, or the work
gets sliced horizontally (all the database, then all the API, then all the UI) so
nothing is demoable until the end.

On **existing code**, the failure is quieter: you fix what you happened to notice.
Without a map you can't tell whether the module you're in is central or peripheral,
and without a measurement you're ranking by irritation instead of by cost. Both
produce busywork that feels like progress.

Plan forces the decisions out early on the first path, and forces the evidence out
early on the second. Either way you end up with issues someone can actually pick up.

## How

### Stage 1 — Orient

Route on the starting point, and say which path you took. If the user came with an
idea, grill. If they came with code — a bug, a cleanup, an unfamiliar area, or
`--health` — map first. **Never start mapping because the codebase is nearby**: a
user who came to design a feature should be grilled, not handed an architecture tour.

**New feature → Grill** *(skip if the design is already settled)*

Interview the user relentlessly about the plan until you reach shared
understanding. Walk down each branch of the design decision tree, resolving
dependencies between decisions one by one.

- Ask **one question at a time**. Wait for the answer before the next question.
- For each question, give **your recommended answer** and why.
- If a question can be answered by reading the codebase, read the codebase instead
  of asking.
- No flattery. If a choice has a real downside, say so.

**DONE when:** every branch of the decision tree has a decision, and you can state
the design back to the user in a few sentences with nothing left as "TBD".

**Existing code → Map**

Go up a layer of abstraction before touching anything. Give the user a map of the
relevant modules and their callers, in the project's own vocabulary (domain glossary
/ ubiquitous language) if it has one — plain module names if it doesn't.

You are answering "what is this area, and what depends on it", not "what's wrong with
it". Measurement is Stage 2, and a finding you can't place on this map is a finding
you can't prioritize.

**DONE when:** the user can point at the part of the map they care about.

### Stage 2 — Write it down

**New feature → PRD**

Synthesize what you now know into a PRD. Do **not** re-interview — you already have
the decisions from Stage 1. Explore the repo first if you haven't, and use the
project's own vocabulary (domain glossary / ubiquitous language) throughout.

Sketch the major **modules** you'll build or change. Prefer deep modules — a lot of
functionality behind a small, stable, testable interface. Check the module list
matches the user's expectations, and ask which modules they want tests for.

Write the PRD with these sections:

- **Problem Statement** — the problem from the user's perspective
- **Solution** — the solution from the user's perspective
- **User Stories** — a long numbered list: "As an `<actor>`, I want `<feature>`, so that `<benefit>`"
- **Implementation Decisions** — modules, interfaces, schema changes, API contracts, architectural calls. No file paths or code (they go stale). Exception: a decision-encoding snippet from a prototype (schema, state machine, type shape) may be inlined, trimmed to the decision.
- **Testing Decisions** — what makes a good test here (external behavior only), which modules get tested, prior art in the codebase
- **Out of Scope** — what this explicitly does not cover

If the project has an issue tracker configured (`/robobuilder:setup` in Standard),
publish the PRD there with the `needs-triage` label. Otherwise keep it in the repo
(e.g. `docs/prd/`).

**DONE when:** the PRD exists and the user agrees it captures the plan.

**Existing code → Health dashboard**

Run the project's own quality tools and score them. Read-only; never fix anything
here — findings become issues in Stage 3.

1. **Detect the stack.** Read a `## Health Stack` section in CLAUDE.md if present;
   otherwise auto-detect type checker, linter, test runner, dead-code detector, and
   shell linter. Offer to persist the detected stack to CLAUDE.md.
2. **Run each tool** sequentially, capturing exit code, duration, and the last ~50
   lines of output. A missing tool is `SKIPPED`, not a failure.
3. **Score** each category 0–10 and compute a weighted composite
   (tests 28%, type check 22%, lint 18%, dead code 13%, shell 9%; redistribute a
   skipped tool's weight). Present a dashboard table with a composite score and,
   for anything below 7, the actual tool output so the user can act.
4. **Rank** the findings by `weight × (10 − score)`, and place each on the Stage 1
   map — a failure in a module nothing calls is not the same problem as the same
   failure under everything.

Wrap, don't replace: report exactly what the tools say. Be honest — 100 type errors
with passing tests is not a healthy codebase.

**DONE when:** the dashboard exists and the findings are ranked and located.

### Stage 3 — Issues

Both paths land here. Break the Stage 2 artifact — the PRD, or the ranked findings —
into issues small enough to pick up one at a time.

**From a PRD:** each issue is a thin **vertical slice** cutting through every layer
end to end (schema → API → UI → tests), NOT a horizontal slice of one layer.

**From health findings:** vertical slicing doesn't apply — "fix 100 type errors"
cuts through nothing. Slice by **blast radius** instead: one coherent fix per issue,
smallest safely-revertable unit, ordered by the Stage 2 ranking so the highest
`weight × gap` in the most-depended-on module goes first. A finding that needs a
design decision isn't an issue yet — it's a new idea, so send it back through Stage 1
as a grill.

Rules for both:
- Each issue delivers a narrow but **complete** change and stands on its own
- Prefer many thin issues over few thick ones
- Mark each **AFK** (an agent can finish and merge it unattended) or **HITL**
  (needs a human decision or review). Prefer AFK.

Present the breakdown as a numbered list. For each show: title, AFK/HITL,
blocked-by, and what it covers — user stories from a PRD, or the finding and its
score from a health run. Ask the user whether the granularity and dependencies look
right, and iterate until they approve.

Then publish each approved slice as an issue, in dependency order (blockers first,
so you can reference real IDs in "Blocked by"). Issue body:

```
## What to build
End-to-end behavior of this slice (not layer-by-layer). No file paths.

## Acceptance criteria
- [ ] ...

## Blocked by
- #<id>   (or "None — can start immediately")
```

**DONE when:** every slice is an issue in the tracker, in dependency order.

**Next:** run `/robobuilder-lite:build` to pick up the first ready issue.

## Example

> **User:** I want to add saved searches to the app.
>
> **plan (Grill):** One at a time — Should a saved search capture the query only,
> or also the sort and filters? My recommendation: query + filters + sort, because
> users expect the exact view back… *(continues until every branch is decided)*
>
> **plan (PRD):** Modules: `SavedSearch` (deep — stores + replays a view),
> `SearchBar` integration. User stories: 1. As a user, I want to save my current
> search so I can return to it… *(full PRD, published as needs-triage)*
>
> **plan (Issues):** 1. *Save & list saved searches* (AFK) — schema + API + a list
> in the sidebar, end to end. 2. *Replay a saved search* (AFK, blocked by #1)…

> **User:** I inherited this repo and don't know where to start. `--health`
>
> **plan (Map):** `billing/` is called by `checkout`, `admin`, and the nightly job;
> `reports/` is called by nothing but the CLI. *(map of modules + callers)*
>
> **plan (Health):** 6.1/10 composite. tsc 41 errors (score 3, weight 22%), lint
> clean, dead code 12 files. Ranked: **tsc errors in `billing/`** first — worst gap,
> and the map says three callers depend on it. The `reports/` dead code ranks last
> despite being larger; nothing calls it.
>
> **plan (Issues):** 1. *Type-clean `billing/` payment path* (AFK, smallest revertable
> unit, covers finding #1)… 2. *Delete unreachable `reports/` exporters* (AFK)…

## Anti-pattern

- **Horizontal slices.** "Issue 1: all the tables. Issue 2: all the endpoints."
  Nothing is demoable until the end and integration risk is hidden until it's
  expensive. Slice vertically — on the PRD path.
- **Grilling with flattery.** "Great idea!" then moving on. If you didn't push on
  the weak part of the design, you didn't grill.
- **Interviewing during the PRD stage.** The PRD synthesizes decisions already made;
  it does not reopen them.
- **Measuring before mapping, or fixing while measuring.** A finding you can't place
  on the map can't be ranked, and Stage 2 is read-only — findings become issues in
  Stage 3, not edits in Stage 2.

## See Also

- `/robobuilder-lite:build` — pick up an issue and implement it with TDD
- `/robobuilder-lite:improve` — review before you merge
- `/robobuilder-lite:ship` — package, PR, land, deploy
- For the unbundled originals (`grill-me`, `to-prd`, `to-issues`, `zoom-out`,
  `health`, plus `design-an-interface` and `grill-with-docs`), see **Robo Builder
  Standard**.
