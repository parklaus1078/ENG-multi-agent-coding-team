# Multi-Agent Coding Team

> Tech Stack Agnostic Multi-Agent Development System

[![Version](https://img.shields.io/badge/version-v0.0.2-blue.svg)](https://github.com/your-repo)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-beta-orange.svg)]()

A Claude Code-based multi-agent system that automates the development cycle from project idea to implementation and testing completion.

---

## ⚠️ Beta Version Warnings

Currently at **v0.0.2 beta**. Please note:

- May consume Claude API tokens excessively depending on usage patterns
- Can be interrupted by context window overflow if tasks aren't broken into smaller units
- Thorough testing recommended before production use

---

## 🎯 Core Concepts

### 1. Multi-Agent System = Tool

This repository is a **development tool**. Your actual project code is managed in separate repositories.

```
ENG-multi-agent-coding-team/         # ← Multi-agent system (this repository)
└── team/                             # Working directory
    ├── scripts/                      # Agent execution scripts
    ├── .agents/                      # 5 unified agents
    └── projects/                     # Project workspace
        ├── my-todo-app/              # ← Project A (independent Git repo)
        │   ├── .git/
        │   ├── planning/
        │   └── src/
        └── my-blog/                  # ← Project B (independent Git repo)
            ├── .git/
            ├── planning/
            └── src/
```

### 2. Tech Stack Agnostic

Supports all languages and all frameworks:
- **Web Fullstack**: Express+React, Django+Vue, FastAPI+Next.js, etc.
- **Web MVC**: Django, Rails, Spring Boot, etc.
- **CLI Tool**: Click, Cobra, Clap, etc.
- **Desktop App**: Tauri, Electron, Qt, etc.
- **Mobile App**: React Native, Flutter, etc.
- **Library**: npm, pip, cargo packages, etc.
- **Data Pipeline**: Airflow, Prefect, etc.

### 3. Project Isolation

Each project is created independently in `team/projects/{name}/` directory and **managed as separate Git repositories**.

---

## 📦 Prerequisites

- [Claude Code](https://docs.claude.ai/claude-code) installed and logged in
- Python 3 (for rate limit tracking)
- Git
- Claude Pro plan or higher recommended

---

## 🚀 Quick Start

### 1. Clone the System

```bash
git clone https://github.com/your-username/ENG-multi-agent-coding-team.git
cd ENG-multi-agent-coding-team/team
```

### 2. Create Your First Project

```bash
# Initialize project in interactive mode
bash scripts/init-project.sh --interactive
```

Select in interactive mode:
- Project type: web-fullstack, cli-tool, desktop-app, etc.
- Language: Python, Go, TypeScript, etc.
- Framework: FastAPI, Cobra, Tauri, etc.
- Project name: my-todo-app

### 3. Initialize Project Git Repository

```bash
# Navigate to the created project directory
cd projects/my-todo-app

# Initialize Git repository
git init
git add .
git commit -m "chore: initial project structure"

# Connect to remote repository (optional)
git remote add origin https://github.com/your-username/my-todo-app.git
git branch -M main
git push -u origin main

# Return to working directory
cd ../..
```

### 4. Run Stack Initializer (Auto-Generate Coding Rules)

```bash
bash scripts/run-agent.sh stack-initializer
```

Stack Initializer:
- Analyzes official documentation of selected framework
- Auto-generates coding rules based on best practices
- Saves to `.rules/_cache/` (24-hour cache)

### 5. Create Tickets

```bash
bash scripts/run-agent.sh project-planner --project "Todo management app: user auth, todo CRUD, category features"
```

Output:
```
projects/my-todo-app/planning/tickets/
├── PLAN-001-user-auth.md
├── PLAN-002-todo-crud.md
└── PLAN-003-category.md
```

### 6. Generate Specifications (Auto Branch Creation)

```bash
bash scripts/run-agent.sh pm --ticket-file projects/my-todo-app/planning/tickets/PLAN-001-user-auth.md
```

Automatic actions:
1. Auto-creates/switches to `docs/PLAN-001-user-auth` branch
2. Writes specifications:
   - `planning/specs/` (dynamic structure based on project type)
   - `planning/test-cases/`

### 7. Coding (Auto Branch Creation)

```bash
bash scripts/run-agent.sh coding --ticket PLAN-001
```

Automatic actions:
1. Auto-creates/switches to `feature/PLAN-001-user-auth` branch
2. Implements code
3. Writes implementation log

### 8. Write Tests (Auto Branch Creation)

```bash
bash scripts/run-agent.sh qa --ticket PLAN-001
```

Automatic actions:
1. Auto-creates/switches to `test/PLAN-001-user-auth` branch
2. Writes test code
3. Writes test log

### 9. Commit and Push

```bash
# Navigate to project directory
cd projects/my-todo-app

# Review code and commit
git add .
git commit -m "feat(PLAN-001): implement user authentication and tests

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Push
git push origin feature/PLAN-001-user-auth

# Return to working directory
cd ../..
```

---

## 🔄 Detailed Workflow

### From Project Idea to Implementation

```
1. Initialize Project
   bash scripts/init-project.sh --interactive
   → creates projects/{name}/

2. Initialize Git Repository (user)
   cd projects/{name}
   git init
   cd ../..

3. Stack Initializer (auto-generate coding rules)
   bash scripts/run-agent.sh stack-initializer

4. Project Planner (create tickets)
   bash scripts/run-agent.sh project-planner --project "project description"
   → planning/tickets/PLAN-XXX-*.md

5. PM Agent (generate specifications)
   bash scripts/run-agent.sh pm --ticket-file projects/{name}/planning/tickets/PLAN-001-*.md
   → Auto-creates Git branch: docs/PLAN-001-xxx
   → Creates planning/specs/ and planning/test-cases/

6. Coding Agent (implement code)
   bash scripts/run-agent.sh coding --ticket PLAN-001
   → Auto-creates Git branch: feature/PLAN-001-xxx
   → Writes src/ code

7. QA Agent (write tests)
   bash scripts/run-agent.sh qa --ticket PLAN-001
   → Auto-creates Git branch: test/PLAN-001-xxx
   → Writes test code

8. Commit and Push (user)
   cd projects/{name}
   git add .
   git commit -m "feat(PLAN-001): implementation complete"
   git push origin feature/PLAN-001-xxx
```

---

## 🤖 Agent List

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| `stack-initializer` | Stack initialization | `.project-meta.json` | Coding rules, project structure |
| `project-planner` | Project decomposition | Natural language description | `planning/tickets/PLAN-XXX-*.md` |
| `pm` | Requirements documentation | Ticket `.md` | Specifications, test cases |
| `coding` | Code implementation (all stacks) | Specifications | `src/` code |
| `qa` | Test writing (all stacks) | Test cases | Test code |

**Total 5 unified agents** - automatically branches based on project type

---

## 📁 Project Structure (Dynamically Generated by Type)

### Web Fullstack (e.g., FastAPI + Next.js)

```
projects/my-todo-app/
├── .git/                           # Project Git repository
├── .project-meta.json              # Project metadata
├── planning/
│   ├── tickets/                    # Ticket files
│   ├── specs/
│   │   ├── backend/                # API specifications
│   │   └── frontend/               # UI specifications
│   └── test-cases/
│       ├── backend/
│       └── frontend/
├── src/
│   ├── backend/                    # FastAPI code
│   └── frontend/                   # Next.js code
└── logs/                           # Agent implementation logs
    ├── coding/
    └── qa/
```

### CLI Tool (e.g., Go + Cobra)

```
projects/file-search-cli/
├── .git/
├── .project-meta.json
├── planning/
│   ├── tickets/
│   ├── specs/                      # Command specifications
│   └── test-cases/
├── src/
│   ├── cmd/                        # Command implementation
│   └── internal/                   # Internal logic
└── logs/
```

### Desktop App (e.g., Tauri + React)

```
projects/notes-app/
├── .git/
├── .project-meta.json
├── planning/
│   ├── tickets/
│   ├── specs/
│   │   ├── screens/                # Screen specifications
│   │   ├── state/                  # State management
│   │   └── ipc/                    # IPC communication
│   └── test-cases/
│       ├── unit/
│       ├── integration/
│       └── e2e/
├── src/
│   ├── src-tauri/                  # Rust backend
│   └── src/                        # React frontend
└── logs/
```

---

## 🔀 Multi-Project Management

### Switch Projects

```bash
# List projects
bash scripts/switch-project.sh --list

# Switch project
bash scripts/switch-project.sh my-blog

# Now all commands run in my-blog context
bash scripts/run-agent.sh coding --ticket PLAN-005
```

### Auto Project Context Recognition

Automatically recognizes projects by reading `current_project` value in `.project-config.json`.

```json
{
  "current_project": "my-todo-app",
  "current_project_path": "projects/my-todo-app",
  "recent_projects": ["my-todo-app", "my-blog"]
}
```

---

## 🌿 Git Branch Strategy

### Auto Branch Creation

PM, Coding, QA Agents **automatically create/switch branches based on ticket numbers**:

| Agent | Branch Pattern | Base Branch | Example |
|-------|---------------|-------------|---------|
| `pm` | `docs/{ticket-number}-{slug}` | base_branch (main/dev) | `docs/PLAN-001-user-auth` |
| `coding` | `feature/{ticket-number}-{slug}` | base_branch (main/dev) | `feature/PLAN-001-user-auth` |
| `qa` | `test/{ticket-number}-{slug}` | **feature branch** | `test/PLAN-001-user-auth` |

**Important:** QA Agent creates test branch based on the feature branch of the same ticket.

### Git Work Location

**Important:** Git operations are performed **within the project repository**.

```bash
# System is in team/, but Git branches are created in projects/{name}/.git
cd team
bash scripts/run-agent.sh coding --ticket PLAN-001

# Internal operations:
# 1. Create feature/PLAN-001-xxx branch in projects/my-todo-app/.git
# 2. Switch to that branch
# 3. Write code
```

### Branch Configuration

`.config/git-workflow.json`:

```json
{
  "branch_strategy": {
    "enabled": true,
    "base_branch": "main",
    "auto_create": true,
    "auto_checkout": true
  },
  "safety": {
    "check_uncommitted_changes": true,
    "stash_before_checkout": true
  }
}
```

---

## ⚡ Rate Limit Management

All agents automatically check rate limits before starting work.

### Thresholds

| Status | Usage | Action |
|--------|-------|--------|
| ✅ Available | 0-34 requests | Proceed with work |
| ⚠️ Warning | 35-44 requests | Notify user, proceed with consent |
| 🛑 Stop | 45+ requests | Stop immediately, show resume time |

### Manual Check

```bash
bash scripts/rate-limit-check.sh
```

Adjust thresholds: `scripts/parse_usage.py`

---

## 📚 Coding Rules System

### Auto-Generated vs Verified Rules

```
.rules/
├── general-coding-rules.md         # Universal principles (DRY, SOLID, etc.)
├── _cache/                          # AI auto-generated (24-hour cache)
│   └── cli-tool-cobra-go.md
└── _verified/                       # Human-verified rules
    └── web-fullstack/
        ├── backend-fastapi-python.md
        └── frontend-nextjs-typescript.md
```

### Stack Initializer Workflow

1. Analyze framework official documentation (WebFetch/WebSearch)
2. Extract best practices
3. Auto-generate coding rules → `.rules/_cache/`
4. After user verification → promote to `.rules/_verified/`

---

## 📖 Logging System

All agents write implementation logs after completing work.

### Log Location

```
projects/{name}/logs/{agent}/
└── 20260312-143022-PLAN-001-user-auth.md
```

### Log Contents

- List of created/modified files
- Key decisions and trade-offs
- Considered alternatives
- Notes for reviewers

### View Logs

```bash
# All logs for current project
bash scripts/show-logs.sh

# Specific agent only
bash scripts/show-logs.sh coding

# All projects' logs
bash scripts/show-logs.sh --all
```

---

## 🛠️ Advanced Usage

### Initialize Project with Flags

```bash
bash scripts/init-project.sh \
  --type cli-tool \
  --language go \
  --framework cobra \
  --name file-search-cli \
  --description "Fast file search tool"
```

### Project Planner Resume Mode

If interrupted by context window overflow:

```bash
bash scripts/run-agent.sh project-planner --resume
```

### Manual Branch Management

```bash
# Prepare branch
bash scripts/git-branch-helper.sh prepare coding PLAN-001 user-auth

# Check current status
bash scripts/git-branch-helper.sh status

# Check configuration
bash scripts/git-branch-helper.sh config
```

---

## 📂 Complete Directory Structure

```
ENG-multi-agent-coding-team/          # Multi-agent system (this repository)
├── .git/                              # System Git
├── README.md                          # This file
├── LICENSE
├── docs/                              # Architecture documentation
│   ├── architecture.md
│   └── supported-tech-stacks.md
├── logs-agent_dev/                    # System development logs
└── team/                              # ← Working directory (run commands here)
    ├── .agents/                       # Agent definitions (CLAUDE.md)
    │   ├── stack-initializer/
    │   ├── project-planner/
    │   ├── pm/
    │   ├── coding/
    │   └── qa/
    ├── .rules/                        # Coding rules
    │   ├── general-coding-rules.md
    │   ├── _cache/                    # AI auto-generated
    │   └── _verified/                 # Human-verified
    ├── .config/                       # System configuration
    │   └── git-workflow.json
    ├── scripts/                       # Utility scripts
    │   ├── init-project.sh
    │   ├── switch-project.sh
    │   ├── run-agent.sh
    │   ├── show-logs.sh
    │   ├── git-branch-helper.sh
    │   └── rate-limit-check.sh
    ├── projects/                      # Project workspace
    │   ├── my-todo-app/               # Project A (independent Git repo)
    │   │   ├── .git/                  # ← Project's own Git
    │   │   ├── .project-meta.json
    │   │   ├── planning/
    │   │   ├── src/
    │   │   └── logs/
    │   └── my-blog/                   # Project B (independent Git repo)
    │       ├── .git/
    │       └── ...
    ├── .project-config.json           # Current active project
    └── .gitignore
```

---

## 🤝 Contributing Guide

### Contributing Verified Coding Rules

You can contribute coding rules for new stacks to `.rules/_verified/`:

1. Generate rules with Stack Initializer
2. Verify in actual projects
3. Submit PR: `.rules/_verified/{project-type}/{framework}.md`

### Contributing Templates

You can contribute new project type templates to `.agents/*/templates/`.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🔗 Related Links

- [Claude Code Documentation](https://docs.claude.ai/claude-code)
- [Supported Tech Stacks](docs/supported-tech-stacks.md)
- [Architecture Details](docs/architecture.md)

---

**Version**: v0.0.2 (beta)
**Last Updated**: 2026-03-12
