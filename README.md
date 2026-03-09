# Multi-Agent Development Workflow(Beta test version)

A Claude Code-based multi-agent system that automates the full development cycle — from Jira ticket to implemented and tested code.

## Important Notice
This project is currently in the beta testing phase. We are not responsible for the following when using this project.
* Depending on how you use this system, Claude Code tokens may be consumed excessively.
* If you assign tasks without breaking them down into smaller units using the Divide and Conquer approach, the work may be interrupted when the context window limit is exceeded.
* The system is currently optimized for developing applications with the following stack: FE — TypeScript + Next.js, BE — Python + FastAPI, DB — Postgres.

---

## Overview

You provide a project idea. The agents handle the rest.

```
Natural Language Project Description
    ↓
Project Planner Agent — Feature list + priorities + tickets/ creation
    ↓
Human Review          — Adjust feature scope
    ↓
PM Agent              — Ticket → API spec, UI wireframe, test cases
    ↓
Human Review          — Inspect all artifacts
    ↓
BE Coding Agent       — FastAPI implementation
FE Coding Agent       — Next.js / React implementation
    ↓
QA-BE Agent           — pytest test suite
QA-FE Agent           — Vitest / Jest test suite
    ↓
Human Review
```

Each agent writes an implementation log explaining every decision it made. Nothing is a black box.

---

## Agents

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| `project-planner` | Project breakdown | Natural language description | `tickets/PLAN-XXX-*.md` |
| `pm` | Requirements authoring | Ticket `.md` | API spec, UI spec, wireframe HTML, test cases |
| `be-coding` | Backend scaffolding | API spec | FastAPI routes, services, repositories |
| `fe-coding` | Frontend scaffolding | UI spec + wireframe + API spec | Next.js pages, components, hooks |
| `qa-be` | Backend test authoring | BE test cases + implemented code | pytest test suite |
| `qa-fe` | Frontend test authoring | FE test cases + implemented code | Vitest / Jest test suite |

---

## Project Structure

```
Workspace/
├── .agents/                        # Agent instruction files
│   ├── project-planner/CLAUDE.md
│   ├── pm/CLAUDE.md
│   ├── be-coding/CLAUDE.md
│   ├── fe-coding/CLAUDE.md
│   ├── qa-be/CLAUDE.md
│   └── qa-fe/CLAUDE.md
│
├── .rules/                         # Coding standards (referenced by agents)
│   ├── be-coding-rules.md
│   └── fe-coding-rules.md
│
├── scripts/                        # Utility scripts
│   ├── run-agent.sh                # Agent launcher
│   ├── rate-limit-check.sh         # Claude Max rate limit check
│   ├── parse_usage.py              # Usage tracking
│   └── show-logs.sh                # View implementation logs
│
├── tickets/                        # Jira ticket exports
│   └── PROJ-123.md
│
├── be-api-requirements/            # API specs (PM Agent output)
│   └── PROJ-123-user-login.md
│
├── fe-ui-requirements/             # UI specs and wireframes (PM Agent output)
│   ├── PROJ-123-login-ui-spec.md
│   └── PROJ-123-login-wireframe.html
│
├── be-test-cases/                  # BE test cases (PM Agent output)
│   └── PROJ-123-user-login.md
│
├── fe-test-cases/                  # FE test cases (PM Agent output)
│   └── PROJ-123-user-login.md
│
├── logs/                           # Implementation logs (agent output)
│   ├── project-planner/
│   ├── pm/
│   ├── be-coding/
│   ├── fe-coding/
│   ├── qa-be/
│   └── qa-fe/
│
├── be-project/                     # FastAPI backend
└── fe-project/                     # Next.js frontend
```

---

## Prerequisites

- [Claude Code](https://docs.claude.ai/claude-code) installed and authenticated
- Python 3 (for rate limit tracking)
- Claude Max plan (5x usage tier)

---

## Usage

### Method A — Start with Project Idea (Recommended)

#### 1. Run Project Planner

```bash
bash scripts/run-agent.sh project-planner --project "Todo management app, needs user auth / todo CRUD / category feature"
```

**⚠️ Context Window Management:**
Project Planner executes work in **3 phases**:

- **Phase 1**: Project analysis → Feature breakdown → Plan approval → Save to `tickets/.plan-{timestamp}.json`
- **Phase 2**: Read plan file → Create ticket files (in batches of 5)
- **Phase 3**: Write log

The agent will present a feature list and priorities, then ask for approval. After approval, ticket files are created in `tickets/`.

```
tickets/
├── PLAN-001-user-auth.md
├── PLAN-002-todo-crud.md
├── PLAN-003-category.md
└── .plan-20260309-103000.json  # Temporary plan file (auto-deleted after completion)
```

**Interruption/Resume:**
If work is interrupted due to context window overflow:

```bash
# Resume from Phase 2 (when plan file already exists)
bash scripts/run-agent.sh project-planner --resume
```

Review the generated files and edit as needed.

#### 2. Continue with Method B below

---

### Method B — Start with Ticket Files

#### 1. Prepare Ticket Files

Place Jira tickets or manually written `.md` files in `tickets/`.

#### 2. Run PM Agent

```bash
bash scripts/run-agent.sh pm --ticket-file ./tickets/PLAN-001-user-auth.md
```

The PM Agent will generate all requirement artifacts and ask for your approval before writing any files.

**Review the outputs:**
- `be-api-requirements/PLAN-001-*.md` — API spec
- `fe-ui-requirements/PLAN-001-*.md` — UI spec
- `fe-ui-requirements/PLAN-001-*.html` — Wireframe (open in browser to inspect interactions)
- `be-test-cases/PLAN-001-*.md` — BE test cases
- `fe-test-cases/PLAN-001-*.md` — FE test cases

Edit any file as needed before proceeding.

#### 3. Run Coding Agents

```bash
bash scripts/run-agent.sh be-coding --ticket PLAN-001
bash scripts/run-agent.sh fe-coding --ticket PLAN-001
```

Each agent will present an implementation plan for your approval before writing any code.

#### 4. Run QA Agents

```bash
bash scripts/run-agent.sh qa-be --ticket PLAN-001
bash scripts/run-agent.sh qa-fe --ticket PLAN-001
```

#### 5. View Logs

```bash
bash scripts/show-logs.sh          # All agents
bash scripts/show-logs.sh be-coding  # Specific agent
```

---

## Wireframe HTML Convention

PM Agent generates interactive wireframes for screens with user flows.

**Static HTML** — for simple display screens with no state transitions.

**Interactive HTML** — for screens with:
- Form submission and page transitions
- Success / failure state display
- Modals, toasts, drawers
- Tabs, steps, or wizards

Interactive wireframes use vanilla JS only (no frameworks, no external libraries). Each state is represented as a `div` with `id="state-{name}"`, toggled via `display:none/block`. API calls are simulated — no real `fetch` calls.

FE Coding Agent reads these wireframes to map states to React `useState` and router transitions.

---

## Git Branch Workflow

Coding agents automatically create and switch to ticket-specific branches before starting work.

### Configuration

Configure branch strategy in `.config/git-workflow.json`:

```json
{
  "branch_strategy": {
    "enabled": true,
    "base_branch": "dev",
    "auto_create": true,
    "auto_checkout": true
  }
}
```

### Branch Naming Convention

| Agent | Branch Pattern | Example |
|-------|---------------|---------|
| `be-coding` | `feature/be/{ticket-number}-{slug}` | `feature/be/PLAN-001-user-auth` |
| `fe-coding` | `feature/fe/{ticket-number}-{slug}` | `feature/fe/PLAN-001-user-auth` |
| `qa-be` | `test/be/{ticket-number}-{slug}` | `test/be/PLAN-001-user-auth` |
| `qa-fe` | `test/fe/{ticket-number}-{slug}` | `test/fe/PLAN-001-user-auth` |

### Automatic Behavior

#### On Work Start
1. Fetch configured base branch (default: `dev`)
2. Create ticket-specific branch if it doesn't exist
3. Automatically switch to that branch
4. Auto-stash uncommitted changes if any

#### On Work Completion
- Agent does **not** commit (human reviews code first)
- Provides next step guidance (commit command examples)

### Manual Branch Management

```bash
# Prepare branch (auto-executed by agents)
bash scripts/git-branch-helper.sh prepare be-coding PLAN-001 user-auth

# Check current Git status
bash scripts/git-branch-helper.sh status

# View configuration
bash scripts/git-branch-helper.sh config
```

### Typical Workflow

```bash
# 1. Run BE coding agent
bash scripts/run-agent.sh be-coding --ticket PLAN-001
# → Auto-creates/switches to feature/be/PLAN-001-user-auth
# → Implements code

# 2. Review and commit
git add .
git commit -m "feat(PLAN-001): Implement user auth API"

# 3. Run FE coding agent
bash scripts/run-agent.sh fe-coding --ticket PLAN-001
# → Auto-creates/switches to feature/fe/PLAN-001-user-auth
# → Implements code

# 4. Review and commit
git add .
git commit -m "feat(PLAN-001): Implement user auth UI"

# 5. Push and create PR
git push origin feature/be/PLAN-001-user-auth
git push origin feature/fe/PLAN-001-user-auth
# Create PR on GitHub
```

### Disable Branch Strategy

If you don't want automatic branch management:

```json
{
  "branch_strategy": {
    "enabled": false
  }
}
```

---

## File Naming Convention

All artifacts are prefixed with the Jira ticket number to prevent cross-ticket confusion.

```
{ticket-number}-{feature-slug}.{ext}

Examples:
  PROJ-123-user-login.md
  PROJ-123-user-login.html
  PROJ-124-product-list.md
```

---

## Rate Limit Handling

This system is designed for **Claude Max 5x** (5-hour rolling window).

Every agent runs `rate-limit-check.sh` before starting work:

| Result | Action |
|--------|--------|
| ✅ Available | Proceed |
| ⚠️ Warning (≥35 calls) | Notify user, proceed with approval |
| 🛑 Stop (≥45 calls) | Halt, show estimated reset time |

To check current usage manually:

```bash
bash scripts/rate-limit-check.sh
```

Thresholds can be adjusted in `scripts/parse_usage.py`:
```python
WARN_THRESHOLD = 35
STOP_THRESHOLD = 45
```

---

## Coding Standards

Agents do not have coding rules embedded in their `CLAUDE.md` files. All standards are delegated to:

- `.rules/be-coding-rules.md` — FastAPI / Python / PostgreSQL standards
- `.rules/fe-coding-rules.md` — Next.js / React / TypeScript standards

This separation means you can update coding rules without touching agent workflow instructions.

---

## Implementation Logs

Every agent writes a log immediately after completing work. Logs include:

- Files created or modified
- Key decisions made (e.g. Server vs Client Component, data fetching strategy)
- Alternative approaches considered and trade-offs
- Notes for the reviewer

Logs are stored in `logs/{agent-name}/` and named with a timestamp and ticket number:

```
logs/project-planner/20250306-143022-todo-app.md
logs/fe-coding/20250306-143022-PLAN-001-user-auth.md
```