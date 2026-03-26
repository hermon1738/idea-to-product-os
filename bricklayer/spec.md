BRICK: Brick 24 - bricklayer agent deploy + live

WHAT:
  `bricklayer agent deploy` copies a scaffolded agent directory to the
  ai-agents deploy repo, commits and pushes, then prints the exact
  docker commands to run on the VPS. Does NOT SSH. Also adds
  `bricklayer agent live --id <id>` which marks a deployed agent as
  live in the registry after VPS confirmation.

INPUT:
  Agent ID (--id), DEPLOY_REPO_PATH env var (path to local clone of
  hermon1738/ai-agents)

OUTPUT:
  deploy: files copied to DEPLOY_REPO_PATH/agents/<id>/, git commit +
    push, registry status updated to deployed, VPS commands printed.
  live: registry status updated from deployed to live, confirmation
    printed.

GATE:
  OUTPUTS — with DEPLOY_REPO_PATH set to a temp git repo, deploy
  copies files, creates git commit, updates registry to deployed,
  prints VPS commands. bricklayer agent live --id updates to live.
  Missing DEPLOY_REPO_PATH exits 1.

BLOCKER:
  Nothing. This closes Phase 6 agent layer.

WAVE:
  SEQUENTIAL

FILES:
- cli/commands/agent.py
- tests/test_agent_deploy.py
- bricklayer/spec.md
- README.md

ACCEPTANCE CRITERIA:
1) deploy: valid agent + DEPLOY_REPO_PATH set -> files copied, commit created, registry status=deployed, exit 0
2) deploy: VPS commands printed with docker build, docker run --env-file, --restart unless-stopped
3) deploy: agent not in registry -> error, exit 1
4) deploy: agent directory missing -> error with path, exit 1
5) deploy: DEPLOY_REPO_PATH not set -> error with setup instructions, exit 1
6) deploy: DEPLOY_REPO_PATH not a git repo -> error, exit 1
7) deploy: git push fails -> error printed with git output, status NOT updated, exit 1
8) live: known ID with status=deployed -> status updated to live, exit 0
9) live: unknown ID -> error, exit 1
10) live: agent already live -> prints already-live message, exit 0
11) No raw tracebacks on any error path

TEST REQUIREMENTS:
- deploy: valid args -> files copied, git commit created, registry=deployed, exit 0
- deploy: VPS commands contain docker build + docker run with --env-file and --restart unless-stopped
- deploy: agent not in registry -> error, exit 1
- deploy: agent directory missing -> error with path, exit 1
- deploy: DEPLOY_REPO_PATH not set -> error with setup hint, exit 1
- deploy: DEPLOY_REPO_PATH not a git repo -> error, exit 1
- deploy: git push fails -> error printed, status not updated, exit 1
- live: known ID status=deployed -> live, exit 0
- live: unknown ID -> error, exit 1
- live: already live -> already-live message, exit 0
- CliRunner integration: deploy + live via CliRunner with mocked git ops

OUT OF SCOPE:
- SSH to VPS
- Actually running docker commands
- Any file outside the FILES list
