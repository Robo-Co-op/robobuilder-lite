---
name: plan
description: "[Lite-1 Plan] Take a rough idea to shippable issues in one flow: grill the design, write a PRD, then split it into vertical-slice issues. Use when starting a new feature, turning an idea into a spec, or breaking work into tickets."
origin: robobuilder-lite
upstream: https://github.com/Robo-Co-op/robobuilder-standard
merged-from: grill-me, to-prd, to-issues
---

# Plan

## What

One command that carries a feature from a rough idea to a set of ready-to-build
issues. It runs three stages back to back:

1. **Grill** — interview you until the design is actually decided
2. **PRD** — write the shared understanding down as a product requirements doc
3. **Issues** — split the PRD into thin vertical slices you can pick up one at a time

This is the Lite bundle of three Standard skills (`grill-me`, `to-prd`,
`to-issues`). It keeps the discipline and drops the ceremony.

## When

Use `/robobuilder-lite:plan` when:
- You have an idea and want to think it through before writing code
- You have a decision to make and want to be pushed on it, not flattered
- You already have a spec or PRD and just need it broken into tickets

You can enter at any stage. If you already have a written PRD, say so — plan skips
grilling and goes straight to issues.

## Why

Most feature work goes wrong before the first line of code: the design has an
unresolved branch nobody noticed, or the work gets sliced horizontally (all the
database, then all the API, then all the UI) so nothing is demoable until the end.
Plan forces the decisions out early and slices vertically so every issue is a
complete, shippable path through the system.

## How

### Stage 1 — Grill  (skip if the design is already settled)

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

### Stage 2 — PRD

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

### Stage 3 — Issues

Break the PRD into **tracer-bullet** issues. Each issue is a thin **vertical
slice** that cuts through every layer end to end (schema → API → UI → tests), NOT a
horizontal slice of one layer.

Rules:
- Each slice delivers a narrow but **complete** path and is demoable on its own
- Prefer many thin slices over few thick ones
- Mark each slice **AFK** (an agent can finish and merge it unattended) or **HITL**
  (needs a human decision or review). Prefer AFK.

Present the breakdown as a numbered list. For each slice show: title, AFK/HITL,
blocked-by, and which user stories it covers. Ask the user whether the granularity
and dependencies look right, and iterate until they approve.

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

## Anti-pattern

- **Horizontal slices.** "Issue 1: all the tables. Issue 2: all the endpoints."
  Nothing is demoable until the end and integration risk is hidden until it's
  expensive. Slice vertically.
- **Grilling with flattery.** "Great idea!" then moving on. If you didn't push on
  the weak part of the design, you didn't grill.
- **Interviewing during the PRD stage.** The PRD synthesizes decisions already made;
  it does not reopen them.
- **File paths in the PRD or issues.** They're stale by the time someone reads them.

## See Also

- `/robobuilder-lite:build` — pick up an issue and implement it with TDD
- `/robobuilder-lite:improve` — review before you merge
- `/robobuilder-lite:ship` — package, PR, land, deploy
- For the unbundled originals (`grill-me`, `to-prd`, `to-issues`, plus
  `design-an-interface` and `grill-with-docs`), see **Robo Builder Standard**.
