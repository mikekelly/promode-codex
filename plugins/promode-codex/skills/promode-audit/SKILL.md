---
name: promode-audit
description: "Audit how well a repository aligns with the Promode methodology in Codex. Use when the user asks to assess Promode alignment, audit a repo against Promode practices, improve tests, feedback loops, traceability, agent knowledge, runbooks, architecture, or bring a codebase into Promode shape."
---

<objective>
Run the Promode methodology audit and return a prioritised improvement plan.
This is the Codex command-equivalent surface for Claude Promode's
`/promode:promode-audit` command.
</objective>

<dispatch>
If `promode_auditor` is available and the user has explicitly authorized
Promode delegation or parallel agent work, dispatch it with:
- target repo, defaulting to the current repository;
- any focus supplied by the user;
- read-only instruction: do not modify, create, or commit files;
- required output: complete audit report, not a pointer to a file.

If delegation is not authorized or the auditor role is unavailable, run the
audit locally using the same rubric below. Do not silently spawn subagents.
</dispatch>

<rubric>
Start with a top-level framing gate:
- Locate the canonical statement of purpose, goals, risks or priorities, and
  non-goals. Check that these are concrete enough to judge proposed features.
- Intended users, personas, or role-based user groups and the user jobs or needs
  the product serves must be explicit. Repository type changes the vocabulary,
  not the requirement: a Codex plugin, library, CLI, or internal tool may use
  roles and jobs instead of fictional marketing personas, but it still needs an
  explicit account of who benefits and why.
- Trace intended users and jobs through goals and product framing into feature
  definitions and behavioral tests. Do not infer missing users, needs, or goals
  from implementation details, command names, or the opinion register.
- Inspect both `README.md` and `AGENTS.md` as root entrypoints. `README.md`
  should orient human readers to purpose, intended users or jobs, primary
  outcomes, and the canonical framing. `AGENTS.md` should give agents a concise
  route to canonical framing, goals, risks, non-goals, user or persona context,
  decisions, and runbooks without duplicating the full corpus.
- Check reachability, not merely file existence. Canonical framing that neither
  root entrypoint summarizes or links is an orientation defect.

Framing cannot be Green when goals are absent, intended users or jobs are
absent without an explicit evidence-backed rationale, or canonical framing is
unreachable from both root entrypoints. Missing both goals and users/jobs is a
high-priority framing failure and must not be averaged away by strong tests or
architecture.

Assess:
- Framing and traceability: intended users or jobs, goals, product framing,
  feature definitions, and tests link upward and explain why.
- Tests and feedback loops: behavioral tests, public interfaces, speed, determinism, one-command checks, operator seams, and UI-tier discipline.
- Agent knowledge and orientation: AGENTS.md concision, critical commands, linked durable knowledge, decisions, and runbooks.
- Architecture and navigability: module shape, testability, file size, coupling, naming, and dead code.
- Change hygiene: focused diffs, tests with code, rationale captured, and visible verification.

Also do setup pre-flight:
- `.codex/agents/promode_*.toml` and `.codex/promode/docs/opinion-register.md` are expected after `$promode-codex:sync`.
- `.codex/PROMODE_CODEX_MAIN.md`, `.codex/hooks/promode-main-context.py`, `.codex/hooks/promode-agent-drift.py`, and Promode entries in `.codex/hooks.json` are legacy Codex artifacts.
- `.claude/PROMODE_MAIN_AGENT.md`, `.claude/hooks/promode-main-context.sh`, or Promode SessionStart entries in `.claude/settings.json` are stale Claude leftovers for this Codex repo.
</rubric>

<references>
When present, use the synced doctrine bundle:
- `.codex/promode/docs/opinion-register.md`
- `.codex/promode/docs/agent-knowledge-wiki.md`
- `.codex/promode/docs/main-agent-delivery.md`
- `.codex/promode/docs/discovery-to-determinism.md`
</references>

<output_format>
```markdown
# Promode Methodology Audit - <repo>

## Overall alignment
<2-4 sentences. Dimension ratings: Framing <R> / Tests <R> / Knowledge <R> / Architecture <R> / Hygiene <R>>

## Setup notes
- <Codex setup status and stale artifact warnings>

## Framing gate
- Canonical framing: <path or missing>
- Goals, risks, and non-goals: <status and evidence>
- Intended users/personas and jobs: <status and evidence>
- README/AGENTS routing: <status and evidence>
- Framing rating cap: <none or reason>

## Findings by dimension
### <Dimension> - <rating>
- <finding with file evidence>

## Prioritised action plan
1. **[Now/Next/Later] <change>** - why it matters for Promode; effort S/M/L; suggested executor.
```
</output_format>
