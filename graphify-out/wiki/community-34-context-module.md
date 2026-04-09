# Context Module

> Community 34 · 12 nodes · cohesion 0.23

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| context.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/context.py` | code |
| _load_project_state() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/context.py` | code |
| Context command: print a compact project context block for AI session start.  WH | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/context.py` | rationale |
| Extract "Next command:" value from STATE.md.      Why it exists: STATE.md is the | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/context.py` | rationale |
| Return the project name to use, reading bricklayer/state.json if needed.      Wh | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/context.py` | rationale |
| Print a compact context block for a project.      Why it exists: See module docs | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/context.py` | rationale |
| Load and parse state.json from a project directory.      Why it exists: Centrali | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/context.py` | rationale |
| Return the last n data rows from decision-log.md.      Why it exists: Only data | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/context.py` | rationale |
| _read_last_decisions() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/context.py` | code |
| _read_next_command() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/context.py` | code |
| _resolve_project_name() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/context.py` | code |
| run_context() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/context.py` | code |

## Key Relationships

- **context.py** `contains` → _load_project_state() `[EXTRACTED]`
- **context.py** `contains` → _read_last_decisions() `[EXTRACTED]`
- **context.py** `contains` → _read_next_command() `[EXTRACTED]`
- **_load_project_state()** `contains` → context.py `[EXTRACTED]`
- **_load_project_state()** `calls` → run_context() `[INFERRED]`
- **_load_project_state()** `rationale_for` → Load and parse state.json from a project directory.      Why it exists: Centrali `[EXTRACTED]`
- **Context command: print a compact project context block for AI session start.  WH** `rationale_for` → context.py `[EXTRACTED]`
- **Extract "Next command:" value from STATE.md.      Why it exists: STATE.md is the** `rationale_for` → _read_next_command() `[EXTRACTED]`
- **Return the project name to use, reading bricklayer/state.json if needed.      Wh** `rationale_for` → _resolve_project_name() `[EXTRACTED]`
- **Print a compact context block for a project.      Why it exists: See module docs** `rationale_for` → run_context() `[EXTRACTED]`
- **Load and parse state.json from a project directory.      Why it exists: Centrali** `rationale_for` → _load_project_state() `[EXTRACTED]`
- **Return the last n data rows from decision-log.md.      Why it exists: Only data** `rationale_for` → _read_last_decisions() `[EXTRACTED]`
- **_read_last_decisions()** `contains` → context.py `[EXTRACTED]`
- **_read_last_decisions()** `calls` → run_context() `[INFERRED]`
- **_read_last_decisions()** `rationale_for` → Return the last n data rows from decision-log.md.      Why it exists: Only data `[EXTRACTED]`
- **_read_next_command()** `contains` → context.py `[EXTRACTED]`
- **_read_next_command()** `calls` → run_context() `[INFERRED]`
- **_read_next_command()** `rationale_for` → Extract "Next command:" value from STATE.md.      Why it exists: STATE.md is the `[EXTRACTED]`