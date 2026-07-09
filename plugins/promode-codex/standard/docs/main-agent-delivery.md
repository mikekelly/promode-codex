# Why the main-agent brief is activated explicitly

Promode for Codex keeps main-agent orchestration out of `AGENTS.md`.

- `AGENTS.md` is the project's own file and the root of the agent-knowledge
  graph. It is useful to the main agent and subagents.
- `skills/activate/SKILL.md` carries Promode's main-agent methodology and
  orchestration rules.
- Promode custom agents carry role instructions in `.codex/agents/*.toml` and
  read shared Promode doctrine from `.codex/promode/docs/opinion-register.md`
  when it is present.

## Why not AGENTS.md?

Main-agent orchestration says when to delegate, how to plan, and how to
synthesize work. That is wrong context for worker agents whose job is to execute
or review a bounded task.

Project knowledge should be shared. Orchestration should be scoped to the main
session. Therefore Promode uses `$promode-codex:activate` for the main brief,
project custom-agent files for role behavior, and a synced project-local
opinion register for shared doctrine.

## Codex-specific delivery

Promode for Codex no longer installs main-session hooks by default. Hooks add
trust, reload, and plugin-runtime uncertainty that outweighs the convenience of
automatic startup activation in Codex.

The current setup is explicit:

1. `$promode-codex:sync` syncs custom-agent templates into `.codex/agents/`,
   syncs the doctrine bundle into `.codex/promode/docs/`, and removes legacy
   Promode hook artifacts.
2. `$promode-codex:activate` loads `skills/activate/SKILL.md` and makes Promode
   active for the current session.

Activation is session-scoped. Users should run it at the start of each Codex
session where they want Promode behavior.
