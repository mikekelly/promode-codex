---
name: promode-audit
description: "Audit how well a repository aligns with the Promode methodology in Codex, then produce a prioritised improvement plan. Use when the user asks to assess Promode alignment, audit a repo against Promode practices, improve tests, feedback loops, traceability, agent knowledge, runbooks, or architecture, or bring a codebase into Promode shape. Also flags stale Claude Promode install leftovers; use managing-promode-codex for Codex setup audits."
---

<objective>
Assess the repository's working practices against Promode: clear framing,
behavioral tests, fast feedback, useful agent knowledge, navigable architecture,
disciplined change hygiene, and reusable operational knowledge.
</objective>

<codex_delegation_policy>
Use Codex subagents only when the user has explicitly asked for Promode,
parallel assessors, delegation, or has approved your prompt to fan out the audit.
If delegation is not already authorized, ask for permission before spawning
assessors.

When subagents are allowed, use read-only assessors with narrow scopes. If
Promode custom agents are installed, use `promode_reviewer` for tests and
architecture dimensions; otherwise use built-in `explorer` or `default`.
</codex_delegation_policy>

<reference_index>
- `references/agent-knowledge-wiki.md` - Codex AGENTS.md-rooted knowledge graph model.
- `references/main-agent-delivery.md` - why Promode main-agent orchestration is hook-delivered.
</reference_index>

<process>
1. **Frame** - Skim `AGENTS.md` and `README` to understand stack, size, commands,
   and product purpose. If no `AGENTS.md` exists, note that as an orientation gap.
   Also do a setup pre-flight:
   - For Codex, `.codex/PROMODE_CODEX_MAIN.md`, `.codex/hooks.json`,
     `.codex/hooks/promode-main-context.py`,
     `.codex/hooks/promode-agent-drift.py`, and
     `.codex/agents/promode_*.toml` are expected after setup.
   - Flag stale Claude Promode leftovers (`.claude/PROMODE_MAIN_AGENT.md`,
     `.claude/hooks/promode-main-context.sh`, or a Promode SessionStart entry
     in `.claude/settings.json`) as warnings because they can double-inject
     Promode in Claude Code sessions.
2. **Choose dimensions** - Use the table below. Merge dimensions for a small
   library; split by subsystem for a large application.
3. **Gather evidence** - Do it locally or with approved parallel read-only
   subagents. Every finding needs concrete file/path evidence.
4. **Synthesize** - Prioritize across dimensions by impact on agent effectiveness
   and delivery risk.
5. **Report** - Produce the output format below and offer to turn actions into
   project tracking files if the user wants that.
</process>

<dimensions>
| Dimension | Assesses | Suggested Codex agent |
| --- | --- | --- |
| Framing and traceability | Goal/product/spec/test links; every layer explains why | `explorer` |
| Tests and feedback loops | Behavioral tests, public interfaces, speed, determinism, one-command checks, operator seams, UI-tier discipline | `promode_reviewer` or `explorer` |
| Agent knowledge and orientation | `AGENTS.md` concision, critical commands, links to durable knowledge, decisions, runbooks | `explorer` |
| Architecture and navigability | Module shape, testability, file size, coupling, naming, dead code | `promode_reviewer` |
| Change hygiene | Focused commits/PRs, tests with code, rationale captured | `explorer` |
</dimensions>

<rubrics>
## AGENTS.md Health

`AGENTS.md` should be concise, project-owned, and useful to every agent. Critical
commands and landmines belong inline. Detailed subsystem knowledge should be
linked, not pasted. Missing `AGENTS.md` is not fatal, but it usually weakens
agent orientation.

Durable knowledge should be a graph of linked markdown docs reachable from
`AGENTS.md`. Check for:
- subsystem orientation
- non-obvious build/run gotchas
- decisions with what/why
- runbooks for repeatable operational procedures such as deploys, migrations,
  environment bring-up, resets, recoveries, and recurring incident classes

Runbooks should link from a `RUNBOOKS.md` hub reachable from `AGENTS.md`, and
should prefer scripts where steps can be automated.

## Framing and Traceability

The repo should be self-describing top-down:

goals / risks / priorities -> marketing or product framing -> feature
definitions -> feature tests.

Each layer should explain why and link upward to a real goal. Broken traceability
is a diagnostic signal: the work may be unnecessary, the goal may be stale, or
the framing may be missing. Watch for goal sprawl and post-hoc justification.

## Layered Coverage

Where a UI sits over real logic, most acceptance coverage should run below the
UI through an operator seam. UI tests should be surgical: only behavior that
really requires the GUI. Discovery should harden into deterministic checks.

Flag slow UI tests that re-check logic a fast headless seam already covers or
could cover. Flag deterministic artifacts that fail imprecisely because they do
not tell the next agent where to re-discover.

## Feedback Loop Quality

An agent should be able to answer quickly: how do I run tests, what failed, what
changed, and what exact behavior is now covered? Slow or flaky feedback is a
methodology defect.

When a deterministic check fails, the repo should support triage: flake
(harden), intended change (re-crystallise), or regression (raise).
</rubrics>

<assessor_brief>
Give each assessor:
- Scope and dimension.
- Read-only instruction: do not modify, create, or commit files.
- Required output:
  - Rating: `Strong`, `Partial`, or `Weak`.
  - Findings with concrete file/path evidence.
  - Recommendations with effort `S`, `M`, or `L`.
  - The Promode principle each recommendation serves.
  - Any stale setup warnings, separately from methodology findings.
</assessor_brief>

<output_format>
```markdown
# Promode Methodology Audit - <repo>

## Overall alignment
<2-4 sentences. Dimension ratings: Framing <R> / Tests <R> / Knowledge <R> / Architecture <R> / Hygiene <R>>

## Setup notes
- <Codex setup status and any stale Claude Promode leftovers>

## Findings by dimension
### <Dimension> - <rating>
- <finding with file evidence>

## Prioritised action plan
1. **[Now/Next/Later] <change>** - why it matters for Promode; effort S/M/L; suggested executor.
```
</output_format>
