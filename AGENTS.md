# Repository Guidance

This repository is a Codex plugin marketplace. The actual Codex plugin lives
under `plugins/promode-codex/`. Keep Claude Code compatibility concerns out of
this repo; the sibling `promode` repository owns the Claude Code plugin.

## Commands

- Run the full local check:
  `scripts/check`
- Validate Promode-specific assumptions:
  `python3 plugins/promode-codex/scripts/validate-promode-codex.py --mode source`
- Validate Codex plugin shape:
  `python3 /Users/mike/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/promode-codex`

## Structure

- `.agents/plugins/marketplace.json` - Codex marketplace manifest
- `docs/PROJECT_FRAMING.md` - product goals, risks, non-goals, and runtime boundaries
- `docs/DECISIONS.md` - durable Codex adaptation decisions
- `docs/TRACEABILITY.md` - product/runtime claims mapped to validation checks
- `plugins/promode-codex/.codex-plugin/plugin.json` - Codex plugin manifest
- `plugins/promode-codex/hooks/` - plugin-bundled lifecycle hooks
- `plugins/promode-codex/standard/PROMODE_CODEX_MAIN.md` - main-session Promode brief injected by hook
- `plugins/promode-codex/standard/agents/` - project-scoped Codex custom-agent templates
- `plugins/promode-codex/skills/` - bundled Codex skills
- `plugins/promode-codex/scripts/` - local validation and install helpers
- `RUNBOOKS.md` and `runbooks/` - repeatable maintenance procedures

## Codex Runtime Rules

- Hooks are not trusted automatically. Users must review project or plugin hooks
  in `/hooks`.
- The local harness currently reports `plugin_hooks=false`; project-local hooks
  are the reliable install path.
- Project custom agents are installed into `.codex/agents/`.
- In this marketplace checkout only, root `/.codex/` is generated local setup
  state and is ignored. Do not generalize that to user projects where `.codex/`
  may contain project-owned hooks, agents, and config.
- `validate-promode-codex.py --mode source` requires this source marketplace
  repo layout. Installed plugin cache copies should use auto/default mode or
  `--mode package` so they do not require `.agents/plugins/marketplace.json`.
- Do not put the Promode main orchestration brief into a user's `AGENTS.md`.
- Treat Codex transcript files as unstable convenience data.
