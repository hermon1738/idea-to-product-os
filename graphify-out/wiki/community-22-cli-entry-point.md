# CLI Entry Point

> Community 22 · 30 nodes · cohesion 0.07

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| main.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | code |
| branch() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | code |
| build() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | code |
| close_feature() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | code |
| close_phase() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | code |
| close_session() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | code |
| commit() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | code |
| context() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | code |
| new_project() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | code |
| next() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | code |
| pause() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | code |
| Bricklayer CLI entry point — wires typer commands to run_* handlers.  WHY THIS E | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | rationale |
| Create and checkout a brick/phase/feature branch with parent enforcement. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | rationale |
| Print brick contract, or run a build pipeline step with a flag. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | rationale |
| Print the single next CLI command to run based on state.json. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | rationale |
| Print session context from HANDOFF.json for session restart. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | rationale |
| Write HANDOFF.json and .continue-here.md for session handoff. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | rationale |
| Merge current phase/* branch into its parent feature/* branch. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | rationale |
| Merge current feature/* branch into main. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | rationale |
| Sprint review via Groq; write session-log.md and STATE.md. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | rationale |
| Print a compact context block for a project for AI session start. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | rationale |
| Scaffold a new project at context/projects/<name>/ with initial state files. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | rationale |
| Validate bricklayer.yaml and confirm all declared paths exist. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | rationale |
| Load and validate bricklayer.yaml; exits 1 on any failure.      Why it exists: T | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | rationale |
| Show current brick, last test result, and next action from state.json. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | rationale |
| Commit staged files with auto-tagged brick ID message. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | rationale |
| resume() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | code |
| run() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | code |
| status() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | code |
| _validate() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/main.py` | code |

## Key Relationships

- **main.py** `contains` → _validate() `[EXTRACTED]`
- **main.py** `contains` → status() `[EXTRACTED]`
- **main.py** `contains` → commit() `[EXTRACTED]`
- **branch()** `contains` → main.py `[EXTRACTED]`
- **branch()** `rationale_for` → Create and checkout a brick/phase/feature branch with parent enforcement. `[EXTRACTED]`
- **build()** `contains` → main.py `[EXTRACTED]`
- **build()** `rationale_for` → Print brick contract, or run a build pipeline step with a flag. `[EXTRACTED]`
- **close_feature()** `contains` → main.py `[EXTRACTED]`
- **close_feature()** `rationale_for` → Merge current feature/* branch into main. `[EXTRACTED]`
- **close_phase()** `contains` → main.py `[EXTRACTED]`
- **close_phase()** `rationale_for` → Merge current phase/* branch into its parent feature/* branch. `[EXTRACTED]`
- **close_session()** `contains` → main.py `[EXTRACTED]`
- **close_session()** `rationale_for` → Sprint review via Groq; write session-log.md and STATE.md. `[EXTRACTED]`
- **commit()** `contains` → main.py `[EXTRACTED]`
- **commit()** `rationale_for` → Commit staged files with auto-tagged brick ID message. `[EXTRACTED]`
- **context()** `contains` → main.py `[EXTRACTED]`
- **context()** `rationale_for` → Print a compact context block for a project for AI session start. `[EXTRACTED]`
- **new_project()** `contains` → main.py `[EXTRACTED]`
- **new_project()** `rationale_for` → Scaffold a new project at context/projects/<name>/ with initial state files. `[EXTRACTED]`
- **next()** `contains` → main.py `[EXTRACTED]`
- **next()** `rationale_for` → Print the single next CLI command to run based on state.json. `[EXTRACTED]`