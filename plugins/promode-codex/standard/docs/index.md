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
