# Commit Module

> Community 33 · 12 nodes · cohesion 0.23

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| commit.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/commit.py` | code |
| _build_message() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/commit.py` | code |
| _check_staged() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/commit.py` | code |
| _do_commit() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/commit.py` | code |
| _parse_brick() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/commit.py` | code |
| Commit command: git commit wrapper with auto-tagged brick ID message.  WHY THIS | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/commit.py` | rationale |
| Build the full conventional-commit message string.      Why it exists: The messa | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/commit.py` | rationale |
| Run ``git commit -m <message>`` and return (exit_code, output).      Why it exis | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/commit.py` | rationale |
| Commit staged files with an auto-tagged brick ID conventional-commit message. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/commit.py` | rationale |
| Parse ``current_brick`` string into (brick_number, brick_name).      Why it exis | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/commit.py` | rationale |
| Return a list of staged file paths; empty list if nothing is staged or git fails | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/commit.py` | rationale |
| run_commit() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/commit.py` | code |

## Key Relationships

- **commit.py** `contains` → _parse_brick() `[EXTRACTED]`
- **commit.py** `contains` → _check_staged() `[EXTRACTED]`
- **commit.py** `contains` → _build_message() `[EXTRACTED]`
- **_build_message()** `contains` → commit.py `[EXTRACTED]`
- **_build_message()** `calls` → run_commit() `[INFERRED]`
- **_build_message()** `rationale_for` → Build the full conventional-commit message string.      Why it exists: The messa `[EXTRACTED]`
- **_check_staged()** `contains` → commit.py `[EXTRACTED]`
- **_check_staged()** `calls` → run_commit() `[INFERRED]`
- **_check_staged()** `rationale_for` → Return a list of staged file paths; empty list if nothing is staged or git fails `[EXTRACTED]`
- **_do_commit()** `contains` → commit.py `[EXTRACTED]`
- **_do_commit()** `calls` → run_commit() `[INFERRED]`
- **_do_commit()** `rationale_for` → Run ``git commit -m <message>`` and return (exit_code, output).      Why it exis `[EXTRACTED]`
- **_parse_brick()** `contains` → commit.py `[EXTRACTED]`
- **_parse_brick()** `calls` → run_commit() `[INFERRED]`
- **_parse_brick()** `rationale_for` → Parse ``current_brick`` string into (brick_number, brick_name).      Why it exis `[EXTRACTED]`
- **Commit command: git commit wrapper with auto-tagged brick ID message.  WHY THIS** `rationale_for` → commit.py `[EXTRACTED]`
- **Build the full conventional-commit message string.      Why it exists: The messa** `rationale_for` → _build_message() `[EXTRACTED]`
- **Run ``git commit -m <message>`` and return (exit_code, output).      Why it exis** `rationale_for` → _do_commit() `[EXTRACTED]`
- **Commit staged files with an auto-tagged brick ID conventional-commit message.** `rationale_for` → run_commit() `[EXTRACTED]`
- **Parse ``current_brick`` string into (brick_number, brick_name).      Why it exis** `rationale_for` → _parse_brick() `[EXTRACTED]`