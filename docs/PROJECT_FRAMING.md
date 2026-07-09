# Project Framing

What this is: product and runtime framing for the `promode-codex` repository.
It explains why the repository exists, what risks matter, and which work is out
of scope.

## Purpose

`promode-codex` packages the Promode methodology as a Codex-native plugin. The
repository is a Codex plugin marketplace source; the actual plugin payload lives
under `plugins/promode-codex/`.

The plugin adapts shared Promode practices to Codex's runtime:

- main-session guidance is activated explicitly with `$promode-codex:activate`,
  not stored in `AGENTS.md`;
- project-scoped custom agents are synced into `.codex/agents/` by
  `$promode-codex:sync`;
- copied custom agents read shared Promode doctrine from the synced
  `.codex/promode/docs/` bundle rather than plugin-cache paths;
- the exposed skill surface stays small: explicit activation, project sync,
  audit, and handoff;
- legacy hook-based Promode artifacts are removed during sync;
- Claude Code compatibility stays in the sibling `promode` repository.

## Intended Users And Jobs

These are role-based audiences rather than fictional named personas because the
product is a developer-tool plugin:

- **Codex project lead:** activate Promode for a session so the main agent owns
  process, challenges unsupported work, preserves coherence, delegates bounded
  execution, and verifies the agreed outcome.
- **Codex project contributor or operator:** install and sync the plugin into a
  project, understand its explicit activation model, and get predictable custom
  agents and project-local doctrine without losing project-owned configuration.
- **Promode for Codex maintainer:** adapt shared Promode doctrine to verified
  Codex runtime behavior, prevent Claude-specific assumptions from leaking in,
  and use deterministic checks to keep the package and methodology aligned.

## Goals

- Make Promode available to Codex users as an installable plugin.
- Keep the shared methodology recognizable while preserving Codex-specific
  runtime behavior.
- Give agents fast, deterministic checks for plugin shape, activation/sync
  behavior, custom-agent templates, and skill structure.
- Keep activated sessions moving through clear, authorized work without making
  the user manage routine orchestration, while preserving user control over
  intent and consequential decisions.
- Make activation an enforced methodology contract: the main agent owns process,
  challenges unjustified features, and respects explicit user divergence after
  explaining the consequence.
- Use GPT-5.6 Sol's high reasoning to preserve overall coherence while defending
  its costly context through bounded delegation of operational work.
- Make methodology audits expose missing goals, users/jobs, or cold-start routes
  to canonical framing instead of allowing engineering quality to hide product
  framing gaps.
- Keep project guidance concise and link detailed knowledge from `AGENTS.md`.

## Risks And Priorities

- **Runtime drift:** Codex plugin, skill, and subagent semantics may change.
  Capture verified assumptions and validate the behavior this plugin relies on.
- **Claude leakage:** Claude-specific hook paths, chunking rules, or compatibility
  files must not become Codex plugin behavior.
- **Activation failure:** The main Promode brief must be easy to load into the
  current session without being copied into project `AGENTS.md`.
- **Async flow loss:** User interjections can coincide with subagent completion.
  Completed results must remain pending work until the main agent explicitly
  reconciles them, rather than silently dropping the original flow.
- **Passive orchestration:** The main agent can turn minor choices into blocking
  questions and make the user drive execution. Activated sessions should act on
  clear steps inside the agreed risk envelope while escalating consequential
  forks.
- **Advisory methodology:** The main agent can describe Promode without enforcing
  it, allowing solution-first work to bypass justification, traceability, tests,
  review, or verification unless the user explicitly opts out.
- **Circular justification:** A feature can be treated as necessary merely
  because it aligns with an opinion. Opinions constrain solutions; evidenced
  project goals and risks justify whether work should exist.
- **Unverified main tier:** Activation cannot switch or always introspect the
  running main model. The agent must not claim Sol is enabled without runtime
  evidence, while the user-facing surface remains responsible for selecting it.
- **Sol context waste:** Bulk exploration, implementation loops, test runs, and
  reversible reviews can consume the expensive coherence tier. Keep judgment
  with Sol and move bounded operational work to cheaper agents.
- **CTO overuse:** Cross-cutting scope can be mistaken for irreversibility.
  Reserve the Sol CTO for one prepared decision that is materially expensive to
  unwind.
- **Framing blind spots:** A repository can have strong code and tests while no
  documented user, job, or goal explains why its features exist. Audits must
  fail this top-level gate and check that README and AGENTS entrypoints expose
  the canonical framing.
- **Custom-agent staleness:** Project-installed Promode agents can drift from the
  plugin templates and may not be visible until Codex reloads the session.
- **Doctrine drift:** Copied project agents need stable project-local doctrine;
  plugin-cache paths are versioned and should not be treated as durable
  subagent references.
- **Local setup confusion:** In this marketplace checkout, root `/.codex/` is
  generated local install state with checkout-specific paths. In normal user
  projects, `.codex/` may be project-owned and should not be ignored by default.

## Non-Goals

- Do not maintain Claude Code plugin compatibility here.
- Do not put Promode's main orchestration brief into a user's `AGENTS.md`.
- Do not parse Codex transcripts as a stable API.
- Do not create broad `.codex/` ignore guidance for user projects.

## Related Knowledge

- Decisions: [DECISIONS.md](DECISIONS.md)
- Validation traceability: [TRACEABILITY.md](TRACEABILITY.md)
- Runbooks: [../RUNBOOKS.md](../RUNBOOKS.md)
- Codex assumptions: [../plugins/promode-codex/standard/docs/codex-assumptions.md](../plugins/promode-codex/standard/docs/codex-assumptions.md)
