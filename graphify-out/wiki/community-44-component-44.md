# Component 44

> Community 44 · 6 nodes · cohesion 0.40

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| status.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/status.py` | code |
| _parse_state_md() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/status.py` | code |
| Status command: print current brick, last test result, and next action.  WHY THI | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/status.py` | rationale |
| Parse STATE.md into a key → value dict.      Why it exists: run_status needs pro | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/status.py` | rationale |
| Print five pipeline status fields to stdout.      Combines data from state.json | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/status.py` | rationale |
| run_status() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/status.py` | code |

## Key Relationships

- **status.py** `contains` → _parse_state_md() `[EXTRACTED]`
- **status.py** `contains` → run_status() `[EXTRACTED]`
- **status.py** `rationale_for` → Status command: print current brick, last test result, and next action.  WHY THI `[EXTRACTED]`
- **_parse_state_md()** `contains` → status.py `[EXTRACTED]`
- **_parse_state_md()** `calls` → run_status() `[INFERRED]`
- **_parse_state_md()** `rationale_for` → Parse STATE.md into a key → value dict.      Why it exists: run_status needs pro `[EXTRACTED]`
- **Status command: print current brick, last test result, and next action.  WHY THI** `rationale_for` → status.py `[EXTRACTED]`
- **Parse STATE.md into a key → value dict.      Why it exists: run_status needs pro** `rationale_for` → _parse_state_md() `[EXTRACTED]`
- **Print five pipeline status fields to stdout.      Combines data from state.json** `rationale_for` → run_status() `[EXTRACTED]`
- **run_status()** `contains` → status.py `[EXTRACTED]`
- **run_status()** `calls` → _parse_state_md() `[INFERRED]`
- **run_status()** `rationale_for` → Print five pipeline status fields to stdout.      Combines data from state.json `[EXTRACTED]`