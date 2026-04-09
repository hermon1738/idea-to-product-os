# File Scope Verifier

> Community 35 · 11 nodes · cohesion 0.36

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| verify_files_touched.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/verify_files_touched.py` | code |
| build_snapshot() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/verify_files_touched.py` | code |
| has_git_repo() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/verify_files_touched.py` | code |
| main() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/verify_files_touched.py` | code |
| modified_files_git() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/verify_files_touched.py` | code |
| modified_files_snapshot() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/verify_files_touched.py` | code |
| parse_allowed_files() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/verify_files_touched.py` | code |
| read_snapshot() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/verify_files_touched.py` | code |
| sha256_for() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/verify_files_touched.py` | code |
| snapshot_target_files() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/verify_files_touched.py` | code |
| write_snapshot() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/verify_files_touched.py` | code |

## Key Relationships

- **verify_files_touched.py** `contains` → parse_allowed_files() `[EXTRACTED]`
- **verify_files_touched.py** `contains` → has_git_repo() `[EXTRACTED]`
- **verify_files_touched.py** `contains` → modified_files_git() `[EXTRACTED]`
- **build_snapshot()** `contains` → verify_files_touched.py `[EXTRACTED]`
- **build_snapshot()** `calls` → snapshot_target_files() `[INFERRED]`
- **build_snapshot()** `calls` → sha256_for() `[INFERRED]`
- **has_git_repo()** `contains` → verify_files_touched.py `[EXTRACTED]`
- **has_git_repo()** `calls` → main() `[INFERRED]`
- **main()** `contains` → verify_files_touched.py `[EXTRACTED]`
- **main()** `calls` → write_snapshot() `[INFERRED]`
- **main()** `calls` → parse_allowed_files() `[INFERRED]`
- **modified_files_git()** `contains` → verify_files_touched.py `[EXTRACTED]`
- **modified_files_git()** `calls` → main() `[INFERRED]`
- **modified_files_snapshot()** `contains` → verify_files_touched.py `[EXTRACTED]`
- **modified_files_snapshot()** `calls` → read_snapshot() `[INFERRED]`
- **modified_files_snapshot()** `calls` → build_snapshot() `[INFERRED]`
- **parse_allowed_files()** `contains` → verify_files_touched.py `[EXTRACTED]`
- **parse_allowed_files()** `calls` → main() `[INFERRED]`
- **read_snapshot()** `contains` → verify_files_touched.py `[EXTRACTED]`
- **read_snapshot()** `calls` → modified_files_snapshot() `[INFERRED]`
- **sha256_for()** `contains` → verify_files_touched.py `[EXTRACTED]`
- **sha256_for()** `calls` → build_snapshot() `[INFERRED]`
- **snapshot_target_files()** `contains` → verify_files_touched.py `[EXTRACTED]`
- **snapshot_target_files()** `calls` → build_snapshot() `[INFERRED]`