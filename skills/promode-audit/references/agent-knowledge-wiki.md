# Agent knowledge: an interlinked markdown graph rooted at AGENTS.md

Promode for Codex keeps durable project knowledge as a graph of linked markdown
docs rooted at the project's own `AGENTS.md`.

## AGENTS.md is the entry point

`AGENTS.md` is project-owned context that Codex reads for normal work and
subagents. It should be a launchpad, not a manual.

Keep only critical essentials inline: how to build, run, test, hard constraints,
and landmines an agent would fail or do harm without. Detailed subsystem
knowledge, product notes, QA notes, decisions, and runbooks should live in
linked docs.

Promode's main orchestration brief does not belong in `AGENTS.md`; it is
delivered by the Promode hook so subagents do not inherit main-agent
orchestration.

## Link densely

Knowledge files link to each other and back toward `AGENTS.md`. File location is
secondary; reachability is the structure. A doc reachable from nothing is
invisible.

## Capture rule

When an agent spends real effort uncovering reusable, undocumented knowledge a
future agent will need, write it as a linked doc and link it into the graph. Good
candidates include:

- non-obvious build or run steps
- API gotchas
- subsystem maps
- why a surprising design exists
- hard-to-reverse decisions and their rationale
- recurring operational procedures

Do not capture one-off trivia, obvious facts from code, or unverified guesses.

## Runbooks

A runbook is a node for repeatable procedures: deploys, releases, migrations,
environment bring-up/reset, recovery, or recurring incident classes. Link them
from a `RUNBOOKS.md` hub reachable from `AGENTS.md`. Prefer scripts for steps
that can be automated; the runbook captures judgment and links to scripts.

## Health checks

- Cold-readable: each doc opens by saying what it is.
- One idea, one home: state facts once and link.
- Compact root: `AGENTS.md` should stay small enough to help every agent.
- Distinct from `README.md`: README is human-facing; the knowledge graph is
  agent-facing operational context.
