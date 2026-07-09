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
| Plugin does not ship Promode lifecycle hooks. | Codex tries to auto-activate Promode through hook trust/reload paths. | `validate_manifest()` rejects legacy hook artifacts. | [../plugins/promode-codex/scripts/validate-promode-codex.py](../plugins/promode-codex/scripts/validate-promode-codex.py) |
| `$promode-codex:activate` is the canonical main-session brief and is explicit-only. | Promode appears installed but the main agent does not receive methodology, or a subagent implicitly loads main-agent orchestration. | `validate_activation_flow()` checks the activate skill carries the main brief contract and disables implicit invocation. | [../plugins/promode-codex/skills/activate/SKILL.md](../plugins/promode-codex/skills/activate/SKILL.md) |
| `$promode-codex:sync` syncs all eleven Promode custom agents. | A target project has incomplete setup or missing delegated roles. | `validate_installer()` runs the sync helper into temporary projects. | [../plugins/promode-codex/scripts/install-project-agents.py](../plugins/promode-codex/scripts/install-project-agents.py) |
| `$promode-codex:sync` syncs the Promode doctrine bundle into `.codex/promode/docs/`. | Copied custom agents reference unavailable plugin-cache files or lose shared opinion-register doctrine. | `validate_doctrine_bundle()`, `validate_agents()`, and `validate_installer()` check source docs, agent references, and installed project docs. | [../plugins/promode-codex/standard/docs/opinion-register.md](../plugins/promode-codex/standard/docs/opinion-register.md) |
| Project sync is idempotent, does not copy `PROMODE_CODEX_MAIN.md`, removes legacy Promode hooks, and prunes stale Promode-owned agent templates. | Repeated setup duplicates files, leaves stale hook activation in place, or leaves obsolete role names available. | `validate_installer()` runs the helper twice and checks stale artifact removal plus non-Promode hook and agent preservation. | [../plugins/promode-codex/scripts/install-project-agents.py](../plugins/promode-codex/scripts/install-project-agents.py) |
| Project sync warns when the plugin copy trails GitHub. | Users successfully sync project files but keep running an outdated plugin cache. | `validate_upgrade_check_parsing()` checks version parsing without making live network calls. | [../plugins/promode-codex/scripts/install-project-agents.py](../plugins/promode-codex/scripts/install-project-agents.py) |
| Users are told to restart/resume after sync and activate Promode per session. | Newly installed `.codex/agents/*.toml` roles are not exposed, or the user expects automatic activation. | `validate_installer()` checks installer stdout for the restart/resume and `$promode-codex:activate` reminders. | [../plugins/promode-codex/scripts/install-project-agents.py](../plugins/promode-codex/scripts/install-project-agents.py) |
| Standard Promode custom agents exist and define required fields. | Subagent roles are missing or invalid. | `validate_agents()` parses all `standard/agents/promode_*.toml`. | [../plugins/promode-codex/standard/agents](../plugins/promode-codex/standard/agents) |
| Only the command-equivalent/structural skills are exposed: `activate`, `sync`, `promode-audit`, and `handoff`. | Methodology docs become voluntary skills and drift from the Claude Promode surface. | `validate_skills()` rejects missing, extra, and forbidden exposed skills. | [../plugins/promode-codex/skills](../plugins/promode-codex/skills) |
| Pull requests and pushes run the repository check. | Contributors skip the local deterministic check before changing plugin behavior. | `.github/workflows/check.yml` runs `scripts/check`; source-mode validation checks the workflow is present. | [../.github/workflows/check.yml](../.github/workflows/check.yml) |
| This marketplace checkout treats root `/.codex/` as generated state. | Checkout-local Promode setup state is accidentally committed or generalized to user projects. | `.gitignore` policy; `scripts/check` validates the policy in source mode. | [../.gitignore](../.gitignore) |
| Stale Claude Promode install leftovers are absent. | Claude Code sessions double-inject or mix runtime assumptions. | Source-mode stale setup checks in `validate-promode-codex.py`. | [PROJECT_FRAMING.md](PROJECT_FRAMING.md) |

## Gaps To Revisit

- Agent and skill validation still checks structure more than methodology. When
  agent contracts change, add focused assertions for role/reporting invariants.
- Hosted CI skips Codex-local validators when their local skill paths are not
  present. If Codex exposes a portable plugin validator package, wire it into
  CI so hosted validation matches local validation more closely.
