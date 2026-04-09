# Build Command Tests

> Community 17 · 37 nodes · cohesion 0.07

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_build.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | code |
| _cli_invoke() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | code |
| Tests for cli/commands/build.py — bricklayer build (print contract). | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| parse_spec() extracts all 6 CONTRACT_FIELDS from a full spec. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| parse_spec() returns the correct content for each field. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| parse_spec() returns no GATE key (or empty string) when absent. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| parse_spec() returns empty string for a blank GATE section. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| run_build() returns 0 for a valid spec.md. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| run_build() prints all 6 field labels. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| run_build() returns 1 when GATE is absent. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| run_build() prints the no-gate message when GATE is absent. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| No raw Python traceback on missing Gate. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| run_build() returns 1 when GATE is present but blank. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| run_build() prints the no-gate message when GATE is blank. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| run_build() returns 1 when spec.md is absent. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| Error output mentions spec.md and contains no raw traceback. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| CliRunner: `bricklayer build` exits 0 for a valid spec.md. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| CliRunner: output contains all 6 field labels. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| CliRunner: `bricklayer build` exits 1 when GATE is absent. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| Write bricklayer/spec.md under tmp_path. Returns repo root. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | rationale |
| test_cli_runner_missing_gate_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | code |
| test_cli_runner_valid_spec_all_labels() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | code |
| test_cli_runner_valid_spec_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | code |
| test_parse_spec_empty_gate_returns_empty_string() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | code |
| test_parse_spec_missing_gate_returns_empty() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | code |
| test_parse_spec_returns_all_six_fields() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | code |
| test_parse_spec_values_match() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | code |
| test_run_build_empty_gate_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | code |
| test_run_build_empty_gate_prints_error() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | code |
| test_run_build_happy_path_all_six_labels() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build.py` | code |
| *(+7 more)* | | |

## Key Relationships

- **test_build.py** `contains` → _write_spec() `[EXTRACTED]`
- **test_build.py** `contains` → test_parse_spec_returns_all_six_fields() `[EXTRACTED]`
- **test_build.py** `contains` → test_parse_spec_values_match() `[EXTRACTED]`
- **_cli_invoke()** `contains` → test_build.py `[EXTRACTED]`
- **_cli_invoke()** `calls` → _write_spec() `[INFERRED]`
- **_cli_invoke()** `calls` → test_cli_runner_valid_spec_exits_zero() `[INFERRED]`
- **Tests for cli/commands/build.py — bricklayer build (print contract).** `rationale_for` → test_build.py `[EXTRACTED]`
- **parse_spec() extracts all 6 CONTRACT_FIELDS from a full spec.** `rationale_for` → test_parse_spec_returns_all_six_fields() `[EXTRACTED]`
- **parse_spec() returns the correct content for each field.** `rationale_for` → test_parse_spec_values_match() `[EXTRACTED]`
- **parse_spec() returns no GATE key (or empty string) when absent.** `rationale_for` → test_parse_spec_missing_gate_returns_empty() `[EXTRACTED]`
- **parse_spec() returns empty string for a blank GATE section.** `rationale_for` → test_parse_spec_empty_gate_returns_empty_string() `[EXTRACTED]`
- **run_build() returns 0 for a valid spec.md.** `rationale_for` → test_run_build_happy_path_exits_zero() `[EXTRACTED]`
- **run_build() prints all 6 field labels.** `rationale_for` → test_run_build_happy_path_all_six_labels() `[EXTRACTED]`
- **run_build() returns 1 when GATE is absent.** `rationale_for` → test_run_build_missing_gate_exits_one() `[EXTRACTED]`