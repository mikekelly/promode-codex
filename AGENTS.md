# Repository Guidance

This repository is a Codex plugin. Keep Claude Code compatibility concerns out
of this repo; the sibling `promode` repository owns the Claude Code plugin.

## Commands

- Validate Promode-specific assumptions:
  `python3 scripts/validate-promode-codex.py`
- Validate Codex plugin shape:
  `python3 /Users/mike/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .`

## Structure

- `.codex-plugin/plugin.json` - Codex plugin manifest
- `hooks/` - plugin-bundled lifecycle hooks
- `standard/PROMODE_CODEX_MAIN.md` - main-session Promode brief injected by hook
- `standard/agents/` - project-scoped Codex custom-agent templates
- `skills/` - bundled Codex skills
- `scripts/` - local validation and install helpers
- `RUNBOOKS.md` and `runbooks/` - repeatable maintenance procedures

## Codex Runtime Rules

- Hooks are not trusted automatically. Users must review project or plugin hooks
  in `/hooks`.
- The local harness currently reports `plugin_hooks=false`; project-local hooks
  are the reliable install path.
- Project custom agents are installed into `.codex/agents/`.
- Do not put the Promode main orchestration brief into a user's `AGENTS.md`.
- Treat Codex transcript files as unstable convenience data.
