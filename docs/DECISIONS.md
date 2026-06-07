# Decision Index

What this is: durable Codex adaptation decisions for `promode-codex`. Each entry
records what was decided and why, so future changes do not rediscover or undo
runtime-specific choices accidentally.

## D1. Keep Codex And Claude Plugins Separate

Decision: this repository owns the Codex plugin marketplace and plugin payload.
The sibling `promode` repository owns Claude Code compatibility.

Why: the shared methodology is portable, but hook formats, plugin packaging,
agent files, trust review, and transcript assumptions differ by runtime.

Evidence:

- [../AGENTS.md](../AGENTS.md)
- [../README.md](../README.md)

## D2. Deliver The Main Brief Through Hooks, Not AGENTS.md

Decision: `PROMODE_CODEX_MAIN.md` stays bundled under
`plugins/promode-codex/standard/` and is injected by `SessionStart` hooks.
It is not copied into project `AGENTS.md`.

Why: `AGENTS.md` is project-owned durable guidance inherited by normal Codex
work and subagents. Main-agent orchestration should be scoped to the main
session, while subagents use their own custom-agent instructions.

Evidence:

- [../plugins/promode-codex/standard/PROMODE_CODEX_MAIN.md](../plugins/promode-codex/standard/PROMODE_CODEX_MAIN.md)
- [../plugins/promode-codex/hooks/promode-main-context.py](../plugins/promode-codex/hooks/promode-main-context.py)
- [../plugins/promode-codex/skills/promode-audit/references/main-agent-delivery.md](../plugins/promode-codex/skills/promode-audit/references/main-agent-delivery.md)

## D3. Use Project-Local Hooks As The Reliable Install Path

Decision: setup installs `.codex/hooks.json` and `.codex/hooks/*.py` in target
projects. Plugin-bundled hooks remain for Codex builds where plugin hooks are
enabled.

Why: the local harness reports `plugin_hooks=false` while regular hooks are
enabled. Project-local hooks are therefore the reliable path today.

Evidence:

- [../plugins/promode-codex/skills/managing-promode-codex/references/codex-assumptions.md](../plugins/promode-codex/skills/managing-promode-codex/references/codex-assumptions.md)
- [../plugins/promode-codex/scripts/install-project-agents.py](../plugins/promode-codex/scripts/install-project-agents.py)

## D4. Restart Or Resume After Agent Install

Decision: install and update workflows tell users to restart Codex, resume the
project thread, or start a fresh project session after installing or refreshing
project custom agents.

Why: a running Codex session may not expose newly installed `.codex/agents/*.toml`
role names until the project custom-agent inventory is reloaded.

Evidence:

- [../plugins/promode-codex/scripts/install-project-agents.py](../plugins/promode-codex/scripts/install-project-agents.py)
- [../plugins/promode-codex/skills/managing-promode-codex/workflows/install.md](../plugins/promode-codex/skills/managing-promode-codex/workflows/install.md)
- [../plugins/promode-codex/skills/managing-promode-codex/workflows/update.md](../plugins/promode-codex/skills/managing-promode-codex/workflows/update.md)

## D5. Treat Root /.codex As Generated In This Repo Only

Decision: this repository ignores its root `/.codex/` directory.

Why: in this marketplace checkout, `/.codex/` is generated local setup state and
contains checkout-specific hook commands such as absolute `PLUGIN_ROOT` values.
The installer can regenerate it. This is not a general policy for user projects;
project-owned `.codex/` hooks, agents, and config may be versioned elsewhere.

Evidence:

- [../.gitignore](../.gitignore)
- [../plugins/promode-codex/scripts/install-project-agents.py](../plugins/promode-codex/scripts/install-project-agents.py)

## D6. Treat Transcript Paths As Unstable

Decision: Promode for Codex treats hook-provided transcript paths as convenience
handles only, not as stable APIs.

Why: Codex documentation does not guarantee transcript format stability, so
methodology and tooling should not depend on parsing transcripts unless the user
accepts best-effort behavior.

Evidence:

- [../plugins/promode-codex/skills/managing-promode-codex/references/codex-assumptions.md](../plugins/promode-codex/skills/managing-promode-codex/references/codex-assumptions.md)
- [../plugins/promode-codex/skills/recovering-subagents/SKILL.md](../plugins/promode-codex/skills/recovering-subagents/SKILL.md)
