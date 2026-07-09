# Promode for Codex

Promode for Codex makes Codex opinionated. It gives the main agent an
evidence-backed development methodology to enforce, so you describe the outcome
and Codex drives the work through framing, planning, implementation, review, and
verification without making you supervise the process.

Promode is designed around expensive, high-quality reasoning. GPT-5.6 Sol keeps
the whole picture: your intent, product goals, constraints, trade-offs, and final
judgement. Bounded exploration, implementation loops, tests, logs, and other
context-heavy work move to GPT-5.5 specialists or the GPT-5.4-mini fast worker.
Frontier context is spent where coherence matters; operational work gets fresh,
focused contexts.

The methodology is explicit rather than ambient. You activate it in sessions
where you want Promode, and the main agent then owns process, challenges
unsupported work, delegates bounded execution, reconciles every result, and
verifies the agreed outcome. Your project's `AGENTS.md` stays project-owned.

It is also deliberately transparent and forkable: four focused skills, eleven
custom-agent templates, a readable opinion register, and deterministic setup and
validation scripts. There are no services, MCP servers, or lifecycle hooks to
trust. Install this fork as-is if its taste fits, or change the opinions and make
it yours.

## Install From GitHub

Codex installs plugins from marketplace sources. This repository is the
marketplace; its `.agents/plugins/marketplace.json` points at the plugin payload
under `plugins/promode-codex/`.

### Codex CLI

```bash
codex plugin marketplace add mikekelly/promode-codex
codex plugin add promode-codex@promode-codex
```

Alternatively, add the marketplace, start `codex`, run `/plugins`, choose the
`promode-codex` marketplace, and install **Promode for Codex**. Start a new Codex
session after installation so its bundled skills are available.

### Codex desktop app

Add the marketplace with the CLI command above, restart the desktop app, open
**Plugins** from Codex, choose the `promode-codex` marketplace, and install
**Promode for Codex**. Start a new task after installation.

To pin a release or branch, add the marketplace with `--ref`:

```bash
codex plugin marketplace add mikekelly/promode-codex --ref <tag-or-branch>
```

## Set Up a Project

After installing and enabling the plugin:

1. Start a new task or session in the target project and run
   `$promode-codex:sync`.
2. Start another new task or session so Codex discovers the installed project
   custom agents. If the roles do not appear, restart Codex.
3. Run `$promode-codex:activate` in the new main-agent session.

`sync` installs or refreshes the eleven project-scoped Promode agents under
`.codex/agents/` and mirrors shared doctrine into `.codex/promode/docs/`. It
preserves non-Promode agents and hooks, prunes stale Promode-owned files, and
removes legacy Promode hook artifacts from older installations. It also warns
when the installed marketplace copy is older than the latest available release.

`activate` loads the main Promode brief for the current main-agent session.
Activation is explicit and session-scoped; run it at the start of every session
where you want Promode. Subagents use their own role instructions instead of the
main-agent orchestration brief.

Run `$promode-codex:promode-audit` after setup to assess the repository and get
a prioritised plan for bringing it into alignment with the methodology.

## The Problem It Solves

An unconfigured coding agent has no durable development taste. Every session can
re-litigate how much discovery is enough, when to test, what counts as done,
which decisions belong to the user, and where project knowledge should live.
Reusable skills help with individual workflows, but they still leave you to
remember when to invoke them and how to coordinate the whole delivery process.

Promode makes the main agent both orchestrator and methodology enforcer. It
clarifies the outcome, challenges features that lack evidence or a real goal,
keeps the plan coherent, delegates bounded work, reviews the evidence, and does
not call the job complete until the result is verified.

It also protects the main context. Long file reads, implementation churn, test
output, and GUI traversal can crowd out the goal and degrade judgement. Promode
keeps collaboration and final decisions in the main session while sending
operational work to fresh specialist contexts.

## Who It Is For

- **Codex project leads** who want the main agent to own process and momentum
  without giving up control over intent or consequential decisions.
- **Contributors and operators** who want predictable project-scoped agents and
  doctrine without losing project-owned Codex configuration.
- **Promode maintainers** who want shared methodology adapted to verified Codex
  behavior with deterministic checks against runtime drift.

The canonical [project framing](docs/PROJECT_FRAMING.md) records these jobs with
the product goals, risks, non-goals, and runtime boundaries they serve.

## How It Works

**The main agent orchestrates and decides.** It keeps the user conversation,
problem framing, plan ownership, synthesis, hard trade-offs, review of
load-bearing evidence, and final judgement.

**Subagents execute bounded jobs.** Exploration, implementation, debugging,
review, verification, environment work, and mechanical edits go to focused
roles with their own instructions and fresh context. Delegation never transfers
accountability: the main agent must inspect and integrate, reject, rework, or
explicitly defer every completed result.

**Model choice follows cognitive load.** The main orchestrator and the CTO role
use GPT-5.6 Sol with high reasoning when the surface makes it available.
Engineering, debugging, review, verification, audit, product, and knowledge
specialists use GPT-5.5. The fast worker uses GPT-5.4-mini for mechanical work
and UI driving. The CTO is reserved for prepared decisions that are materially
expensive to unwind, not merely large or cross-cutting tasks.

**Delivery is Codex-native.** The main orchestration brief lives in the explicit
`activate` skill rather than `AGENTS.md`. Project custom agents live under
`.codex/agents/`. Shared role doctrine is synced into `.codex/promode/docs/` so
copied agents do not depend on versioned plugin-cache paths. Codex transcript
paths remain convenience data, never a stable API.

### Agents

| Agent | Job |
| --- | --- |
| `promode_chief_technology_officer` | Prepared hard-to-reverse architecture, domain-model, technology, and large-refactor decisions |
| `promode_senior_engineer` | Complex or architecture-adjacent implementation through TDD |
| `promode_fast_worker` | Mechanical edits, straightforward tests, formatting, and GUI driving |
| `promode_code_reviewer` | Read-only correctness, regression, design, and test-quality review |
| `promode_debugger` | Evidence-led root-cause diagnosis and the fastest deterministic reproduction |
| `promode_verifier` | Outside-in running-behavior verification with a clear PASS or FAIL |
| `promode_environment_manager` | Development services, scripts, health checks, and repeatable environment operations |
| `promode_product_design_expert` | Product and UX decisions grounded in user evidence |
| `promode_agent_analyzer` | Agent-run evidence, failure classification, and recovery recommendations |
| `promode_auditor` | Repository methodology audit and prioritised improvement plan |
| `promode_constraint_reinforcer` | Hoist non-obvious, load-bearing constraints into agent orientation |

## The Opinions

Promode is opinionated on purpose. The canonical
[opinion register](plugins/promode-codex/standard/docs/opinion-register.md)
names every opinion, gives it a stable ID, and records which prompts, agents,
skills, or docs carry it.

- **Evidence over assumptions.** Read the code, run the check, inspect the
  result, and label unsupported claims.
- **Justification precedes implementation.** Significant work needs an observed
  problem, a real goal or risk link, falsifiable success, and explicit
  non-goals. Methodology alignment does not prove a feature should exist.
- **TDD is the default.** Establish one failing behavioral test for the right
  reason, make the smallest passing change, then refactor with tests green.
- **Tests are behavioral documentation.** Prefer public interfaces and
  user-visible outcomes over assertions coupled to implementation details.
- **Discovery becomes determinism.** Worthwhile findings become checks, tests,
  scripts, maps, recognizers, or runbooks instead of disappearing into chat.
- **Acceptance feedback stays fast.** Exercise most behavior below the GUI
  through an existing operator seam; reserve real UI verification for defects
  that only manifest there.
- **The main context is for coherence.** Delegate bulky operational work while
  keeping plan ownership, synthesis, and final judgement local.
- **Project knowledge is durable.** Keep reusable facts and constraints in the
  `AGENTS.md` knowledge graph, surprising decisions in decision records, and
  repeatable procedures in runbooks.
- **Verification is explicit.** State what ran, what passed, and what remains
  unverified; “looks right” is not done.

## Fork It

Methodology is taste. This repository is the `mikekelly` Codex fork: installing
it as-is means adopting these defaults, while forking it lets you change the
opinions, roles, and enforcement level to match your own way of working.

The opinion register is the customization map. Change an opinion in
`plugins/promode-codex/standard/docs/opinion-register.md`, update the homes named
by that row, run the repository checks, then use `$promode-codex:sync` to refresh
the project-local generated mirror. Do not edit `.codex/promode/docs/` directly;
it is generated setup state.

## Plugin Layout

- `.agents/plugins/marketplace.json` — marketplace catalog
- `plugins/promode-codex/.codex-plugin/plugin.json` — plugin manifest
- `plugins/promode-codex/skills/activate/` — explicit main-session activation
- `plugins/promode-codex/skills/sync/` — project custom-agent and doctrine sync
- `plugins/promode-codex/skills/promode-audit/` — methodology audit
- `plugins/promode-codex/skills/handoff/` — session handoff
- `plugins/promode-codex/standard/agents/` — eleven project custom-agent templates
- `plugins/promode-codex/standard/docs/` — synced Promode doctrine
- `plugins/promode-codex/scripts/` — setup and validation helpers

The marketplace entry points at the plugin with this shape:

```json
{
  "name": "promode-codex",
  "interface": {
    "displayName": "Promode for Codex"
  },
  "plugins": [
    {
      "name": "promode-codex",
      "source": {
        "source": "local",
        "path": "./plugins/promode-codex"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

## Develop From This Checkout

This checkout is already a repository marketplace. Open it as the Codex
project, then install **Promode for Codex** from the repo marketplace using the
desktop Plugins directory or the CLI `/plugins` browser. Start a new task or
session after installing or refreshing the plugin.

When testing project setup, run `$promode-codex:sync`, start another new task or
session, and then run `$promode-codex:activate`.

The helper below only syncs project custom agents and doctrine from this
checkout; it does not install or refresh the plugin itself:

```bash
python3 plugins/promode-codex/scripts/install-project-agents.py /path/to/project
```

Start a new task or session in that project afterward, then run
`$promode-codex:activate`. Use `--skip-upgrade-check` for deterministic local
validation or offline runs.

## Validate

Run the complete repository check:

```bash
scripts/check
```

The same command runs in GitHub Actions. It always runs the repo-owned source
validation. Codex-local plugin and skill validators run when their configured
paths are available and are skipped explicitly in hosted environments where
they are absent.

Component checks are also available:

```bash
python3 plugins/promode-codex/scripts/validate-promode-codex.py --mode source
python3 /Users/mike/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/promode-codex
```

From an installed plugin cache, use auto mode or `--mode package`; those modes
validate the plugin payload without requiring the source marketplace wrapper.

## Project Knowledge And Runbooks

- [Project framing](docs/PROJECT_FRAMING.md) — users/jobs, goals, risks,
  non-goals, and runtime boundaries
- [Decision index](docs/DECISIONS.md) — durable Codex adaptation decisions
- [Validation traceability](docs/TRACEABILITY.md) — product and runtime claims
  mapped to checks
- [Runbook hub](RUNBOOKS.md) — repeatable maintenance procedures

The Claude Code implementation lives in a separate repository. The
[alignment runbook](runbooks/check-promode-alignment.md) explains how maintainers
compare shared methodology without copying Claude-specific runtime behavior into
this Codex plugin.

## Sources Checked

This repository is tuned against current Codex documentation:

- [Build plugins](https://learn.chatgpt.com/docs/build-plugins)
- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

The exact verified assumptions are recorded in
`plugins/promode-codex/standard/docs/codex-assumptions.md`.
