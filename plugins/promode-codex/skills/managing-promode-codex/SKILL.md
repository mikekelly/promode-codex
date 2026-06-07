---
name: managing-promode-codex
description: "Install, update, audit, or repair Promode for Codex in a project. MUST be loaded when the user asks to set up promode-codex, install Promode for Codex custom agents, check the Codex Promode hook or setup, update the project-scoped Promode agents, scaffold Promode project tracking files, or verify that Promode is correctly adapted for Codex."
---

<essential_principles>
Promode for Codex has two layers:

1. **Plugin layer** - this plugin supplies skills and bundled `SessionStart`
   hooks for Codex builds where plugin hooks are enabled.
2. **Project layer** - the setup workflow installs a project-local
   `SessionStart` hook pair and project-scoped custom agents under `.codex/`.
   The project-local main hook reads the bundled plugin brief through
   `PLUGIN_ROOT`. This is the reliable path in the current local harness, where
   `plugin_hooks` is disabled but regular hooks are enabled.

The project's `AGENTS.md` is project-owned. Promode may offer to scaffold it
when missing, but must never overwrite or rewrite it without explicit user
approval.
</essential_principles>

<codex_runtime_facts>
- Codex discovers plugin hooks from `hooks/hooks.json` by default when plugin
  hooks are enabled.
- Codex skips non-managed hooks until the user reviews and trusts them with `/hooks`.
- Codex custom agents live in `~/.codex/agents/` or `<project>/.codex/agents/`.
- A running session may not expose newly installed or refreshed project custom
  agents by name until Codex is restarted, resumed, or a fresh session is
  started in the project.
- Codex subagents inherit parent runtime settings; custom-agent files are config
  layers, not hard isolation boundaries.
- Codex transcript paths are convenience fields, not stable APIs.
</codex_runtime_facts>

<never_do>
- Never create, overwrite, or rewrite `AGENTS.md` without explicit user consent.
- Never write Promode's main orchestration brief into `AGENTS.md`.
- Never hand-edit `~/.codex/config.toml` unless the user asked for user-global setup.
- Never assume hooks are running; check or tell the user to review `/hooks`.
- Never delete existing `.codex/agents/*.toml` files that are not Promode-owned.
</never_do>

<routing>
| User intent | Workflow |
| --- | --- |
| install, set up, add promode-codex | `workflows/install.md` |
| update, refresh, repair Promode agents | `workflows/update.md` |
| audit, check setup, verify install | `workflows/audit.md` |

Route directly when intent is clear. Ask only when the user has not specified
install/update/audit and the surrounding context does not disambiguate it.
</routing>

<reference_index>
- `references/codex-assumptions.md` - verified Codex behavior this plugin relies on.
- `../../standard/PROMODE_CODEX_MAIN.md` - bundled main-session brief loaded by the project or plugin hook.
- `../../standard/agents/*.toml` - project custom-agent templates installed by workflows.
- `../../hooks/hooks.json`, `../../hooks/promode-main-context.py`, and
  `../../hooks/promode-agent-drift.py` - bundled hooks.
</reference_index>

<success_criteria>
A project is set up when:
- `.codex/hooks/promode-main-context.py` exists.
- `.codex/hooks/promode-agent-drift.py` exists.
- `.codex/hooks.json` has a Promode `SessionStart` hook.
- `.codex/agents/promode_*.toml` exists for all standard Promode agents.
- Existing non-Promode `.codex/agents` files are preserved.
- The user knows project hooks must be trusted through `/hooks`.
- The user knows to restart, resume, or start a fresh Codex session so newly
  installed custom-agent roles are available.
- `AGENTS.md` was left alone unless the user explicitly accepted scaffolding.
- Optional tracking files were created only when missing and approved.
</success_criteria>
