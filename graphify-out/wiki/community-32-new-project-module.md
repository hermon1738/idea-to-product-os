# New Project Module

> Community 32 · 12 nodes · cohesion 0.23

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| new_project.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/new_project.py` | code |
| _build_decision_log() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/new_project.py` | code |
| _build_state_json() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/new_project.py` | code |
| _build_state_md() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/new_project.py` | code |
| New-project command: scaffold context/projects/<name>/ with initial state files. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/new_project.py` | rationale |
| Build initial state.json content for a new project.      Args:         name: Pro | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/new_project.py` | rationale |
| Scaffold a new project directory with STATE.md, decision-log.md, state.json. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/new_project.py` | rationale |
| Return an error message if name is invalid, else None.      Why it exists: Centr | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/new_project.py` | rationale |
| Build initial STATE.md content for a new project.      Args:         name: Proje | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/new_project.py` | rationale |
| Build initial decision-log.md content for a new project.      Args:         name | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/new_project.py` | rationale |
| run_new_project() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/new_project.py` | code |
| _validate_name() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/new_project.py` | code |

## Key Relationships

- **new_project.py** `contains` → _validate_name() `[EXTRACTED]`
- **new_project.py** `contains` → _build_state_md() `[EXTRACTED]`
- **new_project.py** `contains` → _build_decision_log() `[EXTRACTED]`
- **_build_decision_log()** `contains` → new_project.py `[EXTRACTED]`
- **_build_decision_log()** `calls` → run_new_project() `[INFERRED]`
- **_build_decision_log()** `rationale_for` → Build initial decision-log.md content for a new project.      Args:         name `[EXTRACTED]`
- **_build_state_json()** `contains` → new_project.py `[EXTRACTED]`
- **_build_state_json()** `calls` → run_new_project() `[INFERRED]`
- **_build_state_json()** `rationale_for` → Build initial state.json content for a new project.      Args:         name: Pro `[EXTRACTED]`
- **_build_state_md()** `contains` → new_project.py `[EXTRACTED]`
- **_build_state_md()** `calls` → run_new_project() `[INFERRED]`
- **_build_state_md()** `rationale_for` → Build initial STATE.md content for a new project.      Args:         name: Proje `[EXTRACTED]`
- **New-project command: scaffold context/projects/<name>/ with initial state files.** `rationale_for` → new_project.py `[EXTRACTED]`
- **Build initial state.json content for a new project.      Args:         name: Pro** `rationale_for` → _build_state_json() `[EXTRACTED]`
- **Scaffold a new project directory with STATE.md, decision-log.md, state.json.** `rationale_for` → run_new_project() `[EXTRACTED]`
- **Return an error message if name is invalid, else None.      Why it exists: Centr** `rationale_for` → _validate_name() `[EXTRACTED]`
- **Build initial STATE.md content for a new project.      Args:         name: Proje** `rationale_for` → _build_state_md() `[EXTRACTED]`
- **Build initial decision-log.md content for a new project.      Args:         name** `rationale_for` → _build_decision_log() `[EXTRACTED]`