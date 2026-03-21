# Stack Rules — Idea-to-Product OS
> Claude must apply these rules to every engineering plan, agent spec,
> and project brief generated in this project. No exceptions.

---

## Infrastructure (non-negotiable)
- Host: Hetzner VPS, CPX21, Ashburn VA, Ubuntu 24.04
- Runtime: Docker CE — every agent runs in a container
- Base image: `python:3.11-slim`
- `ENV PYTHONUNBUFFERED=1` required in every Dockerfile
- Secrets: `os.environ` loaded from `--env-file ~/ai-agents/.env`
- Deploy repo: `hermon1738/ai-agents` — agent files only, no build tools
- Build repo: project-specific (e.g., `redit-monitor`) — bricklayer,
  docs, system prompts, skeptic packets live here
- Build path: `agents/[agent-name]/agent.py + Dockerfile` (relative
  to project repo root)
- Deploy path: `~/ai-agents/agents/[agent-name]/` on VPS

## Excluded Platforms (never recommend)
Vercel, Railway, Render, Oracle Free Tier, any serverless platform.
Exception: only if the task is explicitly stateless and one-time.

## LLM Stack
- Production agents: `llama-3.1-8b-instant` via Groq SDK
- Heavy reasoning tasks: `llama-3.3-70b-versatile` via Groq
- Known working version pins (always use these):
  - `groq==0.11.0`
  - `httpx==0.27.2`

## Control Interface
- Discord (preferred) — one channel per agent
- Server name: Idea-to-Product OS
- Command prefix: `!`

## Every Plan Must Output
1. `agent.py`
2. `Dockerfile`
3. `requirements.txt`
4. `docker run` command using `--env-file`

## Docs Structure (VPS)
- `~/ai-agents/docs/decision-log.md` — append-only session log
- `~/ai-agents/docs/pipeline-status.md` — full pipeline snapshot, rewritten each session

## Cost Baseline (do not exceed)
- Claude Pro: ~$20/mo — planning, Claude Code
- Groq free tier: deployed agents
- Hetzner CPX21: ~$7/mo
- Target total: ~$30/mo

## Agent Naming Convention
- `agent-01`, `agent-02` etc. for sequenced agents
- Descriptive names for named agents: `session-scribe`, `repo-watcher`

## Deployment Workflow (always in this order)
Every agent build must follow this sequence — no exceptions:

```
1. Build → write agent files to agents/[agent-name]/ in project repo
2. Test → gate passes in bricklayer locally (skeptic PASS from human)
3. Copy → copy agents/[agent-name]/ into hermon1738/ai-agents/agents/
4. Push → git push hermon1738/ai-agents
5. Pull → git pull on Hetzner VPS
6. Deploy → docker run on VPS using --env-file ~/ai-agents/.env
7. Verify → docker logs [agent-name] confirms it's live
8. Log → !scribe in Discord
```
Never write agent files directly to ~/ai-agents/ during development.
Build repo is for building. Deploy repo is for running. Never mix them.
Claude Code always writes to the project repo path, never to ~/ai-agents/.

VPS is not a backup. If you deploy without pushing, the code only
exists on one machine. Push every time.

### Git Commit Message Format
```
feat: add [agent-name]

- What it does
- Key dependencies / version pins
- Commands it responds to (if Discord bot)
```

## Docker Run Template (always follow this format)
```bash
docker run -d \
  --name [agent-name] \
  --restart unless-stopped \
  --env-file ~/ai-agents/.env \
  [any -e overrides] \
  [any -v volume mounts] \
  [agent-name]
```
