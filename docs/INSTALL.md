# Installing Robo Builder Lite

## Claude Code (terminal CLI)

```sh
/plugin marketplace add Robo-Co-op/robobuilder-standard
/plugin install robobuilder-lite@robo-coop-tools
/reload-plugins
```

> **The `marketplace add` line points at the Standard repo on purpose.** The
> marketplace catalog (`robo-coop-tools`) lives there and lists all three editions
> (Lite, Standard, Pro). This repo ships only a `plugin.json`, no
> `marketplace.json` — so `/plugin marketplace add Robo-Co-op/robobuilder-lite`
> fails. Add Standard's marketplace once, then install whichever editions you want
> from it. Installing Lite this way does **not** install Standard.

Verify the four skills are available:

```sh
/robobuilder-lite:plan
```

## Other environments (desktop app, web)

`/plugin` is a terminal-CLI command — it opens an interactive panel that doesn't
exist elsewhere. If you see **"/plugin isn't available in this environment."**:

- **Claude desktop app** — use the app's built-in plugin browser instead of `/plugin`.
- **Claude Code on the web / cloud sessions** — declare the plugin in your project's
  `.claude/settings.json`:

  ```json
  {
    "extraKnownMarketplaces": {
      "robo-coop-tools": {
        "source": { "source": "github", "repo": "Robo-Co-op/robobuilder-standard" }
      }
    },
    "enabledPlugins": {
      "robobuilder-lite@robo-coop-tools": true
    }
  }
  ```

  Commit that file so everyone on the repo gets the same setup.

For other ways to get skills into a web session (committing them into the repo's
`.claude/skills/`, or registering account-level skills), see
[robobuilder-standard's CLAUDE_CODE_WEB.md](https://github.com/Robo-Co-op/robobuilder-standard/blob/main/docs/CLAUDE_CODE_WEB.md).

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

## Graduating to Standard

Lite is intentionally small. When you want the finer-grained tools (separate
`grill-me`, `tdd`, `cso`, `canary`, playbooks, meta skills), install Standard
alongside Lite. The marketplace is already added from the install step above, so
this is a one-liner:

```sh
/plugin install robobuilder@robo-coop-tools
```

The command namespaces differ (`/robobuilder-lite:*` vs `/robobuilder:*`), so the
two plugins coexist without collision.

## Uninstall

```sh
/plugin uninstall robobuilder-lite
```
