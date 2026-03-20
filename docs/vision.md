# Vision — Idea-to-Product OS

## The Goal

Run multiple AI-powered businesses where agents handle recurring
operational work and the human handles judgment, approvals, and
external relationships.

The system turns a business idea into a running organization:
- Agents per business function (content, research, ops, code)
- Agents run on schedules without manual triggers
- Human approves anything that touches the outside world
- Software components built via Bricklayer with independent review
- Everything logged, nothing forgotten between sessions

---

## What "Self-Sustaining" Actually Means

Be precise about this or you will build the wrong thing.

**What agents can reliably do today:**
- Repeatable, well-defined tasks (write a post, summarize a repo, review a PR)
- Scheduled work (daily digest, weekly brief, cron-triggered jobs)
- Structured decision-making with clear rules

**What agents cannot reliably do today:**
- Open-ended business judgment (should we pivot?)
- Client relationships (nuanced trust-building)
- Novel creative direction from scratch
- Catching their own errors without a human gate

**The honest version of the vision:** agents run the repeatable
operational layer, you handle the 20% that requires human judgment.
That is still a massive competitive advantage.

---

## The Four Stages

### Stage 1 — Reliable Deployment (DONE)
One agent, one real job, reliable deployment pipeline.
- Agents deploy via Docker on Hetzner VPS
- Session Scribe logs every session automatically
- Full deployment pipeline proven end-to-end

### Stage 2 — Automated Pipeline (DONE)
The pipeline runs itself from idea to deployed agent.
- org-schema-formatter: Phase 2→3 handoff automated
- assignment-dispatcher: Phase 3→4 handoff automated
- Pipeline validated end-to-end twice

### Stage 3 — First Real Business (NEXT)
3-4 specialized agents running simultaneously for one real business.
- Content agent posts weekly
- Research agent briefs you Monday morning
- Ops agent tracks key metrics
- You only touch approvals and judgment calls

### Stage 4 — Multiple Businesses
Multiple businesses, org-level orchestration, cross-business
resource sharing. Agents from one business reused in another.
This is the vision fully realized.

---

## The Playbook Principle

Agents can only run a business when the playbook is written.
The playbook comes from you doing the work first and knowing
what "done" looks like for every function.

Stage 3 is not just a technical step — it is you learning
what the agents need to know by running one business manually
enough to write the playbook. Stage 4 is what happens after
the playbook exists.
