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
with the absolute path to your actual installation.

### Step 2 — Run the bootstrap setup

This is mandatory before the first brick runs. Do not skip it.

```bash
# Set git editor — prevents vim blocking the terminal during merges
git config core.editor "nano"

# Create bricklayer runtime directories
mkdir -p bricklayer/skeptic_packet

# Write initial state.json
# Update current_brick, current_phase, current_feature to match your first brick
cat > bricklayer/state.json << 'EOF'
{
  "current_brick": "BRICK_ID",
  "current_phase": "PHASE_NAME",
  "current_feature": "FEATURE_NAME",
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

# Write context.txt
# IMPORTANT: TEST_COMMAND path is relative to bricklayer/ as CWD
# Use ../ to go up to the project root
# Example: ../proxy/tests/ not proxy/tests/
cat > bricklayer/context.txt << 'EOF'
LANGUAGE: Python
TEST_COMMAND: python3 -m pytest -q ../YOUR_TEST_PATH/
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

### Step 3 — Verify the tooling before Brick 1

Run all four commands in order. Every one must pass before Brick 1 starts.

```bash
bricklayer build --snapshot       # must exit 0
bricklayer build --verify         # must show: OK: all touched files in spec FILES list
bricklayer build --test           # must show: PASS with correct test count
bricklayer build --skeptic-packet # must show: test exit 0, correct test count
```

If `--test` passes but `--skeptic-packet` shows wrong test count or exit 5,
your `context.txt` TEST_COMMAND path is wrong. The path runs from `bricklayer/`
as CWD — verify it resolves correctly from there.

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

**state.json location**
Lives at `bricklayer/state.json`. Not at root `state.json`. Not at
`.workflow/state.json`. The bootstrap step above puts it in the right place.

**context.txt TEST_COMMAND path**
Path is relative to `bricklayer/` as CWD, not the project root.
Always use `../` to reach the project root. `../proxy/tests/` works.
`proxy/tests/` does not.

**state.json required fields**
All of the following fields are required or bricklayer rejects the file:
`current_brick`, `current_phase`, `current_feature`, `status`, `loop_count`,
`last_gate_failed`, `completed_bricks`, `next_action`, `last_test_run`.
`last_test_run` itself requires: `command`, `status`, `exit_code`, `artifact`,
`failed_nodeids`. The bootstrap state.json above includes all of them.

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