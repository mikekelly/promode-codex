# Runbook: Check alignment with the Claude Code Promode repo

What this is: a repeatable check that `promode-codex` still reflects the shared
Promode methodology from the Claude Code `promode` repo while preserving the
Codex-specific runtime contract.

The goal is alignment, not mechanical parity. Shared methodology should stay
consistent. Runtime-specific delivery, hook behavior, agent format, install
flow, and tool assumptions must remain Codex-native.

## Source of truth

- Claude Code upstream: `../promode` by default, or `$PROMODE_REPO` when set.
- Codex adaptation: this repo, `promode-codex`.
- When both repos disagree, inspect commit history and docs before deciding
  whether Claude Promode changed the shared methodology or only changed
  Claude-specific mechanics.

## Setup

Run from the `promode-codex` repo:

```bash
CODEX_REPO="$(git rev-parse --show-toplevel)"
CODEX_PLUGIN_ROOT="$CODEX_REPO/plugins/promode-codex"
CLAUDE_REPO="${PROMODE_REPO:-$(cd "$CODEX_REPO/.." && pwd)/promode}"

git -C "$CODEX_REPO" status --short
git -C "$CLAUDE_REPO" status --short
git -C "$CODEX_REPO" rev-parse --short HEAD
git -C "$CLAUDE_REPO" rev-parse --short HEAD
```

If either worktree has unrelated changes, note that in the report and avoid
overwriting them. If the Claude repo is missing, clone or fetch it before doing
the alignment check.

## File map

Use this as the first-pass map. Re-run `find` or `rg --files` if either repo
has moved files.

| Shared concern | Claude Promode | Promode for Codex |
| --- | --- | --- |
| Main-agent methodology | `plugins/promode/PROMODE_MAIN_AGENT.md` | `plugins/promode-codex/standard/PROMODE_CODEX_MAIN.md` |
| Implementer | `plugins/promode/agents/implementer.md` | `plugins/promode-codex/standard/agents/promode_implementer.toml` |
| Reviewer | `plugins/promode/agents/code-reviewer.md` | `plugins/promode-codex/standard/agents/promode_reviewer.toml` |
| Debugger | `plugins/promode/agents/debugger.md` | `plugins/promode-codex/standard/agents/promode_debugger.toml` |
| Verifier | `plugins/promode/agents/verifier.md` | `plugins/promode-codex/standard/agents/promode_verifier.toml` |
| Environment manager | `plugins/promode/agents/environment-manager.md` | `plugins/promode-codex/standard/agents/promode_environment_manager.toml` |
| Product designer | `plugins/promode/agents/product-design-expert.md` | `plugins/promode-codex/standard/agents/promode_product_designer.toml` |
| Agent analyzer | `plugins/promode/agents/agent-analyzer.md` | `plugins/promode-codex/standard/agents/promode_agent_analyzer.toml` |
| Shared skills | `plugins/promode/skills/` | `plugins/promode-codex/skills/` |
| Hooks | `plugins/promode/hooks/` | `plugins/promode-codex/hooks/` and project-local `.codex/hooks/` installer output |
| Validation | `scripts/check-*.sh` | `plugins/promode-codex/scripts/validate-promode-codex.py` and plugin validator |
| Runbooks | `RUNBOOKS.md`, `runbooks/` | `RUNBOOKS.md`, `runbooks/` |

## Procedure

1. **Capture inventories.**

   ```bash
   find "$CLAUDE_REPO/plugins/promode/agents" -maxdepth 1 -type f | sort
   find "$CODEX_PLUGIN_ROOT/standard/agents" -maxdepth 1 -type f | sort
   find "$CLAUDE_REPO/plugins/promode/skills" -maxdepth 2 -type f | sort
   find "$CODEX_PLUGIN_ROOT/skills" -maxdepth 2 -type f | sort
   find "$CLAUDE_REPO/runbooks" -maxdepth 1 -type f | sort
   find "$CODEX_REPO/runbooks" -maxdepth 1 -type f | sort
   ```

2. **Compare main-agent methodology.**

   Read both main briefs. Check that shared Promode principles still agree:
   TDD as the default discipline, evidence over assumptions, discovery turning
   into deterministic checks, operator-seam testing, focused delegation,
   synthesis by the main agent, and durable runbook/knowledge capture.

   Do not copy Claude-specific hook chunking, Claude command names, transcript
   assumptions, or `.claude/` install paths into the Codex brief.

3. **Compare agent definitions by role.**

   For each mapped agent, compare intent, responsibilities, reporting contract,
   verification expectations, and shared principles. Keep Codex TOML structure
   and Codex custom-agent semantics; do not translate Claude frontmatter or
   model names blindly.

   Useful grep:

   ```bash
   rg -n "TDD|Evidence|operator seam|determin|runbook|delegate|verify|report" \
     "$CLAUDE_REPO/plugins/promode/agents" "$CODEX_PLUGIN_ROOT/standard/agents"
   ```

4. **Compare skills.**

   Shared skills should carry the same methodology unless Codex needs a runtime
   adaptation. Compare at least:

   - `discovery-to-determinism`
   - `handoff`
   - `promode-audit`
   - `recovering-subagents`

   Codex-only skills such as `managing-promode-codex` should be checked against
   Codex docs and local harness behavior, not against Claude plugin mechanics.
   Claude-only skills should be assessed explicitly: either port them, record
   why they are not applicable, or add a Codex-native equivalent.

5. **Compare hooks and install behavior by intent.**

   Claude and Codex hooks use different runtimes. Compare what they guarantee,
   not their implementation language:

   - main brief is injected only into the main session;
   - hook output stays within runtime limits;
   - users can review/trust hooks;
   - project-local install paths are reliable in the current harness;
   - Promode-owned project artifacts can be refreshed safely;
   - project-installed Codex agents are checked for drift.

6. **Compare docs and runbooks.**

   Check `README.md`, root guidance (`CLAUDE.md` vs `AGENTS.md`), and runbook
   hubs. If the Claude repo added a runbook for a recurring operation, decide
   whether `promode-codex` needs the same runbook, a Codex-native variant, or an
   explicit "not applicable" note.

7. **Update with Codex adaptation discipline.**

   When a shared methodology change is real, update every Codex home that
   carries it in the same change:

   - `plugins/promode-codex/standard/PROMODE_CODEX_MAIN.md`
   - relevant `plugins/promode-codex/standard/agents/promode_*.toml`
   - relevant `plugins/promode-codex/skills/*`
   - `README.md`, `AGENTS.md`, or runbooks if behavior changed
   - validation scripts when the invariant should be enforced

   Do not centralize load-bearing methodology into a link if Codex agents need
   it inline to behave correctly.

8. **Validate.**

   ```bash
   python3 plugins/promode-codex/scripts/validate-promode-codex.py
   python3 /Users/mike/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/promode-codex
   ```

   If skill files or runbooks changed, also run the available skill/repo
   validation:

   ```bash
   ruby /Users/mike/.agents/skills/developing-skills/scripts/validate-repo.rb .
   ```

## Report template

```markdown
# Promode Alignment Report - YYYY-MM-DD

Sources:
- promode: <branch> <sha>
- promode-codex: <branch> <sha>

## Summary
- Aligned:
- Needs Codex update:
- Claude-only, not applicable:
- Codex-only, intentionally divergent:

## Findings
1. <finding with file references>

## Changes Made
- <files changed>

## Validation
- <commands and results>

## Follow-ups
- <backlog items>
```

## See also

- Hub: [`../RUNBOOKS.md`](../RUNBOOKS.md)
- Codex assumptions: [`../plugins/promode-codex/skills/managing-promode-codex/references/codex-assumptions.md`](../plugins/promode-codex/skills/managing-promode-codex/references/codex-assumptions.md)
- Promode audit skill: [`../plugins/promode-codex/skills/promode-audit/SKILL.md`](../plugins/promode-codex/skills/promode-audit/SKILL.md)
