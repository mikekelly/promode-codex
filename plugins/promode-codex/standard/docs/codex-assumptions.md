# Verified Codex Assumptions

Checked against current Codex docs and the local Codex CLI on 2026-07-09.

## Plugin packaging

Codex plugins have `.codex-plugin/plugin.json` at plugin root. The root may
include `skills/`, `hooks/`, `.mcp.json`, `.app.json`, and `assets/`.

The source repository is a marketplace wrapper with
`.agents/plugins/marketplace.json` and `plugins/promode-codex/`. Installed plugin
cache copies contain only the plugin payload. Validators must not require the
source marketplace wrapper when they are run from an installed plugin cache.

Codex plugins can package skills, and skills can include scripts and references.
Promode for Codex uses the plugin as the distribution unit and skills as the
user-facing command surface.

Promode for Codex deliberately does not ship `hooks/hooks.json` and does not
install project-local main-session hooks by default. Users activate Promode
explicitly with `$promode-codex:activate` at the start of each session. This
avoids hook-trust and reload friction for the main-agent brief.

## Explicit activation

The main Promode brief lives directly in `skills/activate/SKILL.md`. When the
user invokes `$promode-codex:activate`, Codex reads that skill and the main
agent uses it as the current-session operating contract.

Do not copy the main brief into `AGENTS.md` or project `.codex/`. `AGENTS.md` is
project-owned durable guidance and is inherited by subagents, while the main
Promode brief is main-agent orchestration.

Activation is session-scoped. It is intentionally not automatic; the user runs
`$promode-codex:activate` when they want Promode behavior in a task or session.

The activate skill is main-agent-only. Both the activate and sync skills
include `agents/openai.yaml` with `allow_implicit_invocation: false` so Codex
does not choose them implicitly from a loose prompt. Explicit invocation still
works.

Codex supports `[[skills.config]]` with `enabled = false` to disable a skill by
`SKILL.md` path, and custom agent files may include `skills.config`. That is a
path-specific override, not a documented subagent-wide skill blacklist. Because
plugin cache paths are versioned, static Promode custom-agent templates cannot
reliably hard-code a disable entry for the activate skill.

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

Promode requires GPT-5.6 Sol (`gpt-5.6-sol`) with high reasoning effort for the
main orchestrating agent when the Codex surface makes it available. An activated
skill cannot switch the running main model or assume that exact model identity
is exposed to the agent. The main brief therefore states the requirement,
verifies it only when runtime metadata supports that check, and otherwise reports
the tier as unverified instead of claiming Sol is enabled.

Copied custom agents can select stable model IDs explicitly. The
`promode_chief_technology_officer` uses GPT-5.6 Sol with high reasoning for
bounded hard-to-reverse decisions. Other specialist agents use `gpt-5.5`, while
`promode_fast_worker` uses `gpt-5.4-mini`. Sol context is reserved for coherence,
synthesis, reversibility, and final judgment; operational work normally belongs
on the cheaper tiers.

After project custom agents are installed or refreshed, the already-running
Codex session may not expose those new role names immediately. This is a local
runtime observation rather than a documented reload guarantee. Tell users to
start a new task or session in the project; if the roles still do not appear,
restart Codex so it reloads `.codex/agents/*.toml`.

## Project-local doctrine bundle

Copied project custom agents must not rely on plugin-cache relative paths. The
installed plugin cache is versioned and may move when the marketplace upgrades.

`$promode-codex:sync` therefore mirrors Promode-owned doctrine docs from
`standard/docs/` into `.codex/promode/docs/`. Project custom agents read
`.codex/promode/docs/opinion-register.md` from the target project during
orientation when it is present. If the register is absent, agents continue from
their inline role instructions and report that `$promode-codex:sync` should be
run.

Treat `.codex/promode/docs/` as generated Promode-owned setup state. Do not
store unrelated project docs there.

## Legacy hook cleanup

Older Promode for Codex installs used project-local `SessionStart` hooks. The
current sync path removes these Promode-owned artifacts:

- `.codex/PROMODE_CODEX_MAIN.md`
- `.codex/hooks/promode-main-context.py`
- `.codex/hooks/promode-agent-drift.py`
- Promode hook commands inside `.codex/hooks.json`

The sync helper treats `.codex/agents/promode_*.toml` as Promode-owned
generated files. It copies the current bundled templates and prunes stale
Promode-prefixed templates from older versions. Non-Promode hooks and
non-Promode custom agents must be preserved.

## Upgrade awareness

After syncing project files, the sync helper performs a best-effort GitHub
check for a newer Promode for Codex version. It compares the local plugin
manifest version with stable upstream tags and the upstream main-branch plugin
manifest. This check is advisory only: network failures, missing tags, or
GitHub errors must not make project sync fail.

Offline and deterministic validation runs can pass `--skip-upgrade-check`.

## Local CLI observations

`codex --help` exposes `exec`, `review`, `mcp`, `plugin`, `features`, `debug`,
and related commands. `codex plugin marketplace --help` exposes marketplace
`add`, `upgrade`, and `remove`. Current local `codex features list` shows
`multi_agent`, `hooks`, and `plugins` enabled, with `plugin_hooks` removed and
false in this harness.
