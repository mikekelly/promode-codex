<required_reading>
Read:
1. `../references/codex-assumptions.md`
2. `../../../hooks/hooks.json`
3. `../../../standard/agents/`
</required_reading>

<process>
Audit read-only.

Check:
1. Plugin files exist in the installed plugin root:
   - `.codex-plugin/plugin.json`
   - `hooks/hooks.json`
   - `hooks/promode-main-context.py`
   - `hooks/promode-agent-drift.py`
   - `standard/PROMODE_CODEX_MAIN.md`
2. Project hook and custom agents:
   - `.codex/hooks/promode-main-context.py`
   - `.codex/hooks/promode-agent-drift.py`
   - `.codex/hooks.json` with a Promode `SessionStart` entry
   - `.codex/agents/promode_implementer.toml`
   - `.codex/agents/promode_reviewer.toml`
   - `.codex/agents/promode_debugger.toml`
   - `.codex/agents/promode_verifier.toml`
   - `.codex/agents/promode_environment_manager.toml`
   - `.codex/agents/promode_product_designer.toml`
   - `.codex/agents/promode_agent_analyzer.toml`
   - `.codex/PROMODE_CODEX_MAIN.md` should be absent; the hook should read the
     bundled plugin brief through `PLUGIN_ROOT`.
3. `AGENTS.md` status:
   - Present and project-owned, or missing with recommendation to scaffold.
   - Do not treat missing `AGENTS.md` as a Promode install failure.
4. Hook trust:
   - You cannot reliably inspect trust from project files alone.
   - Report that the user should run `/hooks` to confirm the project hook is trusted.

Output:
```markdown
# Promode for Codex Audit - <project>

| Component | Status | Notes |
| --- | --- | --- |
| Plugin manifest | PASS/FAIL | ... |
| Project SessionStart hook | PASS/FAIL | ... |
| Project Promode agents | PASS/FAIL | ... |
| AGENTS.md | INFO | ... |
| Hook trust | CHECK | Confirm in /hooks |

## Recommended Actions
1. ...
```
</process>

<success_criteria>
Audit reports PASS/FAIL/CHECK for every component without modifying files.
</success_criteria>
