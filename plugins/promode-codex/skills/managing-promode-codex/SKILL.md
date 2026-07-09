---
name: managing-promode-codex
description: "Compatibility router for Promode for Codex setup, activation, audit, sync, install, repair, update, and migration requests. Prefer the dedicated activate and sync skills when the user asks to turn Promode on or sync project files."
---

<essential_principles>
Promode for Codex has two layers:

1. **Plugin layer** - this plugin supplies explicit skills. Users run
   `$promode-codex:activate` to load the main Promode brief into the current
   session.
2. **Project layer** - `$promode-codex:sync` syncs project-scoped custom
   agents under `.codex/agents/`, a Promode doctrine bundle under
   `.codex/promode/docs/`, and removes legacy hook-based Promode artifacts.

The project's `AGENTS.md` is project-owned. Promode may offer to scaffold it
when missing, but must never overwrite or rewrite it without explicit user
approval.
</essential_principles>

<codex_runtime_facts>
- Codex plugins can package skills. Skills can include scripts and references.
- Promode for Codex no longer uses hooks as the primary main-brief delivery
  path; activation is explicit and session-scoped.
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
- Never install Promode main-session hooks as the default setup path.
- Never delete existing `.codex/agents/*.toml` files that are not Promode-owned.
</never_do>

<routing>
| User intent | Workflow |
| --- | --- |
| activate, turn on Promode, load main brief | Use `../activate/SKILL.md` |
| sync, install, set up, add, update, refresh, repair Promode agents | `workflows/sync.md` |
| audit, check setup, verify install | `workflows/audit.md` |

Route directly when intent is clear. Ask only when the user has not specified
sync/install/audit and the surrounding context does not disambiguate it.
</routing>

<reference_index>
- `references/codex-assumptions.md` - verified Codex behavior this plugin relies on.
- `../activate/SKILL.md` - main-session brief loaded by `$promode-codex:activate`.
- `../../standard/agents/*.toml` - project custom-agent templates synced by
  `$promode-codex:sync`.
- `../../standard/docs/` - project-local Promode doctrine bundle synced by
  `$promode-codex:sync`.
- `../../scripts/install-project-agents.py` - deterministic project sync helper.
</reference_index>

<success_criteria>
A project is set up when:
- `.codex/agents/promode_*.toml` exists for all standard Promode agents.
- `.codex/promode/docs/opinion-register.md` exists for project-local Promode
  doctrine.
- Existing non-Promode `.codex/agents` files are preserved.
- The user knows to restart, resume, or start a fresh Codex session so newly
  installed custom-agent roles are available.
- The user knows to run `$promode-codex:activate` at the start of sessions where
  they want Promode behavior.
- `AGENTS.md` was left alone unless the user explicitly accepted scaffolding.
- Optional tracking files were created only when missing and approved.
</success_criteria>
