# Branch Module

> Community 38 · 10 nodes · cohesion 0.27

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| branch.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/branch.py` | code |
| _get_current_branch() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/branch.py` | code |
| _git_create_checkout() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/branch.py` | code |
| Branch command: create and checkout brick/phase/feature branches.  WHY THIS EXIS | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/branch.py` | rationale |
| Run ``git checkout -b <branch_name>`` and return (exit_code, output).      Why i | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/branch.py` | rationale |
| Create and checkout a branch at the correct hierarchy level.      Enforces the t | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/branch.py` | rationale |
| Convert a human-readable name to a lowercase-hyphenated git branch slug.      Wh | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/branch.py` | rationale |
| Return the current git branch name, or None if git fails or is absent.      Why | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/branch.py` | rationale |
| run_branch() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/branch.py` | code |
| _slugify() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/branch.py` | code |

## Key Relationships

- **branch.py** `contains` → _slugify() `[EXTRACTED]`
- **branch.py** `contains` → _get_current_branch() `[EXTRACTED]`
- **branch.py** `contains` → _git_create_checkout() `[EXTRACTED]`
- **_get_current_branch()** `contains` → branch.py `[EXTRACTED]`
- **_get_current_branch()** `calls` → run_branch() `[INFERRED]`
- **_get_current_branch()** `rationale_for` → Return the current git branch name, or None if git fails or is absent.      Why `[EXTRACTED]`
- **_git_create_checkout()** `contains` → branch.py `[EXTRACTED]`
- **_git_create_checkout()** `calls` → run_branch() `[INFERRED]`
- **_git_create_checkout()** `rationale_for` → Run ``git checkout -b <branch_name>`` and return (exit_code, output).      Why i `[EXTRACTED]`
- **Branch command: create and checkout brick/phase/feature branches.  WHY THIS EXIS** `rationale_for` → branch.py `[EXTRACTED]`
- **Run ``git checkout -b <branch_name>`` and return (exit_code, output).      Why i** `rationale_for` → _git_create_checkout() `[EXTRACTED]`
- **Create and checkout a branch at the correct hierarchy level.      Enforces the t** `rationale_for` → run_branch() `[EXTRACTED]`
- **Convert a human-readable name to a lowercase-hyphenated git branch slug.      Wh** `rationale_for` → _slugify() `[EXTRACTED]`
- **Return the current git branch name, or None if git fails or is absent.      Why** `rationale_for` → _get_current_branch() `[EXTRACTED]`
- **run_branch()** `contains` → branch.py `[EXTRACTED]`
- **run_branch()** `calls` → _get_current_branch() `[INFERRED]`
- **run_branch()** `calls` → _slugify() `[INFERRED]`
- **_slugify()** `contains` → branch.py `[EXTRACTED]`
- **_slugify()** `calls` → run_branch() `[INFERRED]`
- **_slugify()** `rationale_for` → Convert a human-readable name to a lowercase-hyphenated git branch slug.      Wh `[EXTRACTED]`