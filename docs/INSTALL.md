# Installing Robo Builder Lite

## Claude Code

```sh
/plugin marketplace add Robo-Co-op/robobuilder-lite
/plugin install robobuilder-lite@robo-coop-tools
/reload-plugins
```

Verify the four skills are available:

```sh
/robobuilder-lite:plan
```

## What gets installed

- 4 skills: `plan`, `build`, `improve`, `ship`
- 6 hooks (see `hooks/hooks.json`) — run automatically:
  - **PreToolUse** on Edit/Write blocks committing secrets
  - **PostToolUse** on Edit/Write auto-formats changed files
  - **SessionStart / Notification** surface lifecycle notifications
  - **PreCompact / SessionEnd** consolidate memory
- 6 review agents used by `improve` and `build`

The hooks call the bundled Python scripts under `scripts/` via
`${CLAUDE_PLUGIN_ROOT}`, so no absolute paths need configuring. Python 3 must be on
PATH.

## Using Claude Code on the web (claude.ai/code)

The `/plugin` flow above is for the local CLI and doesn't carry over to web
sessions — the web runtime doesn't read `~/.claude/plugins/`. To run Lite's
skills there, see [robobuilder-standard's CLAUDE_CODE_WEB.md](https://github.com/Robo-Co-op/robobuilder-standard/blob/main/docs/CLAUDE_CODE_WEB.md)
for the two options (committing skills into the repo, or registering them as
account-level skills) — both apply the same way whether the skill came from
Lite, Standard, or Pro.

## Graduating to Standard

Lite is intentionally small. When you want the finer-grained tools (separate
`grill-me`, `tdd`, `cso`, `canary`, playbooks, meta skills), install Standard
alongside Lite:

```sh
/plugin marketplace add Robo-Co-op/robobuilder-standard
/plugin install robobuilder@robo-coop-tools
```

The command namespaces differ (`/robobuilder-lite:*` vs `/robobuilder:*`), so the
two plugins coexist without collision.

## Uninstall

```sh
/plugin uninstall robobuilder-lite
```
