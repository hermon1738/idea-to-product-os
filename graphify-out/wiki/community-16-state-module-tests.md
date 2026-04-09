# State Module Tests

> Community 16 · 37 nodes · cohesion 0.06

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_state.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | code |
| Tests for cli/state.py — state.json reader/writer. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| write() with a partial last_test_run dict deep-merges; sibling keys survive. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| write() with a state missing a required field raises ValueError. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| write() with state missing last_test_run raises ValueError. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| write() where loop_count is a string raises ValueError. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| write() where completed_bricks is not a list raises ValueError. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| load() auto-creates state.json even when parent directory does not exist.      m | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| load() returns a valid dict when state.json is missing but parent exists.      T | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| load() writes state.json to disk when it auto-creates.      The file must exist | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| Auto-created state derives project name from the repo root directory.      state | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| Auto-created state passes schema validation (i.e. load() can reload it).      En | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| Auto-create prints a warning to stderr naming the created path.      The message | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| Auto-created state has current_brick == '' (not null).      A null current_brick | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| Second load() on auto-created state reads from disk, no second warning.      Ens | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| load() returns dict with all required top-level fields. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| load() returns values matching what was written. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| write() merges a field update; reloading reflects the change. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| write() does not overwrite fields not in updates. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | rationale |
| test_load_autocreate_creates_file_on_disk() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | code |
| test_load_autocreate_default_current_brick_is_empty_string() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | code |
| test_load_autocreate_is_idempotent() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | code |
| test_load_autocreate_passes_schema_validation() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | code |
| test_load_autocreate_prints_warning_to_stderr() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | code |
| test_load_autocreate_project_name_from_repo_root() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | code |
| test_load_autocreate_returns_valid_dict() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | code |
| test_load_autocreate_with_missing_parent() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | code |
| test_load_returns_all_schema_fields() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | code |
| test_load_values_match() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | code |
| test_write_missing_last_test_run_raises() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_state.py` | code |
| *(+7 more)* | | |

## Key Relationships

- **test_state.py** `contains` → _write_state() `[EXTRACTED]`
- **test_state.py** `contains` → test_load_returns_all_schema_fields() `[EXTRACTED]`
- **test_state.py** `contains` → test_load_values_match() `[EXTRACTED]`
- **Tests for cli/state.py — state.json reader/writer.** `rationale_for` → test_state.py `[EXTRACTED]`
- **write() with a partial last_test_run dict deep-merges; sibling keys survive.** `rationale_for` → test_write_partial_nested_update_preserves_siblings() `[EXTRACTED]`
- **write() with a state missing a required field raises ValueError.** `rationale_for` → test_write_missing_required_field_raises() `[EXTRACTED]`
- **write() with state missing last_test_run raises ValueError.** `rationale_for` → test_write_missing_last_test_run_raises() `[EXTRACTED]`
- **write() where loop_count is a string raises ValueError.** `rationale_for` → test_write_wrong_type_loop_count_raises() `[EXTRACTED]`
- **write() where completed_bricks is not a list raises ValueError.** `rationale_for` → test_write_wrong_type_completed_bricks_raises() `[EXTRACTED]`
- **load() auto-creates state.json even when parent directory does not exist.      m** `rationale_for` → test_load_autocreate_with_missing_parent() `[EXTRACTED]`
- **load() returns a valid dict when state.json is missing but parent exists.      T** `rationale_for` → test_load_autocreate_returns_valid_dict() `[EXTRACTED]`
- **load() writes state.json to disk when it auto-creates.      The file must exist** `rationale_for` → test_load_autocreate_creates_file_on_disk() `[EXTRACTED]`