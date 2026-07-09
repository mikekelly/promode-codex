<required_reading>
Read:
1. `../../../standard/agents/`
2. `../../../standard/docs/index.md`
3. `../../../standard/docs/opinion-register.md`
4. `../references/codex-assumptions.md`
</required_reading>

<process>
1. Confirm the target project with `pwd` and `git status --short`.
2. Prefer the dedicated `$promode-codex:sync` skill. If acting from this
   compatibility workflow, run:
   ```bash
   python3 {plugin_root}/scripts/install-project-agents.py {project_path}
   ```
   Use `--skip-upgrade-check` only for offline or deterministic validation
   runs.
3. The helper syncs the seven Promode-owned custom-agent templates into
   `.codex/agents/`.
4. The helper syncs the Promode-owned doctrine bundle into
   `.codex/promode/docs/`. Project custom agents read the project-local
   opinion register from this path instead of referencing the plugin cache.
5. The helper removes legacy Promode hook artifacts:
   - `.codex/PROMODE_CODEX_MAIN.md`
   - `.codex/hooks/promode-main-context.py`
   - `.codex/hooks/promode-agent-drift.py`
   - Promode hook commands inside `.codex/hooks.json`
6. Preserve non-Promode custom agents and non-Promode hooks. Treat
   `.codex/promode/docs/` as Promode-owned generated state.
7. Do not touch `AGENTS.md`.
8. If the helper warns that a newer plugin version is available, tell the user
   to upgrade the configured marketplace, then restart or resume Codex.
9. Remind the user to restart Codex, resume the project thread, or start a
   fresh session in the project so refreshed `.codex/agents/*.toml` files are
   exposed as custom-agent roles.
10. Tell the user to run `$promode-codex:activate` at the start of each session
   where they want Promode behavior.
11. Verify all seven Promode agent files exist and
    `.codex/promode/docs/opinion-register.md` exists.
</process>

<success_criteria>
The project custom-agent files match the plugin templates, legacy Promode hook
artifacts are absent, the project-local Promode doctrine bundle is present, no
non-Promode project agent or hook files were removed, stale plugin cache
warnings are surfaced when detected, and the user has clear restart/resume plus
activation instructions.
</success_criteria>
