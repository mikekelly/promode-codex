<required_reading>
Read before acting:
1. `sync.md`
2. `../references/codex-assumptions.md`
</required_reading>

<process>
Install is now the same operation as sync. Route to `workflows/sync.md` or
the dedicated `$promode-codex:sync` skill.
</process>

<success_criteria>
Installation is complete when the sync workflow has synced all Promode
custom-agent files plus `.codex/promode/docs/opinion-register.md`, removed
legacy Promode hook artifacts, preserved non-Promode project files, and told the
user to restart/resume then run `$promode-codex:activate`.
</success_criteria>
