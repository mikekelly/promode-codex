<required_reading>
Read:
1. `../references/codex-assumptions.md`
2. `../../../standard/agents/`
3. `../../activate/SKILL.md`
</required_reading>

<process>
Audit read-only.

Check:
1. Plugin files exist in the installed plugin root:
   - `.codex-plugin/plugin.json`
   - `skills/activate/SKILL.md`
   - `skills/sync/SKILL.md`
   - `standard/agents/promode_*.toml`
   - `standard/docs/opinion-register.md`
2. Project custom agents:
   - `.codex/agents/promode_implementer.toml`
   - `.codex/agents/promode_reviewer.toml`
   - `.codex/agents/promode_debugger.toml`
   - `.codex/agents/promode_verifier.toml`
   - `.codex/agents/promode_environment_manager.toml`
   - `.codex/agents/promode_product_designer.toml`
   - `.codex/agents/promode_agent_analyzer.toml`
3. Project Promode doctrine:
   - `.codex/promode/docs/opinion-register.md`
4. Legacy hook artifacts should be absent:
   - `.codex/PROMODE_CODEX_MAIN.md`
   - `.codex/hooks/promode-main-context.py`
   - `.codex/hooks/promode-agent-drift.py`
   - Promode hook commands in `.codex/hooks.json`
5. `AGENTS.md` status:
   - Present and project-owned, or missing with recommendation to scaffold.
   - Do not treat missing `AGENTS.md` as a Promode install failure.
6. Activation:
   - Report that Promode is activated per session with `$promode-codex:activate`.

Output:
```markdown
# Promode for Codex Audit - <project>

| Component | Status | Notes |
| --- | --- | --- |
| Plugin manifest | PASS/FAIL | ... |
| Activate/sync skills | PASS/FAIL | ... |
| Project Promode agents | PASS/FAIL | ... |
| Project Promode doctrine | PASS/FAIL | ... |
| Legacy Promode hooks absent | PASS/FAIL | ... |
| AGENTS.md | INFO | ... |
| Activation | INFO | Run `$promode-codex:activate` per session |

## Recommended Actions
1. ...
```
</process>

<success_criteria>
Audit reports PASS/FAIL/INFO for every component without modifying files.
</success_criteria>
