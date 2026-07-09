---
title: Promode for Codex opinion register
domain: promode-codex
category: methodology
status: stable
last_verified: 2026-07-09
tags:
  - promode
  - codex
  - opinions
  - agent-doctrine
sources:
  - title: Upstream Promode methodology opinion register
    kind: internal
    accessed: 2026-07-09
  - title: Promode for Codex activate skill and custom-agent templates
    kind: internal
    accessed: 2026-07-09
see_also:
  - ./index.md
---

# Promode for Codex opinion register

This is the project-local Promode for Codex opinion register. It is synced from
the plugin into `.codex/promode/docs/opinion-register.md` so copied project
custom agents can read the same doctrine without referencing the versioned
plugin cache.

The register is the stable vocabulary for Promode's preferences. Each clause in
the main-agent brief, custom-agent templates, setup skills, or methodology docs
should serve one or more opinions here. A clause with no supporting opinion is
a prompt-smell: either remove it or add the missing opinion deliberately.

This Codex register is compiled from the upstream Promode methodology and the
current Codex adaptation. It keeps the shared methodology recognizable while
replacing non-Codex harness assumptions with Codex-specific runtime facts.

## How agents use this register

- Read this file during orientation when present.
- Treat inline agent instructions as the execution contract for your role.
- Use opinion IDs when reporting methodology gaps, missing feedback loops,
  stale project docs, or proposed Promode changes.
- Do not edit synced project copies directly unless the task is explicitly to
  fork or customize that project-local doctrine. Normal changes belong in the
  plugin source followed by `$promode-codex:sync`.

## Meta and corpus governance

| id | statement | homes |
| --- | --- | --- |
| M0 `owner-preferences-root` | Promode is an opinionated development methodology: the main agent orchestrates and enforces the owner's preferences while subagents execute with matching doctrine. | activate skill, custom agents, this register |
| M1 `opinions-not-tutorials` | Promode prompts instill taste, constraints, and non-derivable doctrine; they do not teach the model generic software engineering. | custom agents, synced docs |
| M2 `principles-inline-where-load-bearing` | A critical rule must appear in the prompt surface an agent actually loads; a link alone does not carry load-bearing behavior. | activate skill, custom agents |
| M3 `rationale-travels-with-rule` | Keep the why with important rules so agents can apply them under pressure instead of pattern-matching shallow wording. | activate skill, register, custom agents |
| M4 `main-brief-main-agent-only` | Main orchestration doctrine belongs in the main-agent activation skill, not in `AGENTS.md` and not in subagent worker prompts. | activate skill |
| M5 `explicit-session-activation` | Codex Promode activation is explicit and session-scoped; the user invokes `$promode-codex:activate` when they want Promode behavior. | activate skill |
| M6 `explicit-project-sync` | Project-scoped custom agents and doctrine are installed by `$promode-codex:sync`; setup is deterministic and user-invoked. | sync skill, installer |
| M7 `no-plugin-cache-coupling` | Copied project agents must not depend on versioned plugin-cache paths. Shared doctrine is synced into `.codex/promode/docs/`. | sync skill, installer, custom agents |
| M8 `preserve-project-ownership` | `AGENTS.md` and non-Promode `.codex/` files are project-owned. Promode may guide or sync Promode-owned files, not silently rewrite project guidance. | sync skill, installer |
| M9 `no-voluntary-methodology-skills` | Methodology mechanics belong in role prompts and synced docs unless they are explicit command equivalents; avoid broad voluntary skill surfaces. | activate skill, sync skill, promode-audit, handoff, synced docs |

## Main-agent orchestration

| id | statement | homes |
| --- | --- | --- |
| O1 `main-agent-accountable` | The main agent owns outcomes: clarify, plan, decide, integrate, verify, and report. Delegation never transfers accountability. | activate skill |
| O2 `activation-authorizes-methodology` | Activating Promode is explicit session intent for the main agent to enforce Promode's workflow, including routine methodology-aligned delegation. Ask again only for unusual cost, permissions, external services, separate workspaces, or conflicts with stated user preference. | activate skill |
| O3 `critical-path-local` | Delegate bounded independent sidecar tasks while keeping the critical path and final decisions local to the main agent. | activate skill |
| O4 `plan-ownership-stays-local` | Subagents may provide evidence, options, or reviews; the main agent makes the plan and owns final trade-offs. | activate skill |
| O5 `one-dispatch-one-deliverable` | Every delegated task names scope, success criteria, exclusions, and the expected report. | activate skill |
| O6 `disjoint-write-scopes` | Parallel coding agents get non-overlapping write scopes and must not revert unrelated edits. | activate skill, senior engineer, fast worker |
| O7 `do-not-busy-poll` | Spawn, steer, wait only when blocked, and close agents; do not fill the main thread with polling noise. | activate skill |
| O8 `transcripts-unstable` | Codex transcript paths are convenience handles, not stable APIs. Use them only as best-effort evidence when accepted. | activate skill, analyzer |
| O9 `custom-agents-are-config-layers` | Codex custom agents tune spawned sessions; they are not hard security or isolation boundaries. | assumptions, custom agents |
| O10 `role-model-tiering` | The main orchestrating agent and CTO should run on GPT-5.5 for now. Specialist agents default to GPT-5.5, while fast-worker uses GPT-5.4-mini for mechanical work. | activate skill, custom agents |

## Shared working principles

| id | statement | homes |
| --- | --- | --- |
| P1 `evidence-over-assumptions` | Read the code, run the test, check the log; do not infer behavior from names. | activate skill, all agents |
| P2 `tdd-non-negotiable` | For code changes, write or identify a failing behavioral test before implementation whenever feasible. | activate skill, senior engineer, fast worker, code reviewer |
| P3 `tests-are-documentation` | Tests are executable behavioral documentation and outrank prose that claims different behavior. | activate skill, senior engineer, fast worker, code reviewer |
| P4 `always-explain-why` | Plans, prompts, tests, decisions, and reports preserve reasoning, not only steps. | activate skill, all agents |
| P5 `kiss-small-diffs` | Solve today's problem without speculative architecture or unrelated refactors. | activate skill, implementer, reviewer |
| P6 `crystallise-discovery` | Useful discovery becomes deterministic checks, scripts, maps, tests, or runbooks; it should not remain only prose. | activate skill, code reviewer, verifier, discovery-to-determinism doc |
| P7 `behavioral-authority` | Verified behavior controls: passing tests, failing tests, explicit specs, code, then external docs. | code reviewer, senior engineer, fast worker |
| P8 `stay-on-task-flag-rest` | Fix the assigned problem, flag adjacent issues for triage, and avoid opportunistic scope creep. | senior engineer, fast worker, debugger |

## Knowledge and memory

| id | statement | homes |
| --- | --- | --- |
| K1 `project-knowledge-graph` | Durable project knowledge belongs in the project-owned `AGENTS.md` graph and linked docs, not in chat history. | activate skill, custom agents |
| K2 `capture-effortful-discovery` | If substantial effort uncovered reusable commands, architecture facts, gotchas, or decisions, capture them where future agents will read them. | activate skill, custom agents |
| K3 `decision-nodes` | Hard-to-reverse or surprising decisions earn a node that records what was decided and why. | activate skill, senior engineer, chief technology officer, product design expert |
| K4 `runbooks-for-repeatable-ops` | Repeatable operational procedures, migrations, recoveries, and recurring incident classes belong in runbooks linked from `RUNBOOKS.md`. | activate skill, environment manager |
| K5 `one-idea-one-home` | Keep one canonical home for durable knowledge and link to it instead of forking prose across the corpus. | promode-audit, synced docs |

## Testing and verification

| id | statement | homes |
| --- | --- | --- |
| T1 `one-test-at-a-time` | Do not batch a pile of tests and then code. Drive one failing behavior to green, then continue. | senior engineer, fast worker |
| T2 `red-for-right-reason` | A new test must fail because the intended behavior is missing, not because of setup noise or a bad assertion. | senior engineer, fast worker |
| T3 `outside-in-behavior` | Prefer tests that express user-visible or externally observable behavior over implementation coupling. | senior engineer, fast worker, code reviewer |
| T4 `operator-seam-bulk-below-ui` | Keep most acceptance coverage below the GUI through a real operator seam; use the GUI tier only for behavior that manifests there. | activate skill, discovery-to-determinism doc, verifier |
| T5 `ui-tier-surgical` | Real GUI verification is slow and surgical. It verifies view wiring, rendering, navigation gates, and interaction defects, not logic already covered below UI. | activate skill, verifier |
| T6 `seam-changes-are-design` | Extending a shared operator seam can be implementation work; reshaping its boundary is an architectural decision for the parent agent. | senior engineer, fast worker, chief technology officer, activate skill |
| T7 `crystallised-failure-triage` | A failing deterministic check asks for classification first: flake, intended change, or regression. | activate skill, debugger, discovery-to-determinism doc |

## Debugging

| id | statement | homes |
| --- | --- | --- |
| D1 `fast-repro-first` | Build the fastest deterministic pass/fail signal before chasing fixes. Slow system tests verify; they are not the debugging loop. | debugger |
| D2 `ranked-falsifiable-hypotheses` | Generate ranked hypotheses with predictions before testing one variable at a time. | debugger |
| D3 `diagnose-or-fix` | Diagnosis and fixing are separate jobs unless the parent explicitly asks for both. | debugger, activate skill |
| D4 `prevention-is-part-of-finding` | A root-cause report should name what feedback loop would have caught the failure earlier. | debugger |

## Review and verification

| id | statement | homes |
| --- | --- | --- |
| R1 `two-axis-review` | Review spec fit and engineering standards as independent axes. | code reviewer |
| R2 `distrust-narration` | Commit messages, task docs, and summaries are claims; review the diff and tests directly. | code reviewer |
| R3 `reviewer-does-not-substitute-for-tests` | Reviewers inspect correctness, design, and test quality. They do not replace the implementer's test loop. | code reviewer, activate skill |
| R4 `crisp-verdicts` | Judging agents return clear verdicts such as APPROVED/REWORK or PASS/FAIL. | code reviewer, verifier |
| V1 `running-app-proof` | User-visible changes are verified by exercising real behavior from the outside when tests alone are insufficient. | verifier |
| V2 `prove-change-took-effect` | Before judging output, confirm the changed code or UI is actually the code or UI under test. | verifier |
| V3 `report-gaps` | Verification reports state what could not be verified and why. | verifier |

## Product and architecture

| id | statement | homes |
| --- | --- | --- |
| PD1 `skeptical-default` | Most feature requests are solutions looking for problems; challenge the problem, user, and need before adding surface area. | product design expert |
| PD2 `defaults-over-settings` | Prefer good defaults and constraints over extra configuration. | product design expert |
| PD3 `user-needs-are-claims` | Workflows and use cases are claims about real people; cite evidence or flag the assumption. | product design expert, activate skill |
| PD4 `traceability-hierarchy` | Significant work traces to goals, product framing, feature definitions, and behavioral tests. Missing traceability is a signal, not a paperwork gap. | activate skill |
| A1 `entity-model-highest-stakes` | Entity/domain model decisions are high leverage and expensive to unwind; treat them as hard-to-reverse. | chief technology officer, product design expert, activate skill |
| A2 `reversibility-weighted-depth` | Spend design depth on one-way doors; decide reversible details quickly and record the distinction when it matters. | chief technology officer, activate skill |

## Environment and run operations

| id | statement | homes |
| --- | --- | --- |
| E1 `environment-safety-envelope` | Check current state before changing services. Avoid destructive data, credential, or network-exposure actions unless explicitly scoped. | environment manager |
| E2 `reproducible-env-budget` | Bring-up, reset, and isolation determine the cost of reliable tests and verification. | environment manager |
| E3 `script-repeated-operations` | Repeated or complex environment procedures should become scripts or runbooks. | environment manager |

## Agent analysis

| id | statement | homes |
| --- | --- | --- |
| AN1 `notification-before-transcript` | The subagent result and final report usually come before transcript inspection; use transcripts only when needed. | analyzer |
| AN2 `testimony-not-evidence` | Agent self-report is testimony. Verify load-bearing claims against files, commands, diffs, tests, or bounded transcript inspection. | analyzer, activate skill |
| AN3 `divergence-is-finding` | A mismatch between what an agent says it did and what evidence shows is itself a useful methodology finding. | analyzer |

## Components as opinions

| id | statement | homes |
| --- | --- | --- |
| C1 `activate-skill` | Main-agent Promode activation earns a dedicated explicit skill because Codex lacks a reliable main-only ambient prompt path for this port. | activate skill |
| C2 `sync-skill` | Project custom agents and doctrine earn a deterministic sync skill because copied agents need stable project-local files. | sync skill |
| C3 `promode-custom-agents` | Dedicated custom agents are the Codex port's role-specific execution surface. | standard agents |
| C4 `discovery-to-determinism-doc` | Operator seams and UI state graphs are important enough to have their own reusable mechanics doc, routed by role prompts rather than exposed as a voluntary skill. | discovery-to-determinism doc, role prompts |
| C5 `promode-audit-skill` | Alignment with Promode doctrine is a separate command-equivalent audit job with concrete evidence, not a vague self-assessment. | promode-audit, auditor |
| C6 `handoff-skill` | Ephemeral session state earns a command-equivalent handoff skill so fresh agents can continue without turning chat history into project doctrine. | handoff |
