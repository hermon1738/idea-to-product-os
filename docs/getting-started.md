# Getting Started — Idea-to-Product OS
How to set up the full system on a new machine.

---

## Prerequisites

- A Hetzner VPS (CPX21 or equivalent) running Ubuntu 24.04
- Docker CE installed on the VPS
- A Discord account and server
- A Groq API key (console.groq.com)
- A Gemini API key (aistudio.google.com) — required for skeptic agent
- Git and SSH access to your VPS
- Python 3.9+ on your local machine
- An Anthropic API account with credits (separate from Claude Pro)
- A Claude Pro subscription for planning sessions

---

## Step 1 — Clone the repo and install the CLI

```bash
git clone https://github.com/hermon1738/idea-to-product-os.git
cd idea-to-product-os
pip install -e .
bricklayer --help
```

`bricklayer` is now available globally on your machine.
You use it from any project directory — not just this repo.

For `bricklayer close-session` (Groq sprint review):

```bash
pip install groq==0.11.0
```

---

## Step 2 — Set up VPS folder structure

SSH into your VPS and run:

```bash
mkdir -p ~/ai-agents/docs
mkdir -p ~/ai-agents/agents
cat > ~/ai-agents/docs/decision-log.md << 'EOF'
# Decision Log — Idea-to-Product OS
| Date | Component | Decision Made | Status | Next Action |
|------|-----------|--------------|--------|-------------|
EOF
touch ~/ai-agents/docs/pipeline-status.md
mkdir -p /workspace
```

`/workspace` is the bind mount root for the Remote Build Executor.
It must exist before any remote build runs.

---

## Step 3 — Configure secrets

```bash
nano ~/ai-agents/.env
```

Add:

```
DISCORD_TOKEN=your_bot_token
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
ANTHROPIC_API_KEY=your_anthropic_api_key
TONY_DISCORD_USER_ID=your_discord_user_id
DOCS_PATH=/app/docs
```

---

## Step 4 — Deploy Session Scribe

```bash
mkdir -p ~/ai-agents/agents/session-scribe
# copy agent.py, Dockerfile, requirements.txt from hermon1738/ai-agents
cd ~/ai-agents/agents/session-scribe
docker build -t session-scribe .
docker run -d \
  --name session-scribe \
  --restart unless-stopped \
  --env-file ~/ai-agents/.env \
  -e DOCS_PATH=/app/docs \
  -v ~/ai-agents/docs:/app/docs \
  session-scribe
docker logs session-scribe
# Should show: Session Scribe online
```

---

## Step 5 — Set up your AI project context

Create a project in Claude. Upload all files from `system-prompts/`.
Also add `context/pipeline-status.md` and `context/decision-log.md`.

Set project instructions to:

```
Read AGENT.md at the start of every session. Read context/pipeline-status.md
to know where the system is. Read context/decision-log.md for the last
decision made. Apply system-prompts/stack-rules.md to every engineering plan.
```

---

## Step 6 — Run your first session

```bash
bricklayer resume
bricklayer status
bricklayer next
```

Or start a new idea — load `system-prompts/venture-os.md` into the Claude
project and describe your idea. The pipeline starts with Venture OS.

End every session with `bricklayer close-session` then `!scribe` in Discord.

---

## Starting a New Project

The CLI is a global tool. New projects do not contain bricklayer source,
tests, or infrastructure. They need `bricklayer.yaml` and a bootstrap setup.

### Step 1 — Create the repo

```bash
mkdir my-project && cd my-project
git init
cp /path/to/idea-to-product-os/templates/bricklayer.yaml ./bricklayer.yaml
```

Open `bricklayer.yaml` and replace every `/path/to/idea-to-product-os`
with the absolute path to your actual installation. Also update the `test:`
section with your project's test path:

```yaml
test:
  language: Python
  command: python3 -m pytest -v ../proxy/
```

**IMPORTANT — target the package root, not a `tests/` subdirectory.**
If tests are co-located with modules (e.g. `proxy/providers/groq/tests/`),
a path like `../proxy/tests/` silently skips them. Always use the highest
common ancestor that contains all your tests. Wrong path = silent PASS
with missing test coverage.

The `test:` section is how bricklayer knows what command to run for your
project. `context.txt` is auto-generated from it — never edit `context.txt`
directly.

### Step 2 — Run the bootstrap setup

This is mandatory before the first brick runs. Do not skip it.

```bash
# Set git editor — prevents vim blocking the terminal during merges
git config core.editor "nano"

# Create bricklayer runtime directories
mkdir -p bricklayer/skeptic_packet

# Write initial state.json
# CRITICAL: current_phase and current_feature MUST include the full branch
# prefix — use "phase/0-name" not "0-name", "feature/my-project" not "my-project".
# Wrong prefixes cause --verdict PASS to fail on merge.
cat > bricklayer/state.json << 'EOF'
{
  "current_brick": "0.1-first-brick",
  "current_phase": "phase/0-phase-name",
  "current_feature": "feature/project-name",
  "status": "in_progress",
  "loop_count": 0,
  "last_gate_failed": null,
  "completed_bricks": [],
  "next_action": "snapshot_init",
  "last_test_run": {
    "command": "",
    "status": "",
    "exit_code": 0,
    "artifact": "",
    "failed_nodeids": []
  }
}
EOF

# Write .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
.pytest_cache/

# Environment
.env

# Bricklayer runtime — never committed
bricklayer/skeptic_packet/
bricklayer/skeptic_verdict.md
bricklayer/state.json
bricklayer/context.txt
bricklayer/handover.md
.workflow/

# Workspace — runtime bind mount root
workspace/

# macOS
.DS_Store
EOF
```

### Step 3 — Validate and write context.txt

`bricklayer run` validates all paths in `bricklayer.yaml` and writes
`bricklayer/context.txt` automatically from the `test:` section. Run this
once after bootstrap and any time you change `bricklayer.yaml`.

```bash
bricklayer run                  # validates all paths + writes context.txt
cat bricklayer/context.txt      # confirm it wrote correctly
```

Expected output of `cat bricklayer/context.txt`:
```
# AUTO-GENERATED by bricklayer — do not edit manually
LANGUAGE: Python
TEST_COMMAND: python3 -m pytest -v ../YOUR_TEST_PATH/
```

If `bricklayer run` reports missing paths, open `bricklayer.yaml` and fix
every path that still contains `/path/to/idea-to-product-os`. Then run
`bricklayer run` again until it shows: `bricklayer.yaml loaded and all paths validated.`

### Step 4 — Start building

```bash
bricklayer branch --feature my-feature
bricklayer branch --phase 0 bootstrap
bricklayer branch 0 first-brick
bricklayer status
```

---

## Known Issues and Fixes

These are real problems that were hit in production. They are fixed in the
current repo. Documented here so they are never hit again.

**make_skeptic_packet.py hardcoded pytest path (fixed in current repo)**
The tool originally ran `pytest -q` with no path, causing exit 5 (no tests
found) because it ran from `bricklayer/` CWD. It now reads `TEST_COMMAND`
from `context.txt`. This fix is already in the current repo — no action needed.

**context.txt is auto-generated — never edit it manually**
`context.txt` is written by `bricklayer run` from the `test:` section of
`bricklayer.yaml`. Editing it directly will cause it to be overwritten on
the next `bricklayer run`. Always change `bricklayer.yaml` instead, then
run `bricklayer run` to apply.

**state.json location**
Lives at `bricklayer/state.json`. Not at root `state.json`. Not at
`.workflow/state.json`. The bootstrap step above puts it in the right place.

**state.json required fields and branch prefix format**
All of the following fields are required or bricklayer rejects the file:
`current_brick`, `current_phase`, `current_feature`, `status`, `loop_count`,
`last_gate_failed`, `completed_bricks`, `next_action`, `last_test_run`.
`last_test_run` itself requires: `command`, `status`, `exit_code`, `artifact`,
`failed_nodeids`. The bootstrap state.json above includes all of them.

**CRITICAL — branch prefix format:** `current_phase` and `current_feature` must
include the full branch prefix. Write `"phase/0-llm-proxy"` not `"0-llm-proxy"`.
Write `"feature/remote-build-executor"` not `"remote-build-executor"`. Wrong
values cause `--verdict PASS` to fail with a git checkout error. The CLI writes
these correctly when `bricklayer branch` runs — only manual state.json edits
can introduce this error.

**git editor set to vim by default**
Set `git config core.editor "nano"` before any merge. Vim blocks the terminal
on merge commits and requires knowing vim commands to exit. The bootstrap
step above sets nano automatically.

---

## Every Session Start Checklist

1. `bricklayer resume` — restore last session state
2. `bricklayer status` — confirm current position
3. `bricklayer next` — get next command
4. Work the phase
5. `bricklayer pause` or `bricklayer close-session`
6. `!scribe` in Discord
7. Sync context files back to AI project