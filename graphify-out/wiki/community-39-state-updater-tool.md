# State Updater Tool

> Community 39 · 8 nodes · cohesion 0.54

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| update_state.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/update_state.py` | code |
| append_handover() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/update_state.py` | code |
| complete_brick() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/update_state.py` | code |
| has_pass_verdict() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/update_state.py` | code |
| load_state() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/update_state.py` | code |
| main() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/update_state.py` | code |
| reject_completion() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/update_state.py` | code |
| save_state() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/update_state.py` | code |

## Key Relationships

- **update_state.py** `contains` → load_state() `[EXTRACTED]`
- **update_state.py** `contains` → save_state() `[EXTRACTED]`
- **update_state.py** `contains` → has_pass_verdict() `[EXTRACTED]`
- **append_handover()** `contains` → update_state.py `[EXTRACTED]`
- **append_handover()** `calls` → reject_completion() `[INFERRED]`
- **append_handover()** `calls` → complete_brick() `[INFERRED]`
- **complete_brick()** `contains` → update_state.py `[EXTRACTED]`
- **complete_brick()** `calls` → save_state() `[INFERRED]`
- **complete_brick()** `calls` → append_handover() `[INFERRED]`
- **has_pass_verdict()** `contains` → update_state.py `[EXTRACTED]`
- **has_pass_verdict()** `calls` → main() `[INFERRED]`
- **load_state()** `contains` → update_state.py `[EXTRACTED]`
- **load_state()** `calls` → main() `[INFERRED]`
- **main()** `contains` → update_state.py `[EXTRACTED]`
- **main()** `calls` → load_state() `[INFERRED]`
- **main()** `calls` → has_pass_verdict() `[INFERRED]`
- **reject_completion()** `contains` → update_state.py `[EXTRACTED]`
- **reject_completion()** `calls` → save_state() `[INFERRED]`
- **reject_completion()** `calls` → append_handover() `[INFERRED]`
- **save_state()** `contains` → update_state.py `[EXTRACTED]`
- **save_state()** `calls` → reject_completion() `[INFERRED]`
- **save_state()** `calls` → complete_brick() `[INFERRED]`