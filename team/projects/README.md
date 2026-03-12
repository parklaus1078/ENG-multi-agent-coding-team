# Projects Directory

This directory contains all projects.

**Important:** Each project is managed as an **independent Git repository** and has different structures based on project type.

---

## 📂 Structure

```
projects/
├── {project-name-1}/
│   ├── .git/                       # ← Project A's Git repository
│   ├── .project-meta.json          # Project metadata
│   ├── planning/                   # Planning documents
│   │   ├── tickets/
│   │   ├── specs/
│   │   └── test-cases/
│   ├── src/                        # Actual code
│   ├── logs/                       # Agent logs
│   └── README.md
├── {project-name-2}/
│   ├── .git/                       # ← Project B's Git repository
│   └── ...
└── README.md                       # This file
```

---

## 🚀 Create New Project

```bash
cd team
bash scripts/init-project.sh --interactive
```

Or using flags:

```bash
bash scripts/init-project.sh \
  --type cli-tool \
  --language go \
  --framework cobra \
  --name my-cli-tool
```

---

## 🔄 Switch Projects

```bash
# List projects
ls projects/

# Switch to specific project
bash scripts/switch-project.sh my-cli-tool
```

---

## 📋 Project Metadata

Each project includes a `.project-meta.json` file:

```json
{
  "project_name": "my-cli-tool",
  "project_type": "cli-tool",
  "stack": {
    "language": "go",
    "framework": "cobra",
    "version": "latest"
  },
  "created_at": "2026-03-12T10:00:00Z",
  "directory_structure": "cli-tool",
  "active": true
}
```

---

## 🗂️ Structure by Project Type

### Web Fullstack

```
planning/specs/
├── backend/
└── frontend/
```

### Web MVC

```
planning/specs/
├── endpoints/
└── templates/
```

### CLI Tool

```
planning/specs/
└── (flat structure)
```

### Desktop App

```
planning/specs/
├── screens/
├── state/
└── ipc/
```

### Library

```
planning/specs/
├── api/
└── examples/
```

### Data Pipeline

```
planning/specs/
├── dags/
├── transforms/
└── schedules/
```

---

## 📝 Workflow Example

### 1. Create Project

```bash
bash scripts/init-project.sh --type cli-tool --language go --framework cobra --name file-search
```

### 2. Initialize Git Repository

```bash
cd projects/file-search
git init
git add .
git commit -m "chore: initial project structure"
git remote add origin https://github.com/your-username/file-search.git
git push -u origin main
cd ../..
```

### 3. Create Tickets

```bash
bash scripts/run-agent.sh project-planner --project "File search CLI"
```

### 4. Generate Specifications (auto-create Git branch)

```bash
bash scripts/run-agent.sh pm --ticket-file projects/file-search/planning/tickets/PLAN-001-search.md
# → Auto-creates docs/PLAN-001-search branch in projects/file-search/.git
```

### 5. Coding (auto-create Git branch)

```bash
bash scripts/run-agent.sh coding --ticket PLAN-001
# → Auto-creates feature/PLAN-001-search branch in projects/file-search/.git
```

### 6. Testing (auto-create Git branch)

```bash
bash scripts/run-agent.sh qa --ticket PLAN-001
# → Auto-creates test/PLAN-001-search branch in projects/file-search/.git
```

### 7. Commit and Push

```bash
cd projects/file-search
git add .
git commit -m "feat(PLAN-001): implement file search feature and tests"
git push origin feature/PLAN-001-search
cd ../..
```

---

## 🔍 Check Project Status

```bash
# Current active project
cat ../.project-config.json

# Specific project metadata
cat projects/my-cli-tool/.project-meta.json

# Project logs
bash scripts/show-logs.sh
```

---

**Last Updated**: 2026-03-12
