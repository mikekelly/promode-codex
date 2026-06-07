# Promode for Codex

Promode for Codex adapts the Promode AI-assisted software development
methodology to Codex's plugin, hook, skill, and subagent runtime.

This is intentionally a separate plugin from the Claude Code version. The
methodology is shared; the runtime contract is not.

## What It Provides

- A Codex marketplace manifest at `.agents/plugins/marketplace.json`
- A Codex plugin manifest at `plugins/promode-codex/.codex-plugin/plugin.json`
- Bundled `SessionStart` hooks, plus project-local hook install support, that
  inject the Promode main-agent brief and check project-agent drift
- Codex skills for setup, audits, handoff, subagent recovery, and
  discovery-to-determinism testing strategy
- Project-scoped custom-agent templates under `plugins/promode-codex/standard/agents/`
- Validation scripts that check the hook output and custom-agent TOML

## Codex Adaptation

Promode for Codex differs from the Claude Code plugin in important ways:

- Codex hooks require review and trust in `/hooks` before they run.
- This local harness currently reports `plugin_hooks=false`, so project setup
  installs a project-local `.codex/hooks.json` hook as the reliable path. The
  bundled plugin hook remains for Codex builds where plugin hooks are enabled.
- Codex custom agents live in `.codex/agents/*.toml` or `~/.codex/agents/*.toml`;
  they are not bundled plugin agent files.
- Codex subagents inherit parent runtime settings and are config layers, not
  separate hard-permission boundaries.
- Codex transcript paths are convenience fields, not stable APIs.
- Delegation is consent-first. Promode should not silently spawn subagents when
  the user did not ask for Promode, delegation, or parallel agent work.

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

Then start a new thread so Codex loads the plugin's skills and hooks. You can
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

After the plugin is installed and enabled, ask Codex from the target project:

```text
Set up promode-codex in this project.
```

The `managing-promode-codex` skill installs project-scoped Promode agents into
`.codex/agents/`, copies project-local hook scripts into `.codex/hooks/`, and
merges the Promode `SessionStart` hook pair into `.codex/hooks.json`. The main
brief stays bundled in the plugin; the project-local main hook reads it through
`PLUGIN_ROOT`.

Review and trust the project hooks with `/hooks`, then restart Codex, resume the
project thread, or start a fresh session in the project. This lets `SessionStart`
hooks run and lets Codex expose the newly installed project custom-agent roles.

## Installation While Developing Locally

From a Codex session with this plugin installed and enabled:

1. Ask Codex: `Set up promode-codex in this project`.
2. The `managing-promode-codex` skill installs project agents into
   `.codex/agents/` and project-local `SessionStart` hooks under `.codex/`.
3. Review and trust the project hook with `/hooks`, then restart Codex, resume
   the project thread, or start a fresh session in the project so the main brief
   and project custom-agent roles are loaded.

For a direct local install of project agents from this repo:

```bash
python3 plugins/promode-codex/scripts/install-project-agents.py /path/to/project
```

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
when syncing methodology, agent definitions, skills, hooks, docs, or runbooks
from the Claude Code Promode plugin into this Codex adaptation.

## Sources Checked

This repo is tuned against current Codex docs for:

- Plugins: https://developers.openai.com/codex/plugins/build
- Skills: https://developers.openai.com/codex/skills
- Hooks: https://developers.openai.com/codex/hooks
- Subagents: https://developers.openai.com/codex/subagents

See `plugins/promode-codex/skills/managing-promode-codex/references/codex-assumptions.md`
for the exact assumptions captured in the plugin.
