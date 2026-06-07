<required_reading>
Read:
1. `../../../standard/agents/`
2. `../references/codex-assumptions.md`
</required_reading>

<process>
1. Confirm `.codex/agents/` exists. If not, route to install.
2. Prefer `python3 {plugin_root}/scripts/install-project-agents.py {project_path}`.
   It refreshes the project hooks and seven Promode-owned agent templates. The
   main brief stays bundled in the plugin and is read through `PLUGIN_ROOT`.
3. Preserve non-Promode custom agents.
4. Do not touch `AGENTS.md`.
5. Remind the user that changed hooks need `/hooks` review and trust.
6. Verify all seven Promode files exist.
</process>

<success_criteria>
The project Promode hooks and custom-agent files match the plugin templates,
the main brief is not copied into `.codex/`, and no non-Promode project agent
files were removed.
</success_criteria>
