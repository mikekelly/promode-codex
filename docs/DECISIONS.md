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
- [../plugins/promode-codex/standard/docs/main-agent-delivery.md](../plugins/promode-codex/standard/docs/main-agent-delivery.md)

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

- [../plugins/promode-codex/standard/docs/codex-assumptions.md](../plugins/promode-codex/standard/docs/codex-assumptions.md)
- [../plugins/promode-codex/skills/sync/SKILL.md](../plugins/promode-codex/skills/sync/SKILL.md)
- [../plugins/promode-codex/scripts/install-project-agents.py](../plugins/promode-codex/scripts/install-project-agents.py)
- [../plugins/promode-codex/standard/docs/opinion-register.md](../plugins/promode-codex/standard/docs/opinion-register.md)

## D4. Start A New Task Or Session After Agent Install

Decision: sync workflows tell users to start a new task or session after
installing or refreshing project custom agents. If the roles do not appear,
users restart Codex. They then run `$promode-codex:activate` where they want
Promode.

Why: a running Codex session may not expose newly installed `.codex/agents/*.toml`
role names until the project custom-agent inventory is reloaded. Public Codex
documentation defines the custom-agent paths but does not promise that resuming
an existing task reloads them, so the guidance uses a new session as the safe
boundary and labels restart as the fallback.

Evidence:

- [../plugins/promode-codex/scripts/install-project-agents.py](../plugins/promode-codex/scripts/install-project-agents.py)
- [../plugins/promode-codex/skills/sync/SKILL.md](../plugins/promode-codex/skills/sync/SKILL.md)

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

- [../plugins/promode-codex/standard/docs/codex-assumptions.md](../plugins/promode-codex/standard/docs/codex-assumptions.md)
- [../plugins/promode-codex/standard/agents/promode_agent_analyzer.toml](../plugins/promode-codex/standard/agents/promode_agent_analyzer.toml)

## D8. Keep The Codex Skill Surface Small

Decision: the Codex plugin exposes only four user-facing skills:
`activate`, `sync`, `promode-audit`, and `handoff`. `activate` and `sync` are
Codex delivery mechanics. `promode-audit` and `handoff` are explicit
command-equivalent workflows. Other Promode mechanics are delivered through
project-scoped custom-agent prompts and synced doctrine docs.

Why: methodology such as discovery-to-determinism and subagent recovery belongs
in role prompts and doctrine rather than optional user-invoked skills. Codex
still needs structural skills for activation and sync because plugins can
package skills but not directly install project custom-agent files.

Evidence:

- [../plugins/promode-codex/skills](../plugins/promode-codex/skills)
- [../plugins/promode-codex/standard/agents](../plugins/promode-codex/standard/agents)
- [../plugins/promode-codex/standard/docs/discovery-to-determinism.md](../plugins/promode-codex/standard/docs/discovery-to-determinism.md)
- [../plugins/promode-codex/scripts/validate-promode-codex.py](../plugins/promode-codex/scripts/validate-promode-codex.py)

## D9. Own Session Momentum Within Clarified Authority

Decision: after activation, the main agent takes control of the session's
workflow and momentum. It acts on clear, authorized in-scope steps inside the
agreed risk envelope, keeps minor steering non-blocking, and asks the user to
decide only significant forks affecting intent, scope, authority, external side
effects, or hard-to-reverse product and architecture choices.

Why: Promode makes the main agent accountable for outcomes. That accountability
is undermined when the user must repeatedly authorize routine mechanics or
manage orchestration. The boundary preserves user control over what is being
built while giving the main agent responsibility for moving agreed work
forward.

Evidence:

- [../plugins/promode-codex/skills/activate/SKILL.md](../plugins/promode-codex/skills/activate/SKILL.md)
- [../plugins/promode-codex/standard/docs/opinion-register.md](../plugins/promode-codex/standard/docs/opinion-register.md)
- [../plugins/promode-codex/skills/activate/evals/behavior.json](../plugins/promode-codex/skills/activate/evals/behavior.json)

## D10. Treat Subagent Completion As A State Transition

Decision: a completed subagent result becomes pending main-agent work. At the
next opportunity the main agent must integrate it, request rework, reject it, or
explicitly defer it with a reason and next action. User steering and side
questions do not implicitly cancel or erase the pending result.

Why: Codex collaboration is asynchronous. A completion notification can arrive
while the user is steering the main thread, so treating it as an informational
message allows the original flow to disappear between turns. Mandatory
reconciliation preserves continuity without forcing the user to supervise
delegation.

Evidence:

- [../plugins/promode-codex/skills/activate/SKILL.md](../plugins/promode-codex/skills/activate/SKILL.md)
- [../plugins/promode-codex/standard/docs/opinion-register.md](../plugins/promode-codex/standard/docs/opinion-register.md)
- [../plugins/promode-codex/skills/activate/evals/behavior.json](../plugins/promode-codex/skills/activate/evals/behavior.json)

## D11. Enforce Promode By Default And Require Feature Justification

Decision: activation puts the main agent in charge of process. The agent
actively enforces Promode rather than merely recommending it, and significant
features do not enter planning until they have an evidenced problem, an upward
goal or risk link, the smallest credible response, falsifiable success criteria,
and non-goals. Opinion alignment constrains the chosen solution but never
justifies the feature itself.

If the user explicitly chooses to diverge after the agent explains the relevant
reason, risk, or evidence gap, the agent respects that choice within the user's
authority, records what is being skipped, and continues without repeatedly
reopening the decision.

Why: Promode activation is an explicit opt-in to an opinionated methodology. A
main agent that yields process ownership by default makes activation ceremonial
and pushes enforcement back onto the user. At the same time, treating Promode's
own opinions as feature goals creates circular justification. Explicit
divergence preserves user authority without weakening the default contract.

Evidence:

- [../plugins/promode-codex/skills/activate/SKILL.md](../plugins/promode-codex/skills/activate/SKILL.md)
- [../plugins/promode-codex/standard/docs/opinion-register.md](../plugins/promode-codex/standard/docs/opinion-register.md)
- [../plugins/promode-codex/skills/activate/evals/behavior.json](../plugins/promode-codex/skills/activate/evals/behavior.json)

## D12. Reserve Sol For Coherence And Hard-To-Reverse Judgment

Decision: the main Promode session requires GPT-5.6 Sol with high reasoning when
the Codex surface makes it available. Sol is the coherence and final-judgment
tier: the main agent keeps problem framing, methodology enforcement, plan
ownership, synthesis, hard trade-offs, review of load-bearing evidence, and
final decisions. Bounded exploration, bulk reading, implementation loops, test
execution, logs, environment work, and GUI driving normally go to GPT-5.5
specialists or the GPT-5.4-mini fast worker.

The Sol CTO is reserved for one materially hard-to-reverse decision after
cheaper agents have prepared bounded evidence. Cross-cutting scope, reversible
critique, broad discovery, and operational execution do not qualify. Small work
stays local when delegation overhead would cost more context than the task.

Why: Sol's high reasoning maintains coherence across goals, constraints,
evidence, plans, and trade-offs, but that benefit is diluted when its context is
filled with operational detail. Reversibility is the relevant CTO gate; topic
breadth and file count are not. This also corrects the observed over-classifying
of a reversible prompt review as CTO work.

The activation skill cannot switch or reliably introspect the already-running
main model in every Codex surface. It states the required configuration, verifies
only when runtime metadata permits, and otherwise reports the tier as unverified
instead of making a false claim.

Evidence:

- [../plugins/promode-codex/skills/activate/SKILL.md](../plugins/promode-codex/skills/activate/SKILL.md)
- [../plugins/promode-codex/standard/agents/promode_chief_technology_officer.toml](../plugins/promode-codex/standard/agents/promode_chief_technology_officer.toml)
- [../plugins/promode-codex/standard/docs/codex-assumptions.md](../plugins/promode-codex/standard/docs/codex-assumptions.md)
- [../plugins/promode-codex/skills/activate/evals/behavior.json](../plugins/promode-codex/skills/activate/evals/behavior.json)

## D13. Gate Audits On Users, Jobs, Goals, And Framing Reachability

Decision: the Promode audit begins with a top-level framing gate. It requires
canonical purpose, goals, risks or priorities, non-goals, and intended users,
personas, or role-based audiences with their jobs or needs. Repository type may
change the vocabulary—a plugin or library can use roles and jobs rather than
fictional personas—but does not remove the need for explicit user grounding.

The audit also checks both root entrypoints. `README.md` orients human readers to
purpose, users/jobs, primary outcomes, and canonical framing. `AGENTS.md` gives
agents a concise route to the same canonical framing plus decisions and
runbooks. They link rather than duplicate the corpus. Framing cannot receive a
Green rating when goals or users/jobs are absent, or when canonical framing is
unreachable from both entrypoints.

Why: a prior audit failed to report that a repository had no documented goals
or personas. The old rubric named goals and AGENTS.md as broad dimensions but
did not make completeness or reachability an exit gate, so strong engineering
could hide a missing product foundation. Features cannot trace upward when
neither the beneficiary nor the desired outcome is documented.

Evidence:

- [../plugins/promode-codex/skills/promode-audit/SKILL.md](../plugins/promode-codex/skills/promode-audit/SKILL.md)
- [../plugins/promode-codex/standard/agents/promode_auditor.toml](../plugins/promode-codex/standard/agents/promode_auditor.toml)
- [../plugins/promode-codex/skills/promode-audit/evals/behavior.json](../plugins/promode-codex/skills/promode-audit/evals/behavior.json)
- [PROJECT_FRAMING.md](PROJECT_FRAMING.md)
