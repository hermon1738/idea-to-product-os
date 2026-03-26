# Getting Started — Idea-to-Product OS

How to set up the full system on a new machine.

---

## Prerequisites

- A Hetzner VPS (CPX21 or equivalent) running Ubuntu 24.04
- Docker CE installed on the VPS
- A Discord account and server
- A Groq API key (console.groq.com)
- Git and SSH access to your VPS
- Python 3.9+ on your local machine
- An AI subscription (Claude Pro, ChatGPT Plus, or similar)

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
```

---

## Step 3 — Configure secrets

```bash
nano ~/ai-agents/.env
```

Add:

```
DISCORD_TOKEN=your_bot_token
GROQ_API_KEY=your_groq_key
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

Create a project in Claude (or any AI). Upload all files from `system-prompts/`.
Also add `context/pipeline-status.md` and `context/decision-log.md`.

Set project instructions to:
```
Read AGENT.md at the start of every session. Read context/pipeline-status.md
to know where the system is. Read context/decision-log.md for the last
decision made. Apply system-prompts/stack-rules.md to every engineering plan.
```

---

## Step 6 — Install the Claude Code skill (if using Claude Code)

```bash
mkdir -p ~/.claude/skills
cp /path/to/idea-to-product-os/run-brick.md ~/.claude/skills/run-brick.md
```

Launch Claude Code with:
```bash
claude --dangerously-skip-permissions
```

---

## Step 7 — Run your first session

```bash
bricklayer resume
bricklayer status
bricklayer next
```

Or start a new idea — load `system-prompts/venture-os.md` into any AI and say:
```
Entry Point B — I have a new idea: [your idea]. Start Phase 2.
```

End every session with `bricklayer close-session` then `!scribe` in Discord.

---

## Starting a New Project (not this repo)

```bash
mkdir my-project && cd my-project
git init
cp /path/to/idea-to-product-os/templates/bricklayer.yaml ./bricklayer.yaml
cp /path/to/idea-to-product-os/templates/env.example ./.env
# edit bricklayer.yaml — replace /path/to/idea-to-product-os with real path
# edit .env — add your GROQ_API_KEY
echo ".env" >> .gitignore
bricklayer --help
bricklayer branch --feature my-feature
```

bricklayer auto-loads `.env` alongside `bricklayer.yaml` at startup — no
manual sourcing required. Keys already set in your shell are not overwritten.

---

## Every Session Start Checklist

1. `bricklayer resume` — restore last session state
2. `bricklayer status` — confirm current position
3. `bricklayer next` — get next command
4. Work the phase
5. `bricklayer pause` or `bricklayer close-session`
6. `!scribe` in Discord
7. Sync context files back to AI project
