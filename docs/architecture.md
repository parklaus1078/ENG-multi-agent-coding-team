# Multi-Agent System Architecture

> Tech Stack Agnostic Universal Multi-Agent Development Workflow

**Version**: v0.0.2
**Last Updated**: 2026-03-12
**Audience**: System Developers

---

## 🎯 Core Design Principles

### 1. **Dynamic Directory Structure**
- Create only necessary directories based on project type
- No fixed directory structure (dynamically generated based on project type)
- All deliverables organized based on project type

### 2. **Project Isolation**
- Each project in independent directory (`team/projects/{project-name}/`)
- **Each project managed as independent Git repository**
- Per-project planning, per-project logs
- Multiple projects can be managed simultaneously

### 3. **Type-Based Structuring**
- web-fullstack → separate `backend/`, `frontend/`
- web-mvc → single `src/` directory
- cli-tool → `cmd/`, `internal/` (Go) or framework-specific structure
- desktop-app → platform-specific structure

---

## 📂 Final Directory Structure

\`\`\`
team/
├── .project-config.json                    # Current active project configuration
├── .project-meta.schema.json               # Configuration schema per Project. The system generates a new project-meta file for each project upon creation, and follows this schema
│
├── .agents/                                 # Agent instruction files
│   ├── stack-initializer/
│   │   └── CLAUDE.md
│   ├── project-planner/
│   │   └── CLAUDE.md
│   ├── pm/
│   │   ├── CLAUDE.md
│   │   └── templates/                       # Type-specific PM templates
│   │       ├── web-fullstack.md
│   │       ├── web-mvc.md
│   │       ├── cli-tool.md
│   │       ├── desktop-app.md
│   │       ├── mobile-app.md
│   │       ├── library.md
│   │       └── data-pipeline.md
│   ├── coding/
│   │   ├── CLAUDE.md
│   │   └── templates/                       # Type-specific coding templates
│   │       ├── web-fullstack.md
│   │       ├── web-mvc.md
│   │       ├── cli-tool.md
│   │       ├── desktop-app.md
│   │       ├── mobile-app.md
│   │       ├── library.md
│   │       └── data-pipeline.md
│   └── qa/
│       ├── CLAUDE.md
│       └── templates/                       # Type-specific QA templates
│           ├── web-fullstack.md
│           ├── web-mvc.md
│           ├── cli-tool.md
│           ├── desktop-app.md
│           ├── mobile-app.md
│           ├── library.md
│           └── data-pipeline.md
│
├── .rules/                                  # Coding rules
│   ├── README.md
│   ├── general-coding-rules.md              # Universal principles
│   ├── _verified/                           # Human-verified rules
│   │   ├── web-fullstack/
│   │   │   ├── backend-fastapi-python.md
│   │   │   └── frontend-nextjs-typescript.md
│   │   ├── web-mvc/
│   │   │   ├── django-python.md
│   │   │   └── springboot-java.md
│   │   ├── cli-tool/
│   │   │   ├── click-python.md
│   │   │   └── cobra-go.md
│   │   ├── desktop-app/
│   │   │   ├── tauri-rust.md
│   │   │   └── electron-typescript.md
│   │   └── ...
│   └── _cache/                              # Auto-generated rules (24 hours)
│       └── (dynamically generated)
│
├── .config/
│   └── git-workflow.json                    # Git branch strategy
│
├── scripts/
│   ├── init-project.sh                      # Project initialization
│   ├── run-agent.sh                         # Agent execution
│   ├── rate-limit-check.sh
│   ├── parse_usage.py
│   ├── show-logs.sh
│   ├── git-branch-helper.sh
│   └── create-dev-log.sh
│
├── projects/                                # 🆕 Project root (replaces applications)
│   ├── my-todo-app/                         # Example: Web Fullstack
│   │   ├── .project-meta.json               # Project metadata
│   │   ├── planning/                        # Planning documents
│   │   │   ├── tickets/
│   │   │   │   ├── PLAN-001-user-auth.md
│   │   │   │   └── PLAN-002-todo-crud.md
│   │   │   ├── specs/                       # Specifications (type-specific structure)
│   │   │   │   ├── backend/
│   │   │   │   │   ├── PLAN-001-api-spec.md
│   │   │   │   │   └── PLAN-002-api-spec.md
│   │   │   │   └── frontend/
│   │   │   │       ├── PLAN-001-ui-spec.md
│   │   │   │       ├── PLAN-001-wireframe.html
│   │   │   │       ├── PLAN-002-ui-spec.md
│   │   │   │       └── PLAN-002-wireframe.html
│   │   │   └── test-cases/                  # Test cases
│   │   │       ├── backend/
│   │   │       │   ├── PLAN-001-tests.md
│   │   │       │   └── PLAN-002-tests.md
│   │   │       └── frontend/
│   │   │           ├── PLAN-001-tests.md
│   │   │           └── PLAN-002-tests.md
│   │   ├── src/                             # Actual code
│   │   │   ├── backend/
│   │   │   │   ├── src/
│   │   │   │   ├── tests/
│   │   │   │   ├── requirements.txt
│   │   │   │   └── .env.example
│   │   │   └── frontend/
│   │   │       ├── src/
│   │   │       ├── public/
│   │   │       ├── package.json
│   │   │       └── .env.example
│   │   ├── logs/                            # Per-project logs
│   │   │   ├── stack-initializer/
│   │   │   ├── project-planner/
│   │   │   ├── pm/
│   │   │   ├── coding/
│   │   │   └── qa/
│   │   └── README.md
│   │
│   ├── file-search-cli/                     # Example: CLI Tool
│   │   ├── .project-meta.json
│   │   ├── planning/
│   │   │   ├── tickets/
│   │   │   │   ├── PLAN-001-search-cmd.md
│   │   │   │   └── PLAN-002-filter-cmd.md
│   │   │   ├── specs/                       # CLI-specific structure
│   │   │   │   ├── PLAN-001-command-spec.md
│   │   │   │   └── PLAN-002-command-spec.md
│   │   │   └── test-cases/
│   │   │       ├── PLAN-001-tests.md
│   │   │       └── PLAN-002-tests.md
│   │   ├── src/                             # Go Cobra structure
│   │   │   ├── cmd/
│   │   │   │   ├── root.go
│   │   │   │   ├── search.go
│   │   │   │   └── filter.go
│   │   │   ├── internal/
│   │   │   ├── go.mod
│   │   │   ├── go.sum
│   │   │   └── main.go
│   │   ├── logs/
│   │   └── README.md
│   │
│   └── admin-dashboard/                     # Example: Web MVC (Django)
│       ├── .project-meta.json
│       ├── planning/
│       │   ├── tickets/
│       │   ├── specs/                       # MVC-specific structure
│       │   │   ├── PLAN-001-endpoint-spec.md
│       │   │   ├── PLAN-001-template-spec.md
│       │   │   └── PLAN-002-endpoint-spec.md
│       │   └── test-cases/
│       │       ├── PLAN-001-tests.md
│       │       └── PLAN-002-tests.md
│       ├── src/                             # Django structure
│       │   ├── manage.py
│       │   ├── config/
│       │   ├── apps/
│       │   ├── templates/
│       │   ├── static/
│       │   └── requirements.txt
│       ├── logs/
│       └── README.md
│
└── docs/                                    # System documentation
    ├── architecture.md                      # This file
    ├── git-branch-strategy.md
    └── supported-tech-stacks.md
\`\`\`

---

## 🔑 Key Changes

### 1. Project Isolation Structure

**Core Principles**:
- Each project in independent directory
- Structure dynamically generated based on project type
- Complete per-project isolation

**Structure**:
\`\`\`
projects/
└── {project-name}/
    ├── .project-meta.json        # Project metadata
    ├── planning/                 # Planning documents (per-project)
    ├── src/                      # Actual code
    └── logs/                     # Logs (per-project)
\`\`\`

### 2. \`.project-meta.json\` (Per-Project Metadata)

Located in each project directory:

\`\`\`json
{
  "project_name": "my-todo-app",
  "project_type": "web-fullstack",
  "stack": {
    "backend": {
      "language": "python",
      "framework": "fastapi",
      "version": "0.110.0"
    },
    "frontend": {
      "language": "typescript",
      "framework": "nextjs",
      "version": "14.0.0"
    }
  },
  "created_at": "2026-03-12T10:00:00Z",
  "directory_structure": "web-fullstack",
  "active": true
}
\`\`\`

### 3. \`.project-config.json\` (Root Level, Current Active Project)

\`\`\`json
{
  "current_project": "my-todo-app",
  "current_project_path": "projects/my-todo-app",
  "recent_projects": [
    "my-todo-app",
    "file-search-cli",
    "admin-dashboard"
  ]
}
\`\`\`

### 4. \`planning/\` Directory Structure (Dynamically Generated by Type)

#### Web Fullstack

\`\`\`
planning/
├── tickets/
├── specs/
│   ├── backend/                  # API specifications
│   └── frontend/                 # UI specifications + wireframes
└── test-cases/
    ├── backend/
    └── frontend/
\`\`\`

#### Web MVC

\`\`\`
planning/
├── tickets/
├── specs/
│   ├── endpoints/                # Endpoint specifications
│   └── templates/                # Template specifications
└── test-cases/
\`\`\`

#### CLI Tool

\`\`\`
planning/
├── tickets/
├── specs/                        # Command specifications (flat structure)
│   ├── PLAN-001-command-spec.md
│   └── PLAN-002-command-spec.md
└── test-cases/
    ├── PLAN-001-tests.md
    └── PLAN-002-tests.md
\`\`\`

#### Desktop App

\`\`\`
planning/
├── tickets/
├── specs/
│   ├── screens/                  # Screen specifications
│   ├── state/                    # State management specifications
│   └── ipc/                      # IPC specifications (Electron/Tauri)
└── test-cases/
    ├── unit/
    ├── integration/
    └── e2e/
\`\`\`

#### Library

\`\`\`
planning/
├── tickets/
├── specs/
│   ├── api/                      # API signatures
│   └── examples/                 # Usage examples
└── test-cases/
\`\`\`

#### Data Pipeline

\`\`\`
planning/
├── tickets/
├── specs/
│   ├── dags/                     # DAG definitions
│   ├── transforms/               # Data transformation logic
│   └── schedules/                # Schedule definitions
└── test-cases/
\`\`\`

---

## 🚀 Workflow (Final)

### 1. Project Initialization

\`\`\`bash
cd team
bash scripts/init-project.sh --interactive
\`\`\`

**Input**:
- Project type: \`cli-tool\`
- Language: \`go\`
- Framework: \`cobra\`
- Project name: \`file-search-cli\`

**Stack Initializer Agent performs**:

1. Create \`projects/file-search-cli/\` directory
2. Generate \`.project-meta.json\`
3. Create \`planning/\` directory (CLI Tool structure)
   \`\`\`
   planning/
   ├── tickets/
   ├── specs/
   └── test-cases/
   \`\`\`
4. Create \`src/\` directory (Go Cobra structure)
   \`\`\`
   src/
   ├── cmd/
   │   └── root.go
   ├── internal/
   ├── go.mod
   └── main.go
   \`\`\`
5. Create \`logs/\` directory
6. Generate \`.rules/_cache/cli-tool/cobra-go.md\` (or use _verified)
7. Update root \`.project-config.json\` (current project configuration)

### 2. Create Tickets

\`\`\`bash
bash scripts/run-agent.sh project-planner \
  --project "Filename search + content search CLI"
\`\`\`

**Output**:
\`\`\`
projects/file-search-cli/planning/tickets/
├── PLAN-001-search-by-name.md
└── PLAN-002-search-by-content.md
\`\`\`

### 3. PM (Generate Specifications)

\`\`\`bash
bash scripts/run-agent.sh pm \
  --ticket-file projects/file-search-cli/planning/tickets/PLAN-001-search-by-name.md
\`\`\`

**PM Agent actions**:
1. Read \`.project-config.json\` → Current project: \`file-search-cli\`
2. Read \`projects/file-search-cli/.project-meta.json\` → Type: \`cli-tool\`
3. Load \`.agents/pm/templates/cli-tool.md\` template
4. Generate specifications:
   \`\`\`
   projects/file-search-cli/planning/specs/
   └── PLAN-001-command-spec.md

   projects/file-search-cli/planning/test-cases/
   └── PLAN-001-tests.md
   \`\`\`

### 4. Coding

\`\`\`bash
bash scripts/run-agent.sh coding --ticket PLAN-001
\`\`\`

**Coding Agent actions**:
1. \`.project-config.json\` → Check current project
2. \`.project-meta.json\` → Check type, stack
3. Load \`.agents/coding/templates/cli-tool.md\` template
4. Load \`.rules/_verified/cli-tool/cobra-go.md\` or \`_cache\`
5. Generate code:
   \`\`\`
   projects/file-search-cli/src/
   ├── cmd/
   │   ├── root.go
   │   └── search.go        # 🆕 Created
   └── internal/
       └── search/          # 🆕 Created
           └── finder.go
   \`\`\`
6. Generate log:
   \`\`\`
   projects/file-search-cli/logs/coding/
   └── 20260312-143000-PLAN-001-search.md
   \`\`\`

### 5. QA

\`\`\`bash
bash scripts/run-agent.sh qa --ticket PLAN-001
\`\`\`

**Output**:
\`\`\`
projects/file-search-cli/src/
└── internal/
    └── search/
        └── finder_test.go   # 🆕 Created

projects/file-search-cli/logs/qa/
└── 20260312-150000-PLAN-001-search.md
\`\`\`

---

## 📋 Directory Structure Templates by Project Type

### Web Fullstack

\`\`\`
projects/{name}/
├── .project-meta.json
├── planning/
│   ├── tickets/
│   ├── specs/
│   │   ├── backend/
│   │   └── frontend/
│   └── test-cases/
│       ├── backend/
│       └── frontend/
├── src/
│   ├── backend/
│   │   ├── src/
│   │   ├── tests/
│   │   └── requirements.txt (or package.json)
│   └── frontend/
│       ├── src/
│       ├── public/
│       └── package.json
├── logs/
└── README.md
\`\`\`

### Web MVC

\`\`\`
projects/{name}/
├── .project-meta.json
├── planning/
│   ├── tickets/
│   ├── specs/
│   │   ├── endpoints/
│   │   └── templates/
│   └── test-cases/
├── src/
│   ├── manage.py (Django) or build.gradle (Spring)
│   ├── apps/ or controllers/
│   ├── templates/ or views/
│   ├── static/
│   └── tests/
├── logs/
└── README.md
\`\`\`

### CLI Tool

\`\`\`
projects/{name}/
├── .project-meta.json
├── planning/
│   ├── tickets/
│   ├── specs/
│   └── test-cases/
├── src/
│   ├── cmd/ (Go) or cli/ (Python)
│   ├── internal/ (Go) or lib/ (Python)
│   ├── go.mod (Go) or setup.py (Python)
│   └── main.go or __main__.py
├── logs/
└── README.md
\`\`\`

### Desktop App

\`\`\`
projects/{name}/
├── .project-meta.json
├── planning/
│   ├── tickets/
│   ├── specs/
│   │   ├── screens/
│   │   ├── state/
│   │   └── ipc/
│   └── test-cases/
│       ├── unit/
│       ├── integration/
│       └── e2e/
├── src/
│   ├── src-tauri/ (Tauri) or main/ (Electron)
│   ├── src/ (Frontend)
│   └── public/
├── logs/
└── README.md
\`\`\`

### Library

\`\`\`
projects/{name}/
├── .project-meta.json
├── planning/
│   ├── tickets/
│   ├── specs/
│   │   ├── api/
│   │   └── examples/
│   └── test-cases/
├── src/
│   ├── src/ or lib/
│   ├── tests/
│   ├── package.json (npm) or setup.py (pip)
│   └── README.md
├── logs/
└── README.md
\`\`\`

### Data Pipeline

\`\`\`
projects/{name}/
├── .project-meta.json
├── planning/
│   ├── tickets/
│   ├── specs/
│   │   ├── dags/
│   │   ├── transforms/
│   │   └── schedules/
│   └── test-cases/
├── src/
│   ├── dags/
│   ├── plugins/
│   ├── tests/
│   └── requirements.txt
├── logs/
└── README.md
\`\`\`

---

## 🔄 Multi-Project Management

### Switch Projects

\`\`\`bash
# List projects
ls projects/

# Switch to specific project
bash scripts/switch-project.sh file-search-cli
\`\`\`

**switch-project.sh performs**:
1. Update \`.project-config.json\` (change \`current_project\`)
2. Read that project's \`.project-meta.json\`
3. Configure environment (if needed)

### Independent Work Per Project

\`\`\`bash
# Work on Project A
cd projects/my-todo-app
bash ../../scripts/run-agent.sh coding --ticket PLAN-001

# Work on Project B (separate terminal)
cd projects/file-search-cli
bash ../../scripts/run-agent.sh coding --ticket PLAN-001
\`\`\`

---

## 🛠️ Agent Template Structure

### PM Agent Template Example

**\`.agents/pm/templates/cli-tool.md\`**:

\`\`\`markdown
# PM Agent - CLI Tool Template

## Deliverable Structure

### 1. Command Specification
- Location: \`projects/{project_name}/planning/specs/PLAN-XXX-command-spec.md\`
- Contents:
  - Command name
  - Subcommands (if any)
  - Flags/options
  - Input parameters
  - Output format
  - Examples

### 2. Test Cases
- Location: \`projects/{project_name}/planning/test-cases/PLAN-XXX-tests.md\`
- Contents:
  - Normal cases
  - Exception cases
  - Edge cases
  - Integration test scenarios

## Template

(Omitted - actual template content)
\`\`\`

### Coding Agent Template Example

**\`.agents/coding/templates/cli-tool.md\`**:

\`\`\`markdown
# Coding Agent - CLI Tool Template

## Work Order

1. Read \`.project-config.json\`
2. Read \`projects/{current_project}/.project-meta.json\`
3. Read \`projects/{current_project}/planning/specs/PLAN-XXX-command-spec.md\`
4. Load coding rules (\`.rules/_verified/\` or \`_cache\`)
5. Generate code:
   - Go Cobra: \`cmd/\`, \`internal/\`
   - Python Click: \`cli/\`, \`lib/\`
   - Rust clap: \`src/cli.rs\`, \`src/lib.rs\`
6. Write log: \`projects/{current_project}/logs/coding/\`

## Framework-Specific Structure

(Omitted - actual template content)
\`\`\`

---

---

## ✅ Change Summary

### Removed
- ❌ Fixed directory structure (be-/fe- etc.)
- ❌ Tech Stack-dependent structure

### Added
- ✅ \`projects/{name}/\` (per-project isolation)
- ✅ \`.project-meta.json\` (project metadata)
- ✅ \`planning/\` (per-project planning documents)
- ✅ Type-specific dynamic \`specs/\` structure
- ✅ \`coding\`, \`qa\` unified agents
- ✅ Project switching feature (\`switch-project.sh\`)

### Maintained
- ✅ \`.agents/\` structure (with added templates)
- ✅ \`.rules/\` structure (_verified, _cache)
- ✅ \`scripts/\` (with some added scripts)
- ✅ Git branch workflow

---

**Version**: v0.0.2
**Last Review**: 2026-03-12
