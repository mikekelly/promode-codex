---
title: Promode for Codex doctrine bundle
domain: promode-codex
category: methodology
status: stable
last_verified: 2026-07-09
tags:
  - promode
  - codex
  - agent-doctrine
sources:
  - title: Promode for Codex plugin source
    kind: internal
    accessed: 2026-07-09
see_also:
  - ./opinion-register.md
  - ./codex-assumptions.md
  - ./main-agent-delivery.md
  - ./agent-knowledge-wiki.md
  - ./discovery-to-determinism.md
---

# Promode for Codex doctrine bundle

This directory is synced into target projects by `$promode-codex:sync` so
project-scoped Codex custom agents can read Promode doctrine without depending
on versioned plugin-cache paths.

Treat files under project `.codex/promode/docs/` as Promode-owned generated
artifacts. To change the doctrine, edit the plugin source or fork the plugin,
then run `$promode-codex:sync` again.

## Start here

- [Opinion register](./opinion-register.md) - the project-local register of
  Promode for Codex opinions that the main brief, custom agents, skills, and
  sync workflow instantiate.
- [Codex assumptions](./codex-assumptions.md) - verified Codex plugin, skill,
  custom-agent, activation, and sync runtime assumptions.
- [Main-agent delivery](./main-agent-delivery.md) - why Promode main-agent
  orchestration is explicit activation rather than project `AGENTS.md`.
- [Agent knowledge wiki](./agent-knowledge-wiki.md) - the AGENTS.md-rooted
  project knowledge graph model.
- [Discovery to determinism](./discovery-to-determinism.md) - operator-seam,
  headless-first acceptance, and UI state-graph doctrine.
- [Operator seam and agent tools](./operator-seam-and-agent-tools.md) -
  boundary between test seams and future agent surfaces.
- [UI state-graph EDT](./ui-state-graph-edt.md) - Explore, Distill, Traverse
  mechanics for surgical GUI verification.
