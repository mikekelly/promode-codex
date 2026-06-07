---
name: recovering-subagents
description: "Recover from failed, stalled, or unclear Codex subagent runs without over-reading unstable transcripts. Use when a Codex subagent failed, stalled, drifted, returned an insufficient result, or needs steering, closing, or a follow-up recovery prompt."
---

<core_rule>
Do not treat Codex transcript files as a stable API. Current Codex docs expose
`transcript_path` and `agent_transcript_path` for convenience, but explicitly
warn that transcript format may change. Prefer tool-visible agent status,
notifications, final messages, changed files, and explicit reported evidence.
</core_rule>

<recovery_process>
1. **Classify the state** - failed, stalled, drifted, insufficient summary, or
   completed but needs integration.
2. **Use stable surfaces first** - subagent id, final notification/result,
   status from available multi-agent tools, changed files listed by the agent,
   and parent prompt.
3. **Decide action**:
   - Stalled but useful: send a tighter steering prompt.
   - Failed due to scope: close and respawn with a smaller task.
   - Failed due to root cause uncertainty: dispatch `promode_debugger` if installed.
   - Completed but vague: ask for a concise follow-up summary with files,
     commands, and unresolved risk.
   - No longer needed: close the agent thread.
4. **Best-effort transcript read** - only if stable surfaces are insufficient
   and the user accepts best-effort analysis. Read narrow slices; never load a
   large transcript wholesale.
</recovery_process>

<codex_tools>
Use whatever Codex multi-agent controls are available in the current harness:
`wait_agent`, `send_input`, `resume_agent`, and `close_agent` when present. In
CLI sessions, `/agent` can switch between active agent threads.
</codex_tools>

<recovery_prompt_template>
Use a prompt like:

```text
You drifted from the assigned scope. Stop adjacent work. Report only:
1. What you completed, with file paths.
2. What failed or remains uncertain.
3. The single next action you recommend.
Do not make further edits unless explicitly asked.
```
</recovery_prompt_template>

<success_criteria>
Recovery is complete when the parent agent knows whether to integrate, steer,
respawn, dispatch a debugger/reviewer, or close the subagent. Do not keep
polling a stalled agent when a smaller replacement task would be clearer.
</success_criteria>
