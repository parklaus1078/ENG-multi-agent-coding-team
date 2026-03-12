# Scripts Directory

Collection of multi-agent system utility scripts.

**Where to run**: Run from the `team/` directory.

```bash
cd team
bash scripts/run-agent.sh coding --ticket PLAN-001
```

---

## 📋 Script List

### Project Management

#### `init-project.sh`
Initialize a project.

```bash
# Interactive mode
bash scripts/init-project.sh --interactive

# Flag mode
bash scripts/init-project.sh \
  --type cli-tool \
  --language go \
  --framework cobra \
  --name my-cli-tool
```

#### `switch-project.sh`
Switch projects.

```bash
# List projects
bash scripts/switch-project.sh --list

# Switch project
bash scripts/switch-project.sh my-cli-tool
```

---

### Run Agents

#### `run-agent.sh`
Agent runner wrapper (automatically detects current active project).

```bash
# Stack Initializer
bash scripts/run-agent.sh stack-initializer

# Project Planner
bash scripts/run-agent.sh project-planner --project "Project description"

# PM (automatic Git branch creation)
bash scripts/run-agent.sh pm --ticket-file projects/{name}/planning/tickets/PLAN-001-*.md

# Coding (automatic Git branch creation)
bash scripts/run-agent.sh coding --ticket PLAN-001

# QA (automatic Git branch creation)
bash scripts/run-agent.sh qa --ticket PLAN-001
```

**Key features:**
- Automatically detects `current_project` from `.project-config.json`
- Automatically creates/switches Git branches based on ticket number when running PM, Coding, QA
- Continues work even if branch creation fails

---

### Logs & Monitoring

#### `show-logs.sh`
View agent logs (v2.0).

```bash
# All logs for the current project
bash scripts/show-logs.sh

# Only a specific agent
bash scripts/show-logs.sh coding

# Logs for all projects
bash scripts/show-logs.sh --all
```

#### `rate-limit-check.sh`
Check Claude API rate limits.

```bash
bash scripts/rate-limit-check.sh [agent_name]
```

#### `parse_usage.py`
Parse API usage (internal use).

---

### Git Management

#### `git-branch-helper.sh`
Automatic Git branch management.

```bash
# Prepare branch
bash scripts/git-branch-helper.sh prepare coding PLAN-001 user-auth

# Check current status
bash scripts/git-branch-helper.sh status

# Show configuration
bash scripts/git-branch-helper.sh config
```

---

### System Development

#### `create-dev-log.sh`
Create system development logs (for improving the agent system itself).

```bash
bash scripts/create-dev-log.sh git-workflow-automation
```

---


## 📊 Differences Between v1.0 and v2.0

| Script            | v1.0                                      | v2.0                         | Change                          |
|-------------------|-------------------------------------------|------------------------------|---------------------------------|
| `init-project.sh` | Creates `applications/`, `planning-materials/` | Creates `projects/{name}/` | Project isolation, type-based dynamic structure |

---

## 🚀 Getting Started

Start a new project:

```bash
cd team
bash scripts/init-project.sh --interactive
```

---

## 🛠️ Script Development Guide

### Common Pattern

```bash
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$WORKSPACE_ROOT/.project-config.json"

# Read current project
CURRENT_PROJECT=$(grep -o '"current_project": *"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)
PROJECT_PATH="$WORKSPACE_ROOT/projects/$CURRENT_PROJECT"
```

### Project Path Rules

All projects are isolated under the `projects/{current_project}/` directory.

---

---

## 🔑 Core Concepts

### Project Git Repositories

Each project is managed as an **independent Git repository**:

```
team/projects/
├── my-todo-app/
│   ├── .git/                    # ← Git repository for project A
│   └── src/
└── my-blog/
    ├── .git/                    # ← Git repository for project B
    └── src/
```

### Git Branch Work

`git-branch-helper.sh` and `run-agent.sh` perform Git operations **inside the project repository**.

```bash
cd team
bash scripts/run-agent.sh coding --ticket PLAN-001

# Internally:
# 1. Create feature/PLAN-001-xxx branch in projects/{current_project}/.git
# 2. Switch to that branch
# 3. Write code
```

---

**Last updated**: 2026-03-12
**Version**: v0.0.2
