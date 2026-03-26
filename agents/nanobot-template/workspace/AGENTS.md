# Agent Instructions

<!-- FILL IN: Replace with specific behavior, trigger command, output format -->

## Job

__JOB_DESCRIPTION__

## Trigger

This agent responds to Discord commands prefixed with `!`.
Trigger command: `!__COMMAND__ __INPUT__`

## Output

__OUTPUT_DESCRIPTION__

## Hard Stops

- Never take irreversible actions without confirmation
- If input is ambiguous, ask one clarifying question before acting
- If a required file is missing, report the error and stop

## Heartbeat Tasks

`HEARTBEAT.md` is checked on the configured heartbeat interval.
Use file tools to manage periodic tasks.
Do NOT write to MEMORY.md for scheduled tasks.
