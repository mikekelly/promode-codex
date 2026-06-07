# Repository Guidance

This repository is a Codex plugin marketplace. The actual Codex plugin lives
under `plugins/promode-codex/`. Keep Claude Code compatibility concerns out of
this repo; the sibling `promode` repository owns the Claude Code plugin.

## Commands

- Validate Promode-specific assumptions:
  `python3 plugins/promode-codex/scripts/validate-promode-codex.py`
- Validate Codex plugin shape:
  `python3 /Users/mike/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/promode-codex`

## Structure

- `.agents/plugins/marketplace.json` - Codex marketplace manifest
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
- Do not put the Promode main orchestration brief into a user's `AGENTS.md`.
- Treat Codex transcript files as unstable convenience data.
