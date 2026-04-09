# Component 42

> Community 42 · 8 nodes · cohesion 0.32

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| close_phase.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_phase.py` | code |
| _get_current_branch() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_phase.py` | code |
| _merge_no_ff() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_phase.py` | code |
| Close-phase command: merge current phase/* branch into parent feature/* branch. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_phase.py` | rationale |
| Merge current phase/* branch into its parent feature/* branch.      Reads the me | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_phase.py` | rationale |
| Return the current git branch name, or None if git fails or is absent.      Why | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_phase.py` | rationale |
| Checkout target, merge branch with --no-ff, delete branch.      Why it exists: T | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_phase.py` | rationale |
| run_close_phase() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_phase.py` | code |

## Key Relationships

- **close_phase.py** `contains` → _get_current_branch() `[EXTRACTED]`
- **close_phase.py** `contains` → _merge_no_ff() `[EXTRACTED]`
- **close_phase.py** `contains` → run_close_phase() `[EXTRACTED]`
- **_get_current_branch()** `contains` → close_phase.py `[EXTRACTED]`
- **_get_current_branch()** `calls` → run_close_phase() `[INFERRED]`
- **_get_current_branch()** `rationale_for` → Return the current git branch name, or None if git fails or is absent.      Why `[EXTRACTED]`
- **_merge_no_ff()** `contains` → close_phase.py `[EXTRACTED]`
- **_merge_no_ff()** `calls` → run_close_phase() `[INFERRED]`
- **_merge_no_ff()** `rationale_for` → Checkout target, merge branch with --no-ff, delete branch.      Why it exists: T `[EXTRACTED]`
- **Close-phase command: merge current phase/* branch into parent feature/* branch.** `rationale_for` → close_phase.py `[EXTRACTED]`
- **Merge current phase/* branch into its parent feature/* branch.      Reads the me** `rationale_for` → run_close_phase() `[EXTRACTED]`
- **Return the current git branch name, or None if git fails or is absent.      Why** `rationale_for` → _get_current_branch() `[EXTRACTED]`
- **Checkout target, merge branch with --no-ff, delete branch.      Why it exists: T** `rationale_for` → _merge_no_ff() `[EXTRACTED]`
- **run_close_phase()** `contains` → close_phase.py `[EXTRACTED]`
- **run_close_phase()** `calls` → _get_current_branch() `[INFERRED]`
- **run_close_phase()** `calls` → _merge_no_ff() `[INFERRED]`