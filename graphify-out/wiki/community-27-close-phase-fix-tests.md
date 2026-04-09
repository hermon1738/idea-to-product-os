# Close Phase Fix Tests

> Community 27 · 18 nodes · cohesion 0.16

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_close_phase_fix.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | code |
| _git() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | code |
| _make_feature_repo() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | code |
| _make_phase_repo() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | code |
| Tests for Brick 26 fixes — null current_brick on close-phase/close-feature.  WHY | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | rationale |
| Initialise a temporary git repo checked out on a phase/* branch.      Sets up ma | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | rationale |
| Initialise a temporary git repo checked out on a feature/* branch.      Used for | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | rationale |
| close-phase with null current_brick exits 0 after a successful merge.      Befor | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | rationale |
| After close-phase, current_phase is None and current_brick is '' in state. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | rationale |
| close-phase with a valid string current_brick exits 0 (non-regression).      Ens | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | rationale |
| close-feature with null current_brick exits 0 after a successful merge.      Sam | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | rationale |
| After close-feature, current_feature/phase are None and current_brick is ''. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | rationale |
| Run a git command in ``cwd``, raise on non-zero exit code.      Why it exists: E | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | rationale |
| test_close_feature_null_current_brick_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | code |
| test_close_feature_null_current_brick_state_cleared() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | code |
| test_close_phase_null_current_brick_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | code |
| test_close_phase_null_current_brick_state_updated() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | code |
| test_close_phase_valid_current_brick_unchanged_behavior() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_phase_fix.py` | code |

## Key Relationships

- **test_close_phase_fix.py** `contains` → _git() `[EXTRACTED]`
- **test_close_phase_fix.py** `contains` → _make_phase_repo() `[EXTRACTED]`
- **test_close_phase_fix.py** `contains` → _make_feature_repo() `[EXTRACTED]`
- **_git()** `contains` → test_close_phase_fix.py `[EXTRACTED]`
- **_git()** `calls` → _make_phase_repo() `[INFERRED]`
- **_git()** `calls` → _make_feature_repo() `[INFERRED]`
- **_make_feature_repo()** `contains` → test_close_phase_fix.py `[EXTRACTED]`
- **_make_feature_repo()** `calls` → _git() `[INFERRED]`
- **_make_feature_repo()** `calls` → test_close_feature_null_current_brick_exits_zero() `[INFERRED]`
- **_make_phase_repo()** `contains` → test_close_phase_fix.py `[EXTRACTED]`
- **_make_phase_repo()** `calls` → _git() `[INFERRED]`
- **_make_phase_repo()** `calls` → test_close_phase_null_current_brick_exits_zero() `[INFERRED]`
- **Tests for Brick 26 fixes — null current_brick on close-phase/close-feature.  WHY** `rationale_for` → test_close_phase_fix.py `[EXTRACTED]`
- **Initialise a temporary git repo checked out on a phase/* branch.      Sets up ma** `rationale_for` → _make_phase_repo() `[EXTRACTED]`
- **Initialise a temporary git repo checked out on a feature/* branch.      Used for** `rationale_for` → _make_feature_repo() `[EXTRACTED]`
- **close-phase with null current_brick exits 0 after a successful merge.      Befor** `rationale_for` → test_close_phase_null_current_brick_exits_zero() `[EXTRACTED]`
- **After close-phase, current_phase is None and current_brick is '' in state.** `rationale_for` → test_close_phase_null_current_brick_state_updated() `[EXTRACTED]`
- **close-phase with a valid string current_brick exits 0 (non-regression).      Ens** `rationale_for` → test_close_phase_valid_current_brick_unchanged_behavior() `[EXTRACTED]`