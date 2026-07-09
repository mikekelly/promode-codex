# Decision Index

What this is: durable Codex adaptation decisions for `promode-codex`. Each entry
records what was decided and why, so future changes do not rediscover or undo
runtime-specific choices accidentally.

## D1. Keep Codex And Claude Plugins Separate

Decision: this repository owns the Codex plugin marketplace and plugin payload.
The sibling `promode` repository owns Claude Code compatibility.

Why: the shared methodology is portable, but plugin packaging, agent files,
activation flow, worktree behavior, and transcript assumptions differ by
runtime.

Evidence:

- [../AGENTS.md](../AGENTS.md)
- [../README.md](../README.md)

## D2. Activate The Main Brief Explicitly, Not Through AGENTS.md

Decision: the main Promode brief lives directly in
`plugins/promode-codex/skills/activate/SKILL.md` and is loaded by
`$promode-codex:activate`. It is not copied into project `AGENTS.md` or
`.codex/`.

Why: `AGENTS.md` is project-owned durable guidance inherited by normal Codex
work and subagents. Main-agent orchestration should be scoped to the main
session, while subagents use their own custom-agent instructions. Explicit
activation avoids hook trust/reload friction and makes Promode's session scope
visible to the user.

Evidence:

- [../plugins/promode-codex/skills/activate/SKILL.md](../plugins/promode-codex/skills/activate/SKILL.md)
- [../plugins/promode-codex/skills/promode-audit/references/main-agent-delivery.md](../plugins/promode-codex/skills/promode-audit/references/main-agent-delivery.md)

## D3. Use Sync Skill For Project Agent Sync

Decision: `$promode-codex:sync` syncs Promode custom-agent templates into
target projects under `.codex/agents/`, syncs Promode doctrine into
`.codex/promode/docs/`, and removes legacy Promode hook artifacts from older
installs. It does not install main-session hooks by default.

Why: Codex plugins can package skills and skills can run deterministic scripts.
Custom agents are discovered from project/user `.codex/agents` files, while the
main brief can be activated explicitly per session. Copied custom agents need a
stable project-local doctrine path rather than a versioned plugin-cache path.

Evidence:

- [../plugins/promode-codex/skills/managing-promode-codex/references/codex-assumptions.md](../plugins/promode-codex/skills/managing-promode-codex/references/codex-assumptions.md)
- [../plugins/promode-codex/skills/sync/SKILL.md](../plugins/promode-codex/skills/sync/SKILL.md)
- [../plugins/promode-codex/scripts/install-project-agents.py](../plugins/promode-codex/scripts/install-project-agents.py)
- [../plugins/promode-codex/standard/docs/opinion-register.md](../plugins/promode-codex/standard/docs/opinion-register.md)

## D4. Restart Or Resume After Agent Install

Decision: sync workflows tell users to restart Codex, resume the project
thread, or start a fresh project session after installing or refreshing project
custom agents, then run `$promode-codex:activate` where they want Promode.

Why: a running Codex session may not expose newly installed `.codex/agents/*.toml`
role names until the project custom-agent inventory is reloaded.

Evidence:

- [../plugins/promode-codex/scripts/install-project-agents.py](../plugins/promode-codex/scripts/install-project-agents.py)
- [../plugins/promode-codex/skills/managing-promode-codex/workflows/sync.md](../plugins/promode-codex/skills/managing-promode-codex/workflows/sync.md)

## D5. Warn About Stale Plugin Copies, Do Not Self-Upgrade

Decision: after syncing project files, the sync helper performs a
best-effort GitHub version check and warns when the current plugin copy is older
than the latest available Promode for Codex version. The helper does not
auto-upgrade the plugin.

Why: project sync and plugin marketplace/cache management are separate
operations. The running plugin copy can safely advise the user, but Codex owns
marketplace upgrades and session reload behavior.

Evidence:

- [../plugins/promode-codex/scripts/install-project-agents.py](../plugins/promode-codex/scripts/install-project-agents.py)
- [../plugins/promode-codex/skills/sync/SKILL.md](../plugins/promode-codex/skills/sync/SKILL.md)

## D6. Treat Root /.codex As Generated In This Repo Only

Decision: this repository ignores its root `/.codex/` directory.

Why: in this marketplace checkout, `/.codex/` is generated local setup state and
contains generated local Promode setup state. The sync helper can regenerate
Promode-owned agent files and doctrine docs, and remove legacy hook artifacts.
This is not a
general policy for user projects; project-owned `.codex/` hooks, agents, and
config may be versioned elsewhere.

Evidence:

- [../.gitignore](../.gitignore)
- [../plugins/promode-codex/scripts/install-project-agents.py](../plugins/promode-codex/scripts/install-project-agents.py)

## D7. Treat Transcript Paths As Unstable

Decision: Promode for Codex treats transcript paths as convenience handles only,
not as stable APIs.

Why: Codex documentation does not guarantee transcript format stability, so
methodology and tooling should not depend on parsing transcripts unless the user
accepts best-effort behavior.

Evidence:

- [../plugins/promode-codex/skills/managing-promode-codex/references/codex-assumptions.md](../plugins/promode-codex/skills/managing-promode-codex/references/codex-assumptions.md)
- [../plugins/promode-codex/skills/recovering-subagents/SKILL.md](../plugins/promode-codex/skills/recovering-subagents/SKILL.md)
