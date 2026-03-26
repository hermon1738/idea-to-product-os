BRICK: Brick 25 - auto-.env loading + LLM config from bricklayer.yaml

WHAT:
  Two config improvements: (1) bricklayer auto-loads .env alongside
  bricklayer.yaml at startup — no manual sourcing required.
  (2) close-session reads LLM provider/model/api_key_env from
  bricklayer.yaml llm: section instead of hardcoded constants.

INPUT:
  .env at project root (optional), bricklayer.yaml llm: section

OUTPUT:
  .env loaded into os.environ at startup (non-overwriting).
  close-session uses llm: section config; falls back to Groq defaults
  with deprecation warning if section absent; exits 1 on unsupported
  provider.

GATE:
  RUNS — .env with GROQ_API_KEY loads automatically. Remove llm:
  section -> deprecation warning. provider: openai -> exit 1.

BLOCKER:
  Nothing downstream.

WAVE:
  SEQUENTIAL

FILES:
- cli/config.py
- cli/commands/close_session.py
- bricklayer.yaml
- templates/bricklayer.yaml
- templates/env.example
- docs/getting-started.md
- DEBT.md
- bricklayer/spec.md
- tests/test_config.py
- tests/test_main.py

ACCEPTANCE CRITERIA:
1) .env alongside bricklayer.yaml is loaded into os.environ at startup
2) .env absent -> silent skip, no error
3) existing os.environ keys NOT overwritten by .env values
4) malformed .env line -> line skipped, warning to stderr, other lines load
5) llm: section present -> correct values used, no deprecation warning
6) llm: section absent -> Groq defaults used, deprecation warning to stderr
7) provider: openai -> "Provider X not yet supported" error, exit 1
8) api_key_env points to unset var -> clear error, exit 1, no traceback
9) No raw tracebacks on any error path

TEST REQUIREMENTS:
- .env auto-load: KEY=VALUE loaded into os.environ
- .env auto-load: absent -> silent skip
- .env auto-load: existing env var not overwritten
- .env auto-load: malformed line skipped, warning, other lines load
- LLM config: llm: present -> no deprecation warning, correct values
- LLM config: llm: absent -> Groq defaults, deprecation warning stderr
- LLM config: provider: openai -> unsupported error, exit 1
- LLM config: api_key_env unset var -> clear error, exit 1
- CliRunner integration: .env + llm config via CliRunner

OUT OF SCOPE:
- openai/anthropic provider implementations (D-037)
- Any file outside the FILES list
