<required_reading>
Read before acting:
1. `../references/codex-assumptions.md`
2. `../../../standard/PROMODE_CODEX_MAIN.md`
3. All files in `../../../standard/agents/`
</required_reading>

<process>
## Step 1: Verify Target Project

Check:
```bash
pwd
git status --short
```

If the project is not under git or has substantial unrelated changes, report the
risk before editing. Do not block on a dirty tree when the user clearly wants
setup in the current project; preserve unrelated changes.

## Step 2: Install Project Hook and Custom Agents

Use the helper when available:

```bash
python3 {plugin_root}/scripts/install-project-agents.py {project_path}
```

Or perform the equivalent manually:

Create `.codex/agents/` if needed. Copy these templates exactly from
`standard/agents/`:

- `promode_implementer.toml`
- `promode_reviewer.toml`
- `promode_debugger.toml`
- `promode_verifier.toml`
- `promode_environment_manager.toml`
- `promode_product_designer.toml`
- `promode_agent_analyzer.toml`

Overwrite only these Promode-owned files. Preserve every other file under
`.codex/agents/`.

Also copy:

- `hooks/promode-main-context.py` -> `.codex/hooks/promode-main-context.py`
- `hooks/promode-agent-drift.py` -> `.codex/hooks/promode-agent-drift.py`

Do not copy `standard/PROMODE_CODEX_MAIN.md` into the project. The main hook
receives `PLUGIN_ROOT` and reads the bundled plugin brief from there. If an
older install left `.codex/PROMODE_CODEX_MAIN.md` behind, remove that
Promode-owned stale file.

Merge these project hooks into `.codex/hooks.json`, preserving existing
non-Promode hooks:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "PLUGIN_ROOT={plugin_root_shell_quoted} python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/promode-main-context.py\"",
            "statusMessage": "Loading Promode for Codex"
          },
          {
            "type": "command",
            "command": "PLUGIN_ROOT={plugin_root_shell_quoted} python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/promode-agent-drift.py\"",
            "statusMessage": "Checking Promode project agents"
          }
        ]
      }
    ]
  }
}
```

## Step 3: Leave Project AGENTS.md Alone By Default

If `AGENTS.md` exists, do not edit it.

If `AGENTS.md` is missing, offer this optional scaffold and create it only if
the user agrees:

```markdown
# Agent Orientation

## Commands
- Test: {fill in}
- Lint/typecheck: {fill in}
- Dev server: {fill in}

## Structure
- {key directories and their purpose}

## Gotchas
- {non-obvious setup or project constraints}
```

## Step 4: Offer Optional Tracking Files

Offer to create missing `KANBAN_BOARD.md`, `IDEAS.md`, and `DONE.md`. Create
only missing files and only after user approval.

## Step 5: Explain Hook Trust and Session Refresh

The main Promode brief and project-agent drift check come from project-local
`SessionStart` hooks. The brief itself stays bundled in the plugin and is read
through `PLUGIN_ROOT`. Codex will skip non-managed hooks until the user reviews
and trusts them through `/hooks`. Tell the user to open `/hooks`, review the
project hooks, and trust them.

Also tell the user to restart Codex, resume the project thread, or start a fresh
session in the project after install. Newly installed `.codex/agents/*.toml`
files may not be exposed as custom-agent roles inside the already-running
thread, and `SessionStart` hooks only run on a new start/resume/clear/compact
event.

## Step 6: Verify

Check:
```bash
ls .codex/agents/promode_*.toml
ls .codex/hooks/promode-main-context.py .codex/hooks/promode-agent-drift.py .codex/hooks.json
```

When validating the plugin from this source marketplace repo, run:
```bash
python3 plugins/promode-codex/scripts/validate-promode-codex.py --mode source
```

When validating from an installed plugin cache, run the installed validator in
auto/default mode or package mode:
```bash
python3 {plugin_root}/scripts/validate-promode-codex.py
python3 {plugin_root}/scripts/validate-promode-codex.py --mode package
```
Installed plugin cache copies do not contain the source repo's
`.agents/plugins/marketplace.json`, so package validation must not require that
marketplace wrapper.

Then report installed files and any optional scaffolding performed.
</process>

<success_criteria>
Installation is complete when the project hooks exist, all seven
`.codex/agents/promode_*.toml` files exist, and the user has clear hook-trust
and restart/resume instructions. `.codex/PROMODE_CODEX_MAIN.md` should not be
installed.
</success_criteria>
