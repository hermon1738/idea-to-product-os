# Context Files

These two files are the living memory of the system.
They are NOT static — they update after every session.

## How They Work

- `pipeline-status.md` — full snapshot of every component's current state.
  Session Scribe rewrites this after every `!scribe` command.

- `decision-log.md` — append-only history of every decision made.
  Session Scribe appends a new row after every `!scribe` command.

## Sync Workflow

After every session:
1. Run `!scribe` in Discord with your session summary
2. Session Scribe updates both files on the VPS at `~/ai-agents/docs/`
3. Copy the updated files from VPS back here:
   ```bash
   cat ~/ai-agents/docs/pipeline-status.md
   cat ~/ai-agents/docs/decision-log.md
   ```
4. Replace these files with the new content
5. Reload your AI project context

## Why This Matters

These files are what let you start a new session without re-explaining
your entire history. If they are stale, Claude starts cold.
If they are current, Claude knows exactly where you are in 30 seconds.

The files in this folder are snapshots — the VPS is the source of truth.
