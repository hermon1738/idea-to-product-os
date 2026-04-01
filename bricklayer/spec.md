BRICK: bricklayer-cli — Test Command Config

WHAT:
  Add test: section to bricklayer.yaml. On startup, CLI reads
  test.command and test.language from bricklayer.yaml and writes
  bricklayer/context.txt automatically. context.txt is never written
  manually again.

INPUT:
  Current CLI load_and_validate() in cli/main.py and cli/config.py.
  Current templates/bricklayer.yaml.

OUTPUT:
  bricklayer.yaml has test: section. CLI writes context.txt on every
  startup from yaml values. Changing test command is a one-line edit
  in bricklayer.yaml.

GATE:
  - bricklayer --help on a project with test: in bricklayer.yaml writes
    correct context.txt automatically
  - changing test.command in bricklayer.yaml and running any bricklayer
    command updates context.txt
  - missing test: section — CLI warns but does not fail; context.txt
    left unchanged if it already exists
  - context.txt write is atomic (temp file then rename)
  - all new tests pass

BLOCKER:
  context.txt can never go out of sync with bricklayer.yaml.

WAVE:
  SEQUENTIAL

FILES:
- cli/main.py
- cli/config.py
- templates/bricklayer.yaml
- bricklayer.yaml
- tests/test_config_write.py
- bricklayer/spec.md
- bricklayer/context.txt
- bricklayer/state.json

ACCEPTANCE CRITERIA:
1) load_and_validate with test.command and test.language writes correct
   context.txt at bricklayer/context.txt
2) load_and_validate without test: section leaves existing context.txt
   unchanged and prints warning to stderr
3) load_and_validate with test: section but missing command field exits
   with clear error message
4) context.txt written atomically (temp file then os.replace)
5) templates/bricklayer.yaml has test: section with -v flag
6) bricklayer.yaml (root) has test: section
7) _write_context_txt has WHY THIS EXISTS docstring

TEST REQUIREMENTS:
- load_and_validate with test.command and test.language writes correct context.txt
- load_and_validate without test: section leaves existing context.txt unchanged
- load_and_validate with test: section but missing command field exits with error
- context.txt written with -v flag when test.command contains -v
- context.txt written atomically (temp file then rename)

OUT OF SCOPE:
- Any file outside the FILES list
- Changes to bricklayer/tools/
- Changes to other CLI commands
- Changes to tests/ other than adding tests/test_config_write.py
