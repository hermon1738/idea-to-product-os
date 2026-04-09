# Registry Module Tests

> Community 15 · 42 nodes · cohesion 0.07

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_registry.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| _make_malformed_registry() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| _make_registry() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| Tests for Brick 21 — agent registry module. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | rationale |
| Write a registry.yaml to tmp_path with the given agents. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | rationale |
| test_add_all_fields_persisted() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_add_atomic_write_leaves_no_tmp_file() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_add_creates_registry_dir_if_absent() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_add_duplicate_id_count_unchanged() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_add_duplicate_id_file_not_modified() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_add_duplicate_id_raises() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_add_increases_count() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_add_missing_field_error_names_field() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_add_missing_field_file_not_modified() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_add_missing_required_field_raises() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_add_valid_agent_appended() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_get_dispatcher_correct_trigger() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_get_formatter_correct_name() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_get_known_id_returns_dict() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_get_scribe_correct_name() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_get_scribe_correct_role() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_get_unknown_id_no_crash() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_get_unknown_id_returns_none() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_load_all_agents_have_live_status() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_load_all_required_fields_present() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_load_dispatcher_agent_present() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_load_empty_registry_returns_empty_list() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_load_formatter_agent_present() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_load_malformed_yaml_error_message() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| test_load_malformed_yaml_raises_value_error() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_registry.py` | code |
| *(+12 more)* | | |

## Key Relationships

- **test_registry.py** `contains` → _make_registry() `[EXTRACTED]`
- **test_registry.py** `contains` → _make_malformed_registry() `[EXTRACTED]`
- **test_registry.py** `contains` → test_load_returns_list() `[EXTRACTED]`
- **_make_malformed_registry()** `contains` → test_registry.py `[EXTRACTED]`
- **_make_malformed_registry()** `calls` → test_load_malformed_yaml_raises_value_error() `[INFERRED]`
- **_make_malformed_registry()** `calls` → test_load_malformed_yaml_error_message() `[INFERRED]`
- **_make_registry()** `contains` → test_registry.py `[EXTRACTED]`
- **_make_registry()** `calls` → test_load_empty_registry_returns_empty_list() `[INFERRED]`
- **_make_registry()** `calls` → test_get_unknown_id_returns_none() `[INFERRED]`
- **Tests for Brick 21 — agent registry module.** `rationale_for` → test_registry.py `[EXTRACTED]`
- **Write a registry.yaml to tmp_path with the given agents.** `rationale_for` → _make_registry() `[EXTRACTED]`
- **test_add_all_fields_persisted()** `contains` → test_registry.py `[EXTRACTED]`
- **test_add_all_fields_persisted()** `calls` → _make_registry() `[INFERRED]`
- **test_add_atomic_write_leaves_no_tmp_file()** `contains` → test_registry.py `[EXTRACTED]`
- **test_add_atomic_write_leaves_no_tmp_file()** `calls` → _make_registry() `[INFERRED]`
- **test_add_creates_registry_dir_if_absent()** `contains` → test_registry.py `[EXTRACTED]`
- **test_add_duplicate_id_count_unchanged()** `contains` → test_registry.py `[EXTRACTED]`
- **test_add_duplicate_id_count_unchanged()** `calls` → _make_registry() `[INFERRED]`
- **test_add_duplicate_id_file_not_modified()** `contains` → test_registry.py `[EXTRACTED]`
- **test_add_duplicate_id_file_not_modified()** `calls` → _make_registry() `[INFERRED]`