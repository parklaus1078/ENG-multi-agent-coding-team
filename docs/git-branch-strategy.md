# Git Branch Strategy

Detailed guide for the multi-agent system's Git branch strategy

---

## 📌 Core Principles

### Branch Flow

```
main/dev (base branch)
  │
  ├─ docs/PLAN-001-xxx        (PM Agent)
  │
  └─ feature/PLAN-001-xxx     (Coding Agent)
       │
       └─ test/PLAN-001-xxx   (QA Agent)
```

**Important:**
- **PM, Coding Agent**: Branch from `base_branch` (main/dev)
- **QA Agent**: Branch from **feature branch** of the same ticket

---

## 🌿 Branch Strategy by Agent

### 1. PM Agent

**Branch Pattern**: `docs/{ticket-number}-{slug}`

**Base**: base_branch (main/dev)

**Example**:
```bash
bash scripts/run-agent.sh pm --ticket-file projects/my-app/planning/tickets/PLAN-001-user-auth.md
# → Creates docs/PLAN-001-user-auth branch from main
```

**Purpose**: Write specifications and test cases

---

### 2. Coding Agent

**Branch Pattern**: `feature/{ticket-number}-{slug}`

**Base**: base_branch (main/dev)

**Example**:
```bash
bash scripts/run-agent.sh coding --ticket PLAN-001
# → Creates feature/PLAN-001-user-auth branch from main
```

**Purpose**: Implement actual code

---

### 3. QA Agent

**Branch Pattern**: `test/{ticket-number}-{slug}`

**Base**: **feature branch** (same ticket)

**Example**:
```bash
bash scripts/run-agent.sh qa --ticket PLAN-001
# → Creates test/PLAN-001-user-auth branch from feature/PLAN-001-user-auth
```

**Purpose**: Write test code

**Important Notes**:
- Coding Agent must be run before QA Agent
- If feature branch doesn't exist, displays warning and uses base_branch

---

## 🔄 Complete Workflow Example

### Scenario: PLAN-001 User Authentication Feature Development

```bash
cd team

# 1. PM Agent: Write specifications
bash scripts/run-agent.sh pm --ticket-file projects/my-app/planning/tickets/PLAN-001-user-auth.md
# → Creates docs/PLAN-001-user-auth branch (from main)

cd projects/my-app
git add .
git commit -m "docs(PLAN-001): write user authentication specifications"
git push origin docs/PLAN-001-user-auth
cd ../..

# 2. Coding Agent: Implement code
bash scripts/run-agent.sh coding --ticket PLAN-001
# → Creates feature/PLAN-001-user-auth branch (from main)

cd projects/my-app
git add .
git commit -m "feat(PLAN-001): implement user authentication"
git push origin feature/PLAN-001-user-auth
cd ../..

# 3. QA Agent: Write tests
bash scripts/run-agent.sh qa --ticket PLAN-001
# → Creates test/PLAN-001-user-auth branch (from feature/PLAN-001-user-auth)

cd projects/my-app
git add .
git commit -m "test(PLAN-001): write user authentication tests"
git push origin test/PLAN-001-user-auth
cd ../..
```

### Branch Structure (Final)

```
my-app/.git/
├── main
├── docs/PLAN-001-user-auth           (from main)
├── feature/PLAN-001-user-auth        (from main)
└── test/PLAN-001-user-auth           (from feature/PLAN-001-user-auth)
```

---

## ⚙️ Configuration File

### `.config/git-workflow.json`

```json
{
  "branch_strategy": {
    "enabled": true,
    "base_branch": "main",
    "auto_create": true,
    "auto_checkout": true
  },
  "branch_naming": {
    "base_branch_by_agent": {
      "pm": "base_branch",
      "coding": "base_branch",
      "qa": "feature_branch"
    }
  }
}
```

**Key Settings**:
- `base_branch`: Base branch for PM/Coding (main, dev, etc.)
- `qa`: Uses feature_branch (same ticket)

---

## 🔧 Manual Branch Management

### Prepare Branch (Automatically run by agents)

```bash
# For Coding Agent
bash scripts/git-branch-helper.sh prepare coding PLAN-001 user-auth
# → Creates feature/PLAN-001-user-auth from main

# For QA Agent
bash scripts/git-branch-helper.sh prepare qa PLAN-001 user-auth
# → Creates test/PLAN-001-user-auth from feature/PLAN-001-user-auth
```

### Check Current Status

```bash
bash scripts/git-branch-helper.sh status
```

### Check Configuration

```bash
bash scripts/git-branch-helper.sh config
```

---

## 🚨 Warnings

### 1. QA Agent Execution Order

❌ **Wrong Order**:
```bash
bash scripts/run-agent.sh qa --ticket PLAN-001
# No feature branch → warning
```

✅ **Correct Order**:
```bash
bash scripts/run-agent.sh coding --ticket PLAN-001
# Creates feature branch

bash scripts/run-agent.sh qa --ticket PLAN-001
# Creates test branch from feature branch
```

### 2. Changing Base Branch

To use dev branch:

```json
{
  "branch_strategy": {
    "base_branch": "dev"
  }
}
```

### 3. Per-Project Git

Each project is an independent Git repository:

```
team/projects/
├── my-app/.git/           # Project A Git
└── my-blog/.git/          # Project B Git
```

Branch operations are performed **within the project repository**.

---

## 📋 Branch Naming Rules

### Pattern

```
{prefix}/{ticket-number}-{slug}
```

### Examples

| Ticket | PM | Coding | QA |
|--------|-------|--------|-----|
| PLAN-001-user-auth | `docs/PLAN-001-user-auth` | `feature/PLAN-001-user-auth` | `test/PLAN-001-user-auth` |
| PLAN-002-todo-crud | `docs/PLAN-002-todo-crud` | `feature/PLAN-002-todo-crud` | `test/PLAN-002-todo-crud` |

### Slug Extraction

Automatically extracted from ticket filename:
- `PLAN-001-user-auth.md` → slug: `user-auth`
- `PLAN-002-todo-crud.md` → slug: `todo-crud`

---

## 🔀 PR (Pull Request) Strategy

### 1. Feature → Main

```bash
cd projects/my-app
git checkout feature/PLAN-001-user-auth
git push origin feature/PLAN-001-user-auth
# GitHub PR: feature/PLAN-001-user-auth → main
```

### 2. Test → Feature (Optional)

Manage tests as separate PR:

```bash
cd projects/my-app
git checkout test/PLAN-001-user-auth
git push origin test/PLAN-001-user-auth
# GitHub PR: test/PLAN-001-user-auth → feature/PLAN-001-user-auth
```

### 3. Feature + Test → Main (Recommended)

Merge test branch into feature branch, then PR:

```bash
cd projects/my-app
git checkout feature/PLAN-001-user-auth
git merge test/PLAN-001-user-auth
git push origin feature/PLAN-001-user-auth
# GitHub PR: feature/PLAN-001-user-auth → main
```

---

## 🛠️ Troubleshooting

### Q1. I ran QA without a feature branch

**Symptom**:
```
⚠️  Feature branch not found: feature/PLAN-001-user-auth
   Run coding agent first.
   Or using default base branch: main
```

**Solution**:
1. Run Coding Agent first
2. Or create test branch from main (not recommended)

### Q2. Branches aren't created automatically

**Check**:
```bash
# Check configuration
cat .config/git-workflow.json

# Verify auto_create is true
```

### Q3. I want to use a different base branch

**Solution**:
```json
{
  "branch_strategy": {
    "base_branch": "develop"
  }
}
```

---

**Version**: v0.0.2
**Last Updated**: 2026-03-12
