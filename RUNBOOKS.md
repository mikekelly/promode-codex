# Runbooks

This is the runbook hub for the `promode-codex` repo. It links repeatable
maintenance procedures that future agents should not rediscover from scratch.

Each runbook lives under [`runbooks/`](runbooks/) and should be cold-readable:
state what it is for, which sources are authoritative, which files are touched,
and how to verify the work.

## Index

- [Check alignment with the Claude Code Promode repo](runbooks/check-promode-alignment.md) - compare
  the upstream Promode methodology, agent definitions, skills, hooks, docs, and
  runbooks against the Codex adaptation without copying Claude-specific runtime
  behavior into Codex.
