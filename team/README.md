# Team Working Directory

This directory is the **working directory** for the multi-agent system. All commands are executed here.

---

## 📍 Current Location

```
KR-multi-agent-coding-team/          # System root
└── team/                            # ← here (working directory)
```

---

## 🚀 Quick Start

### 1. Initialize a project

```bash
bash scripts/init-project.sh --interactive
```

### 2. Initialize the project Git repository

```bash
cd projects/{your-project-name}
git init
git remote add origin https://github.com/your-username/{your-project-name}.git
cd ../..
```

### 3. Agent workflow

```bash
# Initialize stack
bash scripts/run-agent.sh stack-initializer

# Create ticket
bash scripts/run-agent.sh project-planner --project "Project description"

# Write specification
bash scripts/run-agent.sh pm --ticket-file projects/{name}/planning/tickets/PLAN-001-*.md

# Coding
bash scripts/run-agent.sh coding --ticket PLAN-001

# Testing
bash scripts/run-agent.sh qa --ticket PLAN-001
```

---

## 📁 Directory Structure

```
team/
├── .agents/                         # Agent definitions (5)
│   ├── stack-initializer/
│   ├── project-planner/
│   ├── pm/
│   ├── coding/
│   └── qa/
│
├── .rules/                          # Coding rules
│   ├── general-coding-rules.md      # General principles
│   ├── _cache/                      # AI auto-generated (24h)
│   └── _verified/                   # Human-verified
│
├── .config/                         # System settings
│   └── git-workflow.json
│
├── scripts/                         # Utility scripts
│   ├── init-project.sh              # Project initialization
│   ├── switch-project.sh            # Switch project
│   ├── run-agent.sh                 # Run agents
│   ├── show-logs.sh                 # View logs
│   ├── git-branch-helper.sh         # Git branch management
│   └── rate-limit-check.sh          # Rate limit check
│
├── projects/                        # Project workspace
│   ├── project-a/                   # Each project is an independent Git repo
│   │   ├── .project-meta.json       # Project stack settings
│   │   ├── .git/                    # ← Project’s own Git
│   │   ├── planning/
│   │   ├── src/
│   │   └── logs/
│   └── project-b/
│       └── ...
│
├── .project-config.json             # Current active project
└── README.md                        # This file
```

---

## 🔄 Switch Projects

You can manage multiple projects within a single system:

```bash
# Project list
bash scripts/switch-project.sh --list

# Switch project
bash scripts/switch-project.sh project-b

# Now all commands run in the context of project-b
bash scripts/run-agent.sh coding --ticket PLAN-005
```

---

## 📚 Detailed Documentation

- [Root README.md](../README.md) - System overview
- [Scripts Guide](scripts/README.md) - Usage for each script
- [Coding Rules Guide](.rules/README.md) - Coding rules system
- [Architecture document](../docs/architecture-final.md) - Detailed architecture

---

**Version**: v0.0.2
**Last updated**: 2026-03-12
