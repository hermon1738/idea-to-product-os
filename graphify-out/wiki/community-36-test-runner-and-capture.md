# Test Runner & Capture

> Community 36 · 10 nodes · cohesion 0.38

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| run_tests_and_capture.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/run_tests_and_capture.py` | code |
| append_handover() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/run_tests_and_capture.py` | code |
| detect_missing_tool_from_output() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/run_tests_and_capture.py` | code |
| extract_failed_nodeids() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/run_tests_and_capture.py` | code |
| load_state() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/run_tests_and_capture.py` | code |
| main() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/run_tests_and_capture.py` | code |
| parse_test_command() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/run_tests_and_capture.py` | code |
| run_command() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/run_tests_and_capture.py` | code |
| save_state() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/run_tests_and_capture.py` | code |
| short_reason() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/run_tests_and_capture.py` | code |

## Key Relationships

- **run_tests_and_capture.py** `contains` → load_state() `[EXTRACTED]`
- **run_tests_and_capture.py** `contains` → save_state() `[EXTRACTED]`
- **run_tests_and_capture.py** `contains` → parse_test_command() `[EXTRACTED]`
- **append_handover()** `contains` → run_tests_and_capture.py `[EXTRACTED]`
- **append_handover()** `calls` → main() `[INFERRED]`
- **detect_missing_tool_from_output()** `contains` → run_tests_and_capture.py `[EXTRACTED]`
- **detect_missing_tool_from_output()** `calls` → main() `[INFERRED]`
- **extract_failed_nodeids()** `contains` → run_tests_and_capture.py `[EXTRACTED]`
- **extract_failed_nodeids()** `calls` → main() `[INFERRED]`
- **load_state()** `contains` → run_tests_and_capture.py `[EXTRACTED]`
- **load_state()** `calls` → main() `[INFERRED]`
- **main()** `contains` → run_tests_and_capture.py `[EXTRACTED]`
- **main()** `calls` → load_state() `[INFERRED]`
- **main()** `calls` → parse_test_command() `[INFERRED]`
- **parse_test_command()** `contains` → run_tests_and_capture.py `[EXTRACTED]`
- **parse_test_command()** `calls` → main() `[INFERRED]`
- **run_command()** `contains` → run_tests_and_capture.py `[EXTRACTED]`
- **run_command()** `calls` → main() `[INFERRED]`
- **save_state()** `contains` → run_tests_and_capture.py `[EXTRACTED]`
- **save_state()** `calls` → main() `[INFERRED]`
- **short_reason()** `contains` → run_tests_and_capture.py `[EXTRACTED]`
- **short_reason()** `calls` → main() `[INFERRED]`