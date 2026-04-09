# Component 40

> Community 40 · 8 nodes · cohesion 0.32

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| resume.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/resume.py` | code |
| _format_block() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/resume.py` | code |
| _get_current_branch() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/resume.py` | code |
| Resume command: read HANDOFF.json and print a formatted session context block. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/resume.py` | rationale |
| Read HANDOFF.json and print a formatted session context block.      Validates al | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/resume.py` | rationale |
| Return the current git branch name, or None if git fails or is absent.      Why | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/resume.py` | rationale |
| Format the handoff dict into the resume context block string.      Why it exists | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/resume.py` | rationale |
| run_resume() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/resume.py` | code |

## Key Relationships

- **resume.py** `contains` → _get_current_branch() `[EXTRACTED]`
- **resume.py** `contains` → _format_block() `[EXTRACTED]`
- **resume.py** `contains` → run_resume() `[EXTRACTED]`
- **_format_block()** `contains` → resume.py `[EXTRACTED]`
- **_format_block()** `calls` → run_resume() `[INFERRED]`
- **_format_block()** `rationale_for` → Format the handoff dict into the resume context block string.      Why it exists `[EXTRACTED]`
- **_get_current_branch()** `contains` → resume.py `[EXTRACTED]`
- **_get_current_branch()** `calls` → run_resume() `[INFERRED]`
- **_get_current_branch()** `rationale_for` → Return the current git branch name, or None if git fails or is absent.      Why `[EXTRACTED]`
- **Resume command: read HANDOFF.json and print a formatted session context block.** `rationale_for` → resume.py `[EXTRACTED]`
- **Read HANDOFF.json and print a formatted session context block.      Validates al** `rationale_for` → run_resume() `[EXTRACTED]`
- **Return the current git branch name, or None if git fails or is absent.      Why** `rationale_for` → _get_current_branch() `[EXTRACTED]`
- **Format the handoff dict into the resume context block string.      Why it exists** `rationale_for` → _format_block() `[EXTRACTED]`
- **run_resume()** `contains` → resume.py `[EXTRACTED]`
- **run_resume()** `calls` → _format_block() `[INFERRED]`
- **run_resume()** `calls` → _get_current_branch() `[INFERRED]`