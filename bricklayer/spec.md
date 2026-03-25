BRICK: Brick 19 - bricklayer new-project

WHAT:
  `bricklayer new-project <name>` scaffolds a new project directory
  at context/projects/<name>/ with the three files every project
  needs to track state and decisions.

INPUT:
  Project name as positional argument

OUTPUT:
  bricklayer new-project reddit-monitor
    -> creates context/projects/reddit-monitor/
    -> creates context/projects/reddit-monitor/STATE.md
    -> creates context/projects/reddit-monitor/decision-log.md
    -> creates context/projects/reddit-monitor/state.json
    -> prints "Project created: context/projects/reddit-monitor/"

  Project name already exists -> error, exit 1, no files created
  Invalid name (spaces, special chars) -> error, exit 1
  context/projects/ created if it doesn't exist

GATE:
  OUTPUTS

BLOCKER:
  bricklayer context (Brick 20) reads from this structure.

WAVE:
  SEQUENTIAL

FILES:
- cli/commands/new_project.py
- cli/main.py
- tests/test_new_project.py
- bricklayer/spec.md

ACCEPTANCE CRITERIA:
1) Valid name -> all three files created with correct initial content, exit 0
2) Duplicate name -> error, exit 1, no files created
3) Invalid name (spaces) -> error, exit 1
4) Invalid name (/, \, .) -> error, exit 1
5) Kebab-case and underscores are valid names
6) context/projects/ created if it doesn't exist
7) state.json is valid JSON with all required fields

TEST REQUIREMENTS:
- Happy path: valid name -> all three files, correct content, exit 0
- Duplicate name -> error, exit 1, no files created
- Invalid name with spaces -> error, exit 1
- Invalid name with special chars -> error, exit 1
- Kebab-case and underscores are valid
- context/projects/ created if absent
- state.json valid JSON with all required fields
- CliRunner integration

OUT OF SCOPE:
- Modifying any existing project
- Writing to bricklayer/state.json
- Any command other than new-project
- Any file outside the FILES list
