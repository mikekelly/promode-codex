---
name: sync
description: "Explicit user-invoked sync, install, update, or repair for Promode for Codex project files. Use only when the user invokes `$promode-codex:sync` or explicitly asks the main agent to sync Promode project files."
---

<objective>
Make the current project ready for Promode for Codex by syncing the bundled
Promode custom-agent templates into project `.codex/agents/`, syncing the
Promode doctrine bundle into `.codex/promode/docs/`, and removing legacy
hook-based Promode artifacts. After a successful sync, perform a best-effort
GitHub check and warn if this plugin copy is older than the latest available
Promode for Codex version.
</objective>

<required_reading>
Read before acting:
1. `../../standard/docs/codex-assumptions.md`
2. All files in `../../standard/agents/`
3. `../../standard/docs/index.md`
4. `../../standard/docs/opinion-register.md`
</required_reading>

<process>
1. Verify the target project with `pwd` and `git status --short`.
2. Run the bundled sync helper:
   ```bash
   python3 {plugin_root}/scripts/install-project-agents.py {project_path}
   ```
   Use `--skip-upgrade-check` only for offline or deterministic validation
   runs.
3. Preserve non-Promode files under `.codex/agents/` and `.codex/hooks.json`.
   Treat `.codex/agents/promode_*.toml` and `.codex/promode/docs/` as
   Promode-owned generated mirrors.
4. Do not edit `AGENTS.md` unless the user explicitly asks.
5. Do not install Promode main-session hooks. Promode is activated explicitly
   with `$promode-codex:activate` in each session.
6. If the helper warns that a newer plugin is available, tell the user to run
   `codex plugin marketplace upgrade promode-codex`, then start a new task or
   session. If the updated plugin is not visible, restart Codex.
7. Verify all eleven `.codex/agents/promode_*.toml` files exist and that
   `.codex/promode/docs/opinion-register.md` exists.
8. Tell the user to start a new task or session so project custom-agent roles
   are discovered. If the roles do not appear, restart Codex. Then run
   `$promode-codex:activate` in sessions where they want Promode behavior.
</process>

<success_criteria>
The project has the eleven Promode custom-agent files under `.codex/agents/`,
the Promode doctrine bundle under `.codex/promode/docs/`, legacy Promode hook
artifacts are absent, non-Promode project files were preserved, stale plugin
cache warnings are surfaced when detected, and the user knows the new-session,
restart-if-needed, and activation sequence.
</success_criteria>
