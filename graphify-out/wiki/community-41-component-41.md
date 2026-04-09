# Component 41

> Community 41 · 8 nodes · cohesion 0.32

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| close_feature.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_feature.py` | code |
| _get_current_branch() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_feature.py` | code |
| _merge_no_ff() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_feature.py` | code |
| Close-feature command: merge current feature/* branch into main.  WHY THIS EXIST | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_feature.py` | rationale |
| Merge current feature/* branch into main and clear feature context.      Enforce | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_feature.py` | rationale |
| Return the current git branch name, or None if git fails or is absent.      Why | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_feature.py` | rationale |
| Checkout target, merge branch with --no-ff, delete branch.      Why it exists: T | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_feature.py` | rationale |
| run_close_feature() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_feature.py` | code |

## Key Relationships

- **close_feature.py** `contains` → _get_current_branch() `[EXTRACTED]`
- **close_feature.py** `contains` → _merge_no_ff() `[EXTRACTED]`
- **close_feature.py** `contains` → run_close_feature() `[EXTRACTED]`
- **_get_current_branch()** `contains` → close_feature.py `[EXTRACTED]`
- **_get_current_branch()** `calls` → run_close_feature() `[INFERRED]`
- **_get_current_branch()** `rationale_for` → Return the current git branch name, or None if git fails or is absent.      Why `[EXTRACTED]`
- **_merge_no_ff()** `contains` → close_feature.py `[EXTRACTED]`
- **_merge_no_ff()** `calls` → run_close_feature() `[INFERRED]`
- **_merge_no_ff()** `rationale_for` → Checkout target, merge branch with --no-ff, delete branch.      Why it exists: T `[EXTRACTED]`
- **Close-feature command: merge current feature/* branch into main.  WHY THIS EXIST** `rationale_for` → close_feature.py `[EXTRACTED]`
- **Merge current feature/* branch into main and clear feature context.      Enforce** `rationale_for` → run_close_feature() `[EXTRACTED]`
- **Return the current git branch name, or None if git fails or is absent.      Why** `rationale_for` → _get_current_branch() `[EXTRACTED]`
- **Checkout target, merge branch with --no-ff, delete branch.      Why it exists: T** `rationale_for` → _merge_no_ff() `[EXTRACTED]`
- **run_close_feature()** `contains` → close_feature.py `[EXTRACTED]`
- **run_close_feature()** `calls` → _get_current_branch() `[INFERRED]`
- **run_close_feature()** `calls` → _merge_no_ff() `[INFERRED]`