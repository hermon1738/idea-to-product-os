# Component 43

> Community 43 · 6 nodes · cohesion 0.33

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| runner.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/runner.py` | code |
| get_tool_path() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/runner.py` | code |
| Shared tool invocation and output capture for bricklayer build flags.  WHY THIS | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/runner.py` | rationale |
| Run ``python3 tool_path [args]`` and return (exit_code, combined_output).      W | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/runner.py` | rationale |
| Resolve a named tool entry from bricklayer.yaml config to an absolute Path. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/runner.py` | rationale |
| run_tool() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/runner.py` | code |

## Key Relationships

- **runner.py** `contains` → run_tool() `[EXTRACTED]`
- **runner.py** `contains` → get_tool_path() `[EXTRACTED]`
- **runner.py** `rationale_for` → Shared tool invocation and output capture for bricklayer build flags.  WHY THIS `[EXTRACTED]`
- **get_tool_path()** `contains` → runner.py `[EXTRACTED]`
- **get_tool_path()** `rationale_for` → Resolve a named tool entry from bricklayer.yaml config to an absolute Path. `[EXTRACTED]`
- **Shared tool invocation and output capture for bricklayer build flags.  WHY THIS** `rationale_for` → runner.py `[EXTRACTED]`
- **Run ``python3 tool_path [args]`` and return (exit_code, combined_output).      W** `rationale_for` → run_tool() `[EXTRACTED]`
- **Resolve a named tool entry from bricklayer.yaml config to an absolute Path.** `rationale_for` → get_tool_path() `[EXTRACTED]`
- **run_tool()** `contains` → runner.py `[EXTRACTED]`
- **run_tool()** `rationale_for` → Run ``python3 tool_path [args]`` and return (exit_code, combined_output).      W `[EXTRACTED]`