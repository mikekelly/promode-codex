# Repository Guidance

This repository is a Codex plugin marketplace. The actual Codex plugin lives
under `plugins/promode-codex/`. Keep Claude Code compatibility concerns out of
this repo; the sibling `promode` repository owns the Claude Code plugin.

Before significant changes, read `docs/PROJECT_FRAMING.md` for the canonical
purpose, intended users and jobs, goals, risks, non-goals, and runtime
boundaries. Do not infer product need from plugin structure or Promode opinions.

## Commands

- Run the full local check:
  `scripts/check`
- Validate Promode-specific assumptions:
  `python3 plugins/promode-codex/scripts/validate-promode-codex.py --mode source`
- Validate Codex plugin shape:
  `python3 /Users/mike/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/promode-codex`

## Structure

- `.agents/plugins/marketplace.json` - Codex marketplace manifest
- `docs/PROJECT_FRAMING.md` - canonical purpose, users/jobs, goals, risks, non-goals, and runtime boundaries
- `docs/DECISIONS.md` - durable Codex adaptation decisions
- `docs/TRACEABILITY.md` - product/runtime claims mapped to validation checks
- `plugins/promode-codex/.codex-plugin/plugin.json` - Codex plugin manifest
- `plugins/promode-codex/skills/activate/SKILL.md` - main-session Promode brief loaded by `$promode-codex:activate`
- `plugins/promode-codex/standard/agents/` - project-scoped Codex custom-agent templates
- `plugins/promode-codex/standard/docs/` - project-local Promode doctrine templates synced into `.codex/promode/docs/`
- `plugins/promode-codex/skills/` - bundled Codex skills; exposed surface is `activate`, `sync`, `promode-audit`, and `handoff`
- `plugins/promode-codex/scripts/` - local validation and install helpers
- `RUNBOOKS.md` and `runbooks/` - repeatable maintenance procedures

## Codex Runtime Rules

- Promode for Codex uses explicit activation, not default main-session hooks.
  Users run `$promode-codex:activate` at the start of sessions where they want
  Promode behavior.
- `$promode-codex:sync` syncs project custom agents into `.codex/agents/`,
  syncs Promode doctrine into `.codex/promode/docs/`, and removes legacy
  Promode hook artifacts from older installs.
- Project custom agents are installed into `.codex/agents/`. Promode owns
  `.codex/agents/promode_*.toml` during sync; non-Promode agents must be
  preserved.
- In this marketplace checkout only, root `/.codex/` is generated local setup
  state and is ignored. Do not generalize that to user projects where `.codex/`
  may contain project-owned hooks, agents, and config.
- `validate-promode-codex.py --mode source` requires this source marketplace
  repo layout. Installed plugin cache copies should use auto/default mode or
  `--mode package` so they do not require `.agents/plugins/marketplace.json`.
- Do not put the Promode main orchestration brief into a user's `AGENTS.md`.
- Treat Codex transcript files as unstable convenience data.
