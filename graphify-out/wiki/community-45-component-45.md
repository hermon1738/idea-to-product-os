# Component 45

> Community 45 · 4 nodes · cohesion 0.50

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| next.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/next.py` | code |
| Next command: read next_action from state.json and print the next CLI command. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/next.py` | rationale |
| Read next_action from state.json and print the corresponding CLI command.      W | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/next.py` | rationale |
| run_next() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/next.py` | code |

## Key Relationships

- **next.py** `contains` → run_next() `[EXTRACTED]`
- **next.py** `rationale_for` → Next command: read next_action from state.json and print the next CLI command. `[EXTRACTED]`
- **Next command: read next_action from state.json and print the next CLI command.** `rationale_for` → next.py `[EXTRACTED]`
- **Read next_action from state.json and print the corresponding CLI command.      W** `rationale_for` → run_next() `[EXTRACTED]`
- **run_next()** `contains` → next.py `[EXTRACTED]`
- **run_next()** `rationale_for` → Read next_action from state.json and print the corresponding CLI command.      W `[EXTRACTED]`