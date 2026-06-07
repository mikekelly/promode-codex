# Validation Traceability

What this is: a traceability matrix from product/runtime claims to the
deterministic checks that protect them.

Run the full local check:

```bash
scripts/check
```

## Matrix

| Claim or feature | Risk guarded | Deterministic check | Source |
| --- | --- | --- | --- |
| Marketplace source points at `./plugins/promode-codex`. | Codex cannot discover or install the plugin from this marketplace repo. | `validate_marketplace()` in `validate-promode-codex.py --mode source`; plugin validator. | [../.agents/plugins/marketplace.json](../.agents/plugins/marketplace.json) |
| Installed plugin cache validation does not require source marketplace wrapper files. | A valid installed plugin reports a false failure for missing `.agents/plugins/marketplace.json`. | `validate_installed_cache_layout()` copies the plugin into a cache-shaped temp directory and runs the copied validator in auto mode. | [../plugins/promode-codex/scripts/validate-promode-codex.py](../plugins/promode-codex/scripts/validate-promode-codex.py) |
| Plugin manifest is Codex-specific and exposes skills from `./skills/`. | Claude-specific metadata leaks into Codex or skills are undiscoverable. | `validate_manifest()` in `validate-promode-codex.py`; plugin validator. | [../plugins/promode-codex/.codex-plugin/plugin.json](../plugins/promode-codex/.codex-plugin/plugin.json) |
| Plugin hooks are discoverable through `hooks/hooks.json`. | The main brief or drift check does not run when plugin hooks are supported. | `validate_hook()` checks bundled `SessionStart` commands. | [../plugins/promode-codex/hooks/hooks.json](../plugins/promode-codex/hooks/hooks.json) |
| Main-session Promode brief is injected by the hook. | Promode appears installed but the main agent does not receive methodology. | `validate_hook()` executes `promode-main-context.py` and checks JSON output. | [../plugins/promode-codex/hooks/promode-main-context.py](../plugins/promode-codex/hooks/promode-main-context.py) |
| Project install copies hooks and all seven Promode custom agents. | A target project has incomplete setup or missing delegated roles. | `validate_installer()` runs install into temporary projects. | [../plugins/promode-codex/scripts/install-project-agents.py](../plugins/promode-codex/scripts/install-project-agents.py) |
| Project install is idempotent and does not copy `PROMODE_CODEX_MAIN.md`. | Repeated setup duplicates hooks or creates stale project prompt copies. | `validate_installer()` runs install twice and checks hook counts plus stale brief removal. | [../plugins/promode-codex/scripts/install-project-agents.py](../plugins/promode-codex/scripts/install-project-agents.py) |
| Project-installed Promode agents warn when they drift. | Delegation uses stale or locally edited agent instructions without warning. | `validate_drift_hook_clean_project()` and `validate_drift_hook_warning()`. | [../plugins/promode-codex/hooks/promode-agent-drift.py](../plugins/promode-codex/hooks/promode-agent-drift.py) |
| Users are told to restart or resume after install/update. | Newly installed `.codex/agents/*.toml` roles are not exposed in the running session. | `validate_installer()` checks installer stdout for the restart/resume reminder. | [../plugins/promode-codex/scripts/install-project-agents.py](../plugins/promode-codex/scripts/install-project-agents.py) |
| Standard Promode custom agents exist and define required fields. | Subagent roles are missing or invalid. | `validate_agents()` parses all `standard/agents/promode_*.toml`. | [../plugins/promode-codex/standard/agents](../plugins/promode-codex/standard/agents) |
| Skills have valid frontmatter and repo skill structure. | Skills fail discovery or break plugin validation. | `validate_skills()` plus `developing-skills` repo validation. | [../plugins/promode-codex/skills](../plugins/promode-codex/skills) |
| This marketplace checkout treats root `/.codex/` as generated state. | Absolute local hook paths are accidentally committed. | `.gitignore` policy; `scripts/check` validates the policy in source mode. | [../.gitignore](../.gitignore) |
| Stale Claude Promode install leftovers are absent. | Claude Code sessions double-inject or mix runtime assumptions. | Source-mode stale setup checks in `validate-promode-codex.py`. | [PROJECT_FRAMING.md](PROJECT_FRAMING.md) |

## Gaps To Revisit

- Agent and skill validation still checks structure more than methodology. When
  agent contracts change, add focused assertions for role/reporting invariants.
- There is no CI workflow yet. `scripts/check` is the local deterministic entry
  point and should be the command wired into CI when this repo adds one.
