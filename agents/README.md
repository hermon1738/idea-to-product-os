# Agents

All live agents are maintained in a separate repository:

**[hermon1738/ai-agents](https://github.com/hermon1738/ai-agents)**

---

## Current Agents

| Agent | Path | Command | Status |
|-------|------|---------|--------|
| Session Scribe | `agents/session-scribe/` | `!scribe`, `!log`, `!status`, `!debug` | Live |
| Org Schema Formatter | `agents/org-schema-formatter/` | `!schema` | Live |
| Assignment Dispatcher | `agents/assignment-dispatcher/` | `!dispatch` | Live |

---

## Agent Structure

Every agent follows this pattern:

```
agents/[agent-name]/
├── agent.py          ← the bot
├── Dockerfile        ← python:3.11-slim, PYTHONUNBUFFERED=1
└── requirements.txt  ← pinned deps including groq==0.11.0, httpx==0.27.2
```

---

## Deployment Pattern

```bash
cd ~/ai-agents/agents/[agent-name]
docker build -t [agent-name] .
docker run -d \
  --name [agent-name] \
  --restart unless-stopped \
  --env-file ~/ai-agents/.env \
  [agent-name]
```

---

## Known Version Pins

Always use these — they resolve the groq/httpx proxies conflict:

```
groq==0.11.0
httpx==0.27.2
discord.py==2.3.2
```
