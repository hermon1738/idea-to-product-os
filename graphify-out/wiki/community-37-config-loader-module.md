# Config Loader Module

> Community 37 · 10 nodes · cohesion 0.27

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| config.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/config.py` | code |
| find_yaml() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/config.py` | code |
| load_and_validate() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/config.py` | code |
| _load_dotenv() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/config.py` | code |
| YAML loader and path validation for bricklayer.yaml.  WHY THIS EXISTS:     Every | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/config.py` | rationale |
| Write bricklayer/context.txt from the test: section of bricklayer.yaml.      WHY | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/config.py` | rationale |
| Load bricklayer.yaml, resolve all declared paths, exit 1 on any failure.      Wh | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/config.py` | rationale |
| Load a .env file from directory into os.environ (non-overwriting).      Why it e | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/config.py` | rationale |
| Walk upward from start until bricklayer.yaml is found.      Why it exists: Comma | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/config.py` | rationale |
| _write_context_txt() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/config.py` | code |

## Key Relationships

- **config.py** `contains` → _load_dotenv() `[EXTRACTED]`
- **config.py** `contains` → find_yaml() `[EXTRACTED]`
- **config.py** `contains` → _write_context_txt() `[EXTRACTED]`
- **find_yaml()** `contains` → config.py `[EXTRACTED]`
- **find_yaml()** `calls` → load_and_validate() `[INFERRED]`
- **find_yaml()** `rationale_for` → Walk upward from start until bricklayer.yaml is found.      Why it exists: Comma `[EXTRACTED]`
- **load_and_validate()** `contains` → config.py `[EXTRACTED]`
- **load_and_validate()** `calls` → find_yaml() `[INFERRED]`
- **load_and_validate()** `calls` → _load_dotenv() `[INFERRED]`
- **_load_dotenv()** `contains` → config.py `[EXTRACTED]`
- **_load_dotenv()** `calls` → load_and_validate() `[INFERRED]`
- **_load_dotenv()** `rationale_for` → Load a .env file from directory into os.environ (non-overwriting).      Why it e `[EXTRACTED]`
- **YAML loader and path validation for bricklayer.yaml.  WHY THIS EXISTS:     Every** `rationale_for` → config.py `[EXTRACTED]`
- **Write bricklayer/context.txt from the test: section of bricklayer.yaml.      WHY** `rationale_for` → _write_context_txt() `[EXTRACTED]`
- **Load bricklayer.yaml, resolve all declared paths, exit 1 on any failure.      Wh** `rationale_for` → load_and_validate() `[EXTRACTED]`
- **Load a .env file from directory into os.environ (non-overwriting).      Why it e** `rationale_for` → _load_dotenv() `[EXTRACTED]`
- **Walk upward from start until bricklayer.yaml is found.      Why it exists: Comma** `rationale_for` → find_yaml() `[EXTRACTED]`
- **_write_context_txt()** `contains` → config.py `[EXTRACTED]`
- **_write_context_txt()** `calls` → load_and_validate() `[INFERRED]`
- **_write_context_txt()** `rationale_for` → Write bricklayer/context.txt from the test: section of bricklayer.yaml.      WHY `[EXTRACTED]`