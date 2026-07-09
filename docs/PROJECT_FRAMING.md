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
- legacy hook-based Promode artifacts are removed during sync;
- Claude Code compatibility stays in the sibling `promode` repository.

## Goals

- Make Promode available to Codex users as an installable plugin.
- Keep the shared methodology recognizable while preserving Codex-specific
  runtime behavior.
- Give agents fast, deterministic checks for plugin shape, activation/sync
  behavior, custom-agent templates, and skill structure.
- Keep project guidance concise and link detailed knowledge from `AGENTS.md`.

## Risks And Priorities

- **Runtime drift:** Codex plugin, skill, and subagent semantics may change.
  Capture verified assumptions and validate the behavior this plugin relies on.
- **Claude leakage:** Claude-specific hook paths, chunking rules, or compatibility
  files must not become Codex plugin behavior.
- **Activation failure:** The main Promode brief must be easy to load into the
  current session without being copied into project `AGENTS.md`.
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
- Codex assumptions: [../plugins/promode-codex/skills/managing-promode-codex/references/codex-assumptions.md](../plugins/promode-codex/skills/managing-promode-codex/references/codex-assumptions.md)
