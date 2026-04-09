# Config Loader Tests

> Community 18 · 35 nodes · cohesion 0.07

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_config.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | code |
| _make_file() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | code |
| Tests for cli/config.py — YAML loader, path validation, and .env loading. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | rationale |
| Error output must not contain 'Traceback'. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | rationale |
| All missing paths are reported, not just the first one. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | rationale |
| No bricklayer.yaml → human-readable message, exit 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | rationale |
| Missing yaml error must not include 'Traceback'. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | rationale |
| KEY=VALUE in .env is loaded into os.environ. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | rationale |
| .env absent → no error, no exception. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | rationale |
| Existing os.environ key is NOT overwritten by .env value. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | rationale |
| Malformed line (no '=') is skipped with warning; subsequent lines still load. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | rationale |
| llm: section present → correct values returned, no deprecation warning. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | rationale |
| llm: section absent → Groq defaults returned, deprecation warning on stderr. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | rationale |
| provider: openai → 'not yet supported' error, exit 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | rationale |
| Unsupported provider error must not show a Python traceback. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | rationale |
| All declared paths exist → load_and_validate returns config dict. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | rationale |
| Empty sections are valid — no files to check. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | rationale |
| One path declared but absent → human-readable error, exit 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | rationale |
| test_dotenv_absent_silent_skip() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | code |
| test_dotenv_does_not_overwrite_existing() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | code |
| test_dotenv_loads_key_value() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | code |
| test_dotenv_malformed_line_skips_with_warning_other_lines_load() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | code |
| test_happy_path_all_paths_valid() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | code |
| test_happy_path_empty_sections() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | code |
| test_llm_config_absent_uses_groq_defaults_with_warning() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | code |
| test_llm_config_present_no_deprecation_warning() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | code |
| test_llm_config_unsupported_provider_exits_1_with_message() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | code |
| test_llm_config_unsupported_provider_no_traceback() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | code |
| test_missing_path_no_traceback() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | code |
| test_missing_path_prints_error_and_exits() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_config.py` | code |
| *(+5 more)* | | |

## Key Relationships

- **test_config.py** `contains` → _write_yaml() `[EXTRACTED]`
- **test_config.py** `contains` → _make_file() `[EXTRACTED]`
- **test_config.py** `contains` → test_happy_path_all_paths_valid() `[EXTRACTED]`
- **_make_file()** `contains` → test_config.py `[EXTRACTED]`
- **_make_file()** `calls` → test_happy_path_all_paths_valid() `[INFERRED]`
- **Tests for cli/config.py — YAML loader, path validation, and .env loading.** `rationale_for` → test_config.py `[EXTRACTED]`
- **Error output must not contain 'Traceback'.** `rationale_for` → test_missing_path_no_traceback() `[EXTRACTED]`
- **All missing paths are reported, not just the first one.** `rationale_for` → test_multiple_missing_paths_all_reported() `[EXTRACTED]`
- **No bricklayer.yaml → human-readable message, exit 1.** `rationale_for` → test_missing_yaml_file_exits_with_message() `[EXTRACTED]`
- **Missing yaml error must not include 'Traceback'.** `rationale_for` → test_missing_yaml_no_traceback() `[EXTRACTED]`
- **KEY=VALUE in .env is loaded into os.environ.** `rationale_for` → test_dotenv_loads_key_value() `[EXTRACTED]`
- **.env absent → no error, no exception.** `rationale_for` → test_dotenv_absent_silent_skip() `[EXTRACTED]`
- **Existing os.environ key is NOT overwritten by .env value.** `rationale_for` → test_dotenv_does_not_overwrite_existing() `[EXTRACTED]`