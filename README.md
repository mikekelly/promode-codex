# Promode for Codex

Promode for Codex adapts the Promode AI-assisted software development
methodology to Codex's plugin, skill, and subagent runtime.

This is intentionally a separate plugin from the Claude Code version. The
methodology is shared; the runtime contract is not.

## What It Provides

- A Codex marketplace manifest at `.agents/plugins/marketplace.json`
- A Codex plugin manifest at `plugins/promode-codex/.codex-plugin/plugin.json`
- `$promode-codex:activate` to load the Promode main-agent brief into the
  current session
- `$promode-codex:sync` to sync project-scoped custom agents and remove
  legacy hook-based Promode artifacts
- Command-equivalent Codex skills for audits and handoff
- Project-scoped custom-agent templates under `plugins/promode-codex/standard/agents/`
- Project-local Promode doctrine templates under `plugins/promode-codex/standard/docs/`
- Validation scripts that check activation/sync behavior and custom-agent TOML

## Codex Adaptation

Promode for Codex differs from the Claude Code plugin in important ways:

- Promode activation is explicit. Run `$promode-codex:activate` at the start of
  each Codex session where you want Promode behavior.
- Project setup no longer installs Promode main-session hooks. `$promode-codex:sync`
  removes legacy Promode hook artifacts from older installs.
- Codex custom agents live in `.codex/agents/*.toml` or `~/.codex/agents/*.toml`;
  they are not bundled plugin agent files.
- Copied project custom agents read shared Promode doctrine from
  `.codex/promode/docs/opinion-register.md`; they do not reference versioned
  plugin-cache paths.
- The exposed skill surface is deliberately small: `activate`, `sync`,
  `promode-audit`, and `handoff`. Larger methodology mechanics such as
  discovery-to-determinism live in synced docs and role prompts, matching the
  current Claude Promode shape more closely.
- Codex subagents inherit parent runtime settings and are config layers, not
  separate hard-permission boundaries.
- Codex transcript paths are convenience fields, not stable APIs.
- Activation authorizes Promode's methodology for the session, including
  routine methodology-aligned delegation. Promode still asks before unusual
  cost, permission changes, external services, separate workspaces, or anything
  that conflicts with the user's stated preference.
- Model tiering follows role responsibility: the main orchestrator and CTO
  should run on GPT-5.5 for now; specialist agents are pinned to `gpt-5.5`,
  with `promode_fast_worker` pinned to `gpt-5.4-mini`.

## Install From GitHub

Codex installs plugins from a marketplace source, not directly from an
arbitrary plugin folder. This repository is the marketplace source:
`.agents/plugins/marketplace.json` points at the plugin payload in
`plugins/promode-codex/`.

```bash
codex plugin marketplace add mikekelly/promode-codex
codex plugin marketplace upgrade
codex plugin add promode-codex@promode-codex
```

Then start a new thread so Codex loads the plugin's skills. You can
also open Codex, run `/plugins`, select **Promode for Codex**, and install it
from the plugin UI.

For a fixed release, pass a tag or branch:

```bash
codex plugin marketplace add mikekelly/promode-codex --ref <tag-or-branch>
```

The marketplace manifest in this repo uses this shape:

```json
{
  "name": "promode-codex",
  "interface": {
    "displayName": "Promode for Codex"
  },
  "plugins": [
    {
      "name": "promode-codex",
      "source": {
        "source": "local",
        "path": "./plugins/promode-codex"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

## Set Up a Project

After the plugin is installed and enabled, run these from the target project:

```text
$promode-codex:sync
$promode-codex:activate
```

`$promode-codex:sync` installs or refreshes the eleven project-scoped Promode
agents in `.codex/agents/` and removes legacy Promode hook artifacts left by
older installs. It also mirrors Promode doctrine into `.codex/promode/docs/` so
copied agents can read the project-local opinion register. It prunes stale
Promode-owned `.codex/agents/promode_*.toml` files while preserving
non-Promode agents and non-Promode hooks. After a successful sync, it performs a
best-effort GitHub version check and warns if the installed plugin copy is older
than the latest available Promode for Codex version.

Restart Codex, resume the project thread, or start a fresh session in the
project after sync so Codex exposes the newly installed project custom-agent
roles.

`$promode-codex:activate` contains the main Promode brief and makes Promode
active for the current main-agent session. Activation is explicit and
session-scoped; run it at the start of each main-agent session where you want
Promode behavior. It is not intended for subagents, which should use their
custom-agent instructions.

## Installation While Developing Locally

From a Codex session with this plugin installed and enabled:

1. Run `$promode-codex:sync`.
2. Restart Codex, resume the project thread, or start a fresh session in the
   project so project custom-agent roles are loaded.
3. Run `$promode-codex:activate` in each session where you want Promode
   behavior.

For a direct local install of project agents from this repo:

```bash
python3 plugins/promode-codex/scripts/install-project-agents.py /path/to/project
```

Then restart or resume Codex in that project and run `$promode-codex:activate`.
Use `--skip-upgrade-check` for deterministic local validation or offline runs.

## Validate

```bash
scripts/check
```

Or run the component checks directly:

```bash
python3 plugins/promode-codex/scripts/validate-promode-codex.py --mode source
python3 /Users/mike/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/promode-codex
```

The first script validates Promode-specific assumptions. The second validates
Codex plugin manifest and skill shape according to the local Codex plugin
validator.

When running from an installed plugin cache rather than this source marketplace
repo, use the validator's default auto mode or `--mode package`:

```bash
python3 /path/to/installed/promode-codex/scripts/validate-promode-codex.py
python3 /path/to/installed/promode-codex/scripts/validate-promode-codex.py --mode package
```

Package mode validates the plugin payload and project installer behavior without
requiring the source-repo `.agents/plugins/marketplace.json` wrapper.

## Project Knowledge

- [Project framing](docs/PROJECT_FRAMING.md) - goals, risks, non-goals, and runtime boundaries
- [Decision index](docs/DECISIONS.md) - durable Codex adaptation decisions
- [Validation traceability](docs/TRACEABILITY.md) - product/runtime claims mapped to checks

## Runbooks

Operational maintenance runbooks live in [`RUNBOOKS.md`](RUNBOOKS.md). Start
with [Check alignment with the Claude Code Promode repo](runbooks/check-promode-alignment.md)
when syncing methodology, agent definitions, skills, docs, or runbooks
from the Claude Code Promode plugin into this Codex adaptation.

## Sources Checked

This repo is tuned against current Codex docs for:

- Plugins: https://developers.openai.com/codex/plugins/build
- Skills: https://developers.openai.com/codex/skills
- Subagents: https://developers.openai.com/codex/subagents

See `plugins/promode-codex/standard/docs/codex-assumptions.md`
for the exact assumptions captured in the plugin.
