# Getting Started — Idea-to-Product OS

How to set up the full system on a new machine.

---

## Prerequisites

- A Hetzner VPS (CPX21 or equivalent) running Ubuntu 24.04
- Docker CE installed on the VPS
- A Discord account and server
- A Groq API key (console.groq.com)
- Git and SSH access to your VPS
- An AI subscription (Claude Pro, ChatGPT Plus, or similar)

---

## Step 1 — Clone the repo

```bash
git clone https://github.com/hermon1738/idea-to-product-os.git
cd idea-to-product-os
```

---

## Step 2 — Set up VPS folder structure

SSH into your VPS and run:

```bash
mkdir -p ~/ai-agents/docs
mkdir -p ~/ai-agents/agents

# Seed the docs
cat > ~/ai-agents/docs/decision-log.md << 'EOF'
# Decision Log — Idea-to-Product OS
> Session rows appended automatically by Session Scribe

## Session Log
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

Add these lines:

```
DISCORD_TOKEN=your_main_bot_token
GROQ_API_KEY=your_groq_key
DOCS_PATH=/app/docs
```

Add additional tokens as you deploy more agents:

```
SCHEMA_CHANNEL_ID=your_channel_id
DISPATCHER_TOKEN=your_dispatcher_bot_token
DISPATCHER_CHANNEL_ID=your_dispatcher_channel_id
```

---

## Step 4 — Deploy Session Scribe (Agent-02)

```bash
mkdir -p ~/ai-agents/agents/session-scribe
# Copy agent.py, Dockerfile, requirements.txt from hermon1738/ai-agents

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

Create a new project in your AI tool of choice (Claude, ChatGPT, etc.)
Upload or paste all files from `system-prompts/`:

- `venture-os.md`
- `agent-os.md`
- `repo-auditor.md`
- `stack-rules.md`

Also add your working context files:

- `pipeline-status.md` (from `~/ai-agents/docs/`)
- `decision-log.md` (from `~/ai-agents/docs/`)

Set the project instructions to:

```
I am building the Idea-to-Product OS. Read pipeline-status.md at the
start of every session to know where the system is. Read decision-log.md
to know the last decision made. Apply stack-rules.md to every engineering
plan. Never ask me to re-explain my stack.
```

---

## Step 6 — Run your first session

Open your AI project. Say:

```
Entry Point B — I have a new idea: [describe your idea].
Start Phase 2.
```

Follow the pipeline through to Phase 7.
End every session with `!scribe` in Discord.
Sync the updated docs back into your AI project.

---

## Every Session Start Checklist

1. Read `pipeline-status.md` — know where you are in 30 seconds
2. Read `decision-log.md` — know last session's next action
3. Tell the AI which phase you're entering
4. Work the phase
5. End with `!scribe` in Discord
6. Sync docs back to AI project

---

## Deploying Additional Agents

All agents follow the same pattern:

```bash
mkdir -p ~/ai-agents/agents/[agent-name]
# create agent.py, Dockerfile, requirements.txt

cd ~/ai-agents/agents/[agent-name]
docker build -t [agent-name] .
docker run -d \
  --name [agent-name] \
  --restart unless-stopped \
  --env-file ~/ai-agents/.env \
  [any additional -e or -v flags] \
  [agent-name]

docker logs [agent-name]

# After confirming it works:
cd ~/ai-agents
git add agents/[agent-name]/
git commit -m 'feat: add [agent-name]'
git push origin main
```

See `hermon1738/ai-agents` for all deployed agent source code.
