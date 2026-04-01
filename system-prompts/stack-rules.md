# Stack Rules — Idea-to-Product OS
> Claude must apply these rules to every engineering plan, agent spec,
> and project brief generated in this project. No exceptions.
>
> FIRST: identify the project type from the Org Schema.
> Only the rules for that type apply. Rules from other types do not bleed in.

---

## Project Types

| Type | What it is |
|---|---|
| **AGENT** | Background automation. Discord or cron triggered. Single container. No UI. |
| **WEB_APP** | Browser UI + FastAPI backend + Postgres. docker-compose on VPS. |
| **SYSTEM** | Multi-layer software. Stack decided per project during Venture OS. |
| **CLI_TOOL** | Python package. Local install. No server. |

---

## AGENT Rules

### Infrastructure
- Host: Hetzner VPS, CPX21, Ashburn VA, Ubuntu 24.04
- Runtime: Docker CE — every agent runs in its own container
- Base image: `python:3.11-slim`
- `ENV PYTHONUNBUFFERED=1` required in every Dockerfile
- Secrets: `os.environ` loaded from `--env-file ~/ai-agents/.env`
- Deploy repo: `hermon1738/ai-agents` — agent files only, no build tools
- Build repo: project-specific — bricklayer, docs, system prompts, skeptic packets
- Build path: `agents/[agent-name]/agent.py + Dockerfile`
- Deploy path: `~/ai-agents/agents/[agent-name]/` on VPS

### LLM Stack (AGENT)
- Production: `llama-3.1-8b-instant` via Groq SDK
- Heavy reasoning: `llama-3.3-70b-versatile` via Groq
- Pinned versions (always use these):
  - `groq==0.11.0`
  - `httpx==0.27.2`

### Control Interface (AGENT)
- Discord — one channel per agent
- Server: Idea-to-Product OS
- Command prefix: `!`

### Every AGENT Plan Must Output
1. `agent.py`
2. `Dockerfile`
3. `requirements.txt`
4. `docker run` command using `--env-file`

### Deployment Workflow (AGENT)
```
1. Build  → write agent files to agents/[agent-name]/ in project repo
2. Test   → skeptic PASS from human
3. Copy   → copy into hermon1738/ai-agents/agents/
4. Push   → git push hermon1738/ai-agents
5. Pull   → git pull on Hetzner VPS
6. Deploy → docker run on VPS using --env-file ~/ai-agents/.env
7. Verify → docker logs [agent-name] confirms live
8. Log    → !scribe in Discord
```
Never write agent files directly to ~/ai-agents/ during development.
Build repo is for building. Deploy repo is for running. Never mix them.

### Docker Run Template (AGENT)
```bash
docker run -d \
  --name [agent-name] \
  --restart unless-stopped \
  --env-file ~/ai-agents/.env \
  [any -e overrides] \
  [any -v volume mounts] \
  [agent-name]
```

---

## WEB_APP Rules

### Stack Defaults
These are the default choices for WEB_APP projects. The arch-brain
architecture session may override any of these. When an override is
made, it is recorded as a Decision Record in ARCHITECTURE.md and
becomes the locked choice for that project.

If no architecture session has been run for this project, these
defaults apply. If an architecture session has been run, ARCHITECTURE.md
overrides this section entirely for that project.

| Layer | Default Choice | Common Alternatives |
|---|---|---|
| Backend | FastAPI (Python 3.11, async) | Django, Node/Express, Hono |
| Frontend | Next.js (App Router) + React | Remix, SvelteKit, plain React |
| Styling | Tailwind CSS | CSS Modules, styled-components |
| Component lib | shadcn/ui | Radix, MUI, custom |
| Database | PostgreSQL 15 | MySQL, SQLite (small scale), MongoDB |
| ORM | SQLAlchemy 2.x (async) + Alembic | Prisma (if Node), Drizzle |
| Auth | JWT (python-jose + passlib) | Clerk, Auth0, Supabase Auth |
| Reverse proxy | Caddy (auto-TLS) | Nginx |
| Payments | Stripe | Paddle, Lemon Squeezy |
| Email | Resend | SendGrid, Postmark |
| Storage | Local VPS volume | S3-compatible (Cloudflare R2) |
| Monitoring | Sentry (free tier) + UptimeRobot | Datadog, New Relic |

### Infrastructure (WEB_APP)
- Host: Hetzner VPS, CPX21, Ashburn VA, Ubuntu 24.04
- Runtime: Docker Compose — all services as a compose stack
- Secrets: `.env` at project root, loaded by docker-compose

### Services (WEB_APP)
```
api    — FastAPI app (python:3.11-slim)
db     — PostgreSQL 15 (postgres:15-alpine)
caddy  — Reverse proxy + TLS (caddy:2-alpine)
```
Frontend is built as static files, served by Caddy directly.
No separate Node.js container in production.

### docker-compose Template (WEB_APP)
```yaml
services:
  db:
    image: postgres:15-alpine
    restart: unless-stopped
    env_file: .env
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: ./backend
    restart: unless-stopped
    env_file: .env
    depends_on:
      - db
    expose:
      - "8000"

  caddy:
    image: caddy:2-alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
    depends_on:
      - api

volumes:
  postgres_data:
  caddy_data:
```

### Every WEB_APP Plan Must Output
1. `docs/ARCHITECTURE.md` — approved before any other file is written
2. `docs/wireframes/` — one markdown file per screen (before frontend starts)
3. Backend source — framework and structure per ARCHITECTURE.md
4. Frontend source — framework and structure per ARCHITECTURE.md
5. `docker-compose.yml` — or deployment config per ARCHITECTURE.md
6. Migration files — schema as defined in ARCHITECTURE.md data domain
7. `.env.example` — all required env vars, no real values

### Deployment Workflow (WEB_APP)
```
1. Design   → wireframe spec approved by Tony before any component is written
2. Build    → source files written in project repo
3. Test     → backend: pytest passes. Frontend: next build clean.
4. Migrate  → alembic upgrade head runs clean on fresh Postgres
5. Push     → git push project repo
6. Pull     → git pull on Hetzner VPS
7. Deploy   → docker compose up -d --build
8. Verify   → curl https://[domain]/health returns 200
9. Log      → !scribe in Discord
```
Always run migrations before starting the API container.

### LLM Stack (WEB_APP, if AI features exist)
Same as AGENT. Switch Groq to paid tier before accepting user payments.

---

## SYSTEM Rules

A SYSTEM is any multi-component software that doesn't fit cleanly into
AGENT, WEB_APP, or CLI_TOOL. Examples: desktop applications, data
pipelines, embedded software, hardware-integrated systems, internal
tools with multiple services.

### Stack Decision Rule
SYSTEM projects do not have a fixed prescribed stack.
The stack is determined by the Architecture Layers in the Org Schema,
confirmed during the Venture OS Phase Confirmation Gate.

When plan-brain receives a SYSTEM brief, it uses the confirmed layers
to determine the right stack per layer — not this file.

### Infrastructure Defaults (SYSTEM)
- Server-side components: Hetzner VPS, Docker (single containers or compose)
- Hardware components: determined by the project (Raspberry Pi, Arduino, etc.)
- Edge/embedded components: determined by the project
- If a layer needs a database: PostgreSQL preferred, unless the data
  model clearly requires something else (time-series → TimescaleDB, etc.)
- If a layer has a web UI: follow WEB_APP frontend rules for that layer
- If a layer has background workers: Docker container, same VPS

### Deployment Workflow (SYSTEM)
There is no fixed deployment workflow for SYSTEM projects.
The deployment approach is determined by the architecture layers
confirmed in the Venture OS Phase Confirmation Gate.

plan-brain generates a deployment workflow per layer as part of
the build plan. That workflow is the authority — not this file.

Required regardless of stack:
- Every deployed component has a verify step
  (health check, log, smoke test, or equivalent for the technology)
- Every secret is kept out of source code
- Always backup or push before deploying to a live environment

### Every SYSTEM Plan Must Output (at minimum)
1. Architecture diagram (markdown, in `docs/architecture.md`)
2. Per-layer: source files, build config, deployment instructions
3. `.env.example` — all required env vars across all layers
4. Integration test spec — how layers are verified to talk to each other

---

## CLI_TOOL Rules

### Stack
- Language: Python 3.11
- Package manager: `pyproject.toml` (no setup.py)
- CLI framework: Typer
- Distribution: `pip install` or binary via PyInstaller

### Infrastructure (CLI_TOOL)
- No server required
- No Docker unless the tool needs a sidecar service
- Runs locally on developer machine

### Every CLI_TOOL Plan Must Output
1. `src/[package_name]/` — source modules
2. `pyproject.toml`
3. `README.md` — install + usage

---

## Excluded Platforms (all types)
- Railway, Render, Oracle Free Tier: never recommend
- Vercel: excluded for backends and agents. Acceptable only for deploying
  a pre-built static frontend that calls an API hosted on your VPS.
- Any serverless platform: excluded for background workers and agents

---

## Code Architecture Standard (all project types)

These rules govern how modules are structured and how they talk to
each other. They apply on top of the production-ready standard in
plan-brain.md. Together they ensure that changes to one module do
not break others.

### Interface-First
Every new module defines its public contract before implementation.
  Python:
    - Pydantic models define all inputs and outputs
    - `__init__.py` defines `__all__` — the explicit public API
    - Nothing outside this list may be imported by other modules
  TypeScript/React:
    - Types and interfaces defined in a `types.ts` or `types/` file
    - Components export only what is documented
    - Props interfaces are defined before the component is written

### No Internals Imports
Other modules import only from a module's public API.
Never import from inside another module's internal files.
  Bad:  from backend.modules.users.crud import _hash_password
  Good: from backend.modules.users import hash_password
  Bad:  import { internalHelper } from './UserCard/helpers'
  Good: import { UserCard } from './UserCard'

### Dependency Direction
Dependencies flow in one direction only. Never circular.
  Standard layering (backend):
    API routes → Services → Repositories → Database
    Each layer may only import from the layer directly below it.
    Database layer never imports from Services.
    Services never import from API routes.
  Standard layering (frontend):
    Pages → Features → Components → UI primitives
    Lower layers never import from higher layers.

### Business Logic Isolation
Business logic lives in one place. It does not leak into other layers.
  Backend: business logic lives in the Services layer only
    - API routes validate input and call services. No logic.
    - Repositories query the database. No logic.
    - Services do the work. No database queries directly.
  Frontend: business logic lives in hooks or service files only
    - Components render. No business logic.
    - Hooks and service files compute and transform. No rendering.

### Shared Types as the Contract
Types shared between modules are the contract between them.
  Backend: shared Pydantic schemas in a `schemas/` module
  Frontend: shared TypeScript interfaces in a `types/` module
  Full-stack: API response types defined once, used by both layers
  When a type changes, every module that uses it must be updated
  in the same brick — never leave consumers out of sync.

These standards are checked at the gate by the skeptic.
Any violation is a critical flaw, same weight as a broken test.

### Docs Structure (VPS)
- `~/ai-agents/docs/decision-log.md` — append-only session log
- `~/ai-agents/docs/pipeline-status.md` — full pipeline snapshot, rewritten each session

### Cost Baseline (do not exceed)
- Claude Pro: ~$20/mo
- Groq free tier: deployed agents
- Hetzner CPX21: ~$7/mo
- Target total: ~$30/mo
- WEB_APP add: Postgres + Caddy = $0 (same VPS). Stripe = % of revenue only.
- SYSTEM: cost determined per project at Venture OS phase.

### Git Commit Message Format
```
feat: add [component-name]

- What it does
- Key dependencies / version pins
- Interfaces it exposes (Discord commands / API routes / CLI commands)
```

### VPS is not a backup.
Push before deploying. Every time. No exceptions.
