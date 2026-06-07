# Verified Codex Assumptions

Checked against current Codex docs and the local Codex CLI on 2026-06-06.

## Plugin packaging

Codex plugins have `.codex-plugin/plugin.json` at plugin root. The root may also
include `skills/`, `hooks/`, `.mcp.json`, `.app.json`, and `assets/`.

If `hooks/hooks.json` exists, Codex discovers it by default when plugin hooks
are enabled; the manifest does not need an explicit `hooks` field.

Plugin-bundled hooks are non-managed hooks. Codex will list them but skip them
until the user reviews and trusts the current hook definition in `/hooks`.

The local harness checked during repo creation reported `hooks=true`,
`plugins=true`, and `plugin_hooks=false`. Therefore this plugin's reliable setup
path installs project-local `.codex/hooks.json` hooks and `.codex/hooks/`
scripts. The bundled plugin hooks remain as a forward-compatible path for Codex
builds where plugin hooks are enabled.

## Hook wire format

Command hooks receive one JSON object on stdin. Shared fields include:

- `hook_event_name`
- `session_id`
- `cwd`
- `transcript_path`
- `model`
- `permission_mode`

`SessionStart` adds `source`, with values `startup`, `resume`, `clear`, and
`compact`. JSON stdout may include:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "..."
  }
}
```

That text is added as extra developer context.

Promode uses one `SessionStart` hook to inject the main-session brief and a
separate `SessionStart` hook to warn when project-installed
`.codex/agents/promode_*.toml` files no longer match the plugin's
`standard/agents/promode_*.toml` files.

`SubagentStart` can add subagent-only developer context with the same
`hookSpecificOutput.additionalContext` shape and `hookEventName:
"SubagentStart"`.

`transcript_path` and `agent_transcript_path` are convenience fields. Codex docs
state that transcript format is not a stable hook interface.

## Custom agents

Project custom agents live in `.codex/agents/*.toml`; personal custom agents
live in `~/.codex/agents/*.toml`.

Required fields:

- `name`
- `description`
- `developer_instructions`

Optional settings can use normal Codex config keys such as `sandbox_mode`,
`model`, `model_reasoning_effort`, `mcp_servers`, and `skills.config`.

Subagents inherit parent runtime settings. Custom agents are config layers, not
hard security boundaries.

## Local CLI observations

`codex --help` exposes `exec`, `review`, `mcp`, `plugin`, `features`, `debug`,
and related commands. `codex plugin marketplace --help` exposes marketplace
`add`, `upgrade`, and `remove`. `codex features list` shows `multi_agent`,
`hooks`, and `plugins` enabled, with `plugin_hooks` disabled in this harness.
