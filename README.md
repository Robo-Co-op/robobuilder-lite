# robobuilder-lite

**Robo Builder Lite — the beginner on-ramp.**

Forty-one skills is a lot to learn on day one. Lite collapses the whole
development workflow into **four commands** you can memorize in a minute, then
graduate from into the full Standard edition when you want the finer-grained tools.

## Three editions

| Edition | Repo | Who it's for |
|---|---|---|
| **Lite** (this repo) | [robobuilder-lite](https://github.com/Robo-Co-op/robobuilder-lite) | Beginners — learn the workflow with 4 commands |
| **Standard** | [robobuilder-standard](https://github.com/Robo-Co-op/robobuilder-standard) | Daily development — 41 skills / 9 agents / 6 hooks |
| **Pro** | [robobuilder-pro](https://github.com/Robo-Co-op/robobuilder-pro) | Loop & Graph Engineering — autonomous agent loops, and the graph that keeps them honest (add-on to Standard) |

## The four commands

| Command | Does | Bundles (from Standard) |
|---|---|---|
| `/robobuilder-lite:plan` | New feature: idea → grilled design → PRD. Existing code: map → `--health` measure. Both → issues | grill-me, to-prd, to-issues, zoom-out, health |
| `/robobuilder-lite:build` | Pick an issue → red-green-refactor; bug branch when something breaks | triage, tdd, diagnose |
| `/robobuilder-lite:improve` | Review before merge; `--deep` / `--security` / `--refactor` | diff-review, cross-review, grill, cso, improve-codebase-architecture, request-refactor-plan |
| `/robobuilder-lite:ship` | Green tests → PR → merge → CI → deploy verify | ship, land-and-deploy |

The typical loop: **plan → build → improve → ship**, then back to plan for the next
piece of work — and it's the same four either way. A new feature enters plan as an
idea and gets grilled; existing code enters plan as a codebase and gets mapped and
measured. Both leave plan as issues, so build onward doesn't care which you started
with.

## What ships with it

- The same 6 lifecycle **hooks** as Standard (secret-blocking, auto-format,
  notifications, memory consolidation)
- The 6 **review agents** the skills call (code-simplifier, test-writer,
  security-auditor, e2e-tester, tdd-pair, codebase-explorer)

## Install

```sh
/plugin marketplace add Robo-Co-op/robobuilder-standard
/plugin install robobuilder-lite@robo-coop-tools
/reload-plugins
```

The marketplace catalog (`robo-coop-tools`) lives in the Standard repo and lists all
three editions — that's why the `marketplace add` line points there even when you
only want Lite. Adding `Robo-Co-op/robobuilder-lite` as a marketplace does not work.

`/plugin` is terminal-CLI only. In the Claude desktop app use its plugin browser, and
for web sessions declare the plugin in `.claude/settings.json` — see `docs/INSTALL.md`.

When you outgrow the four commands, install
[Robo Builder Standard](https://github.com/Robo-Co-op/robobuilder-standard) for the
full 41-skill set — the commands don't collide, so you can run both.

These four don't get retired later, either. [Robo Builder
Pro](https://github.com/Robo-Co-op/robobuilder-pro)'s `dev-loop` runs *this* cycle —
`plan → build → improve → ship` — as the inner loop of an autonomous one, so Lite stays
the engine rather than becoming a stepping stone. Pro requires Lite installed alongside
it for that reason.

## Attribution

Lite's four skills are merged and adapted from three MIT-licensed upstreams:

- 🟢 Matt Pocock — [mattpocock/skills](https://github.com/mattpocock/skills)
- 🟠 Garry Tan — [garrytan/gstack](https://github.com/garrytan/gstack)
- 🔵 Jin Kim — Robo Co-op custom skills

Full license and per-skill derivation in `LICENSE`.
