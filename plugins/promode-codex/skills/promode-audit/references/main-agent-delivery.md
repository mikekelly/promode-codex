# Why the main-agent brief is delivered by a hook

Promode for Codex keeps main-agent orchestration out of `AGENTS.md`.

- `AGENTS.md` is the project's own file and the root of the agent-knowledge
  graph. It is useful to the main agent and subagents.
- `PROMODE_CODEX_MAIN.md` carries Promode's main-agent methodology and
  orchestration rules.
- Promode custom agents carry their own methodology in `.codex/agents/*.toml`.

## Why not AGENTS.md?

Main-agent orchestration says when to delegate, how to plan, and how to
synthesize work. That is wrong context for worker agents whose job is to execute
or review a bounded task.

Project knowledge should be shared. Orchestration should be scoped to the main
session. Therefore Promode uses a SessionStart hook for the main brief and
project custom-agent files for subagent behavior.

## Codex-specific delivery

Current Codex docs support plugin hooks, but this local harness reports
`plugin_hooks=false`. The reliable setup path here installs a project-local
`.codex/hooks.json` SessionStart hook pair. The project-local main hook reads
the bundled plugin brief through `PLUGIN_ROOT`; it does not install a project
copy of `PROMODE_CODEX_MAIN.md`.

The plugin also ships bundled hooks for Codex builds where plugin hooks are
enabled.
