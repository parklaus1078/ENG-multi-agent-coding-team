#!/bin/bash
# Project initialization script
#
# Usage:
#   bash scripts/init-project.sh --interactive
#   bash scripts/init-project.sh --type cli-tool --language go --framework cobra --name my-cli

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
PROJECTS_DIR="$WORKSPACE_ROOT/projects"
CONFIG_FILE="$WORKSPACE_ROOT/.project-config.json"

# ── Defaults ────────────────────────────────────────────────
PROJECT_TYPE=""
LANGUAGE=""
FRAMEWORK=""
VERSION="latest"
PROJECT_NAME=""
PROJECT_DESC=""
INTERACTIVE=false

# ── Parse flags ─────────────────────────────────────────────
if [[ $# -eq 0 ]]; then
    INTERACTIVE=true
fi

while [[ $# -gt 0 ]]; do
    case "$1" in
        --interactive)
            INTERACTIVE=true
            shift
            ;;
        --type)
            PROJECT_TYPE="$2"
            shift 2
            ;;
        --language)
            LANGUAGE="$2"
            shift 2
            ;;
        --framework)
            FRAMEWORK="$2"
            shift 2
            ;;
        --version)
            VERSION="$2"
            shift 2
            ;;
        --name)
            PROJECT_NAME="$2"
            shift 2
            ;;
        --description)
            PROJECT_DESC="$2"
            shift 2
            ;;
        *)
            echo "❌ Unknown option: '$1'"
            echo ""
            echo "Usage:"
            echo "  bash scripts/init-project.sh --interactive"
            echo "  bash scripts/init-project.sh --type cli-tool --language go --framework cobra --name my-cli"
            echo ""
            echo "Options:"
            echo "  --interactive       Interactive mode"
            echo "  --type             Project type (web-fullstack, web-mvc, cli-tool, desktop-app, mobile-app, library, data-pipeline)"
            echo "  --language         Language (python, javascript, typescript, go, rust, java, etc.)"
            echo "  --framework        Framework (fastapi, django, nextjs, cobra, etc.)"
            echo "  --version          Framework version (default: latest)"
            echo "  --name             Project name"
            echo "  --description      Project description"
            exit 1
            ;;
    esac
done

# ── Interactive mode ────────────────────────────────────────
if [[ "$INTERACTIVE" == true ]]; then
    echo "╔══════════════════════════════════════════════╗"
    echo "║  Multi-Agent Project Initialization          ║"
    echo "╚══════════════════════════════════════════════╝"
    echo ""

    # Select project type
    echo "1. Select project type:"
    echo "   1) web-fullstack     (FE + BE separated)"
    echo "   2) web-mvc           (Django, Rails, Spring Boot MVC, etc.)"
    echo "   3) cli-tool          (CLI tools)"
    echo "   4) desktop-app       (Electron, Tauri, Qt, etc.)"
    echo "   5) mobile-app        (React Native, Flutter, etc.)"
    echo "   6) library           (npm, pip packages, etc.)"
    echo "   7) data-pipeline     (Airflow, Prefect, etc.)"
    echo ""
    read -p "Select (1-7): " TYPE_CHOICE

    case $TYPE_CHOICE in
        1) PROJECT_TYPE="web-fullstack" ;;
        2) PROJECT_TYPE="web-mvc" ;;
        3) PROJECT_TYPE="cli-tool" ;;
        4) PROJECT_TYPE="desktop-app" ;;
        5) PROJECT_TYPE="mobile-app" ;;
        6) PROJECT_TYPE="library" ;;
        7) PROJECT_TYPE="data-pipeline" ;;
        *) echo "❌ Invalid selection"; exit 1 ;;
    esac

    echo ""
    read -p "2. Project name: " PROJECT_NAME
    read -p "3. Enter language (e.g., python, go, javascript): " LANGUAGE
    read -p "4. Enter framework (e.g., fastapi, cobra, nextjs): " FRAMEWORK
    read -p "5. Framework version (default: latest): " INPUT_VERSION
    if [[ -n "$INPUT_VERSION" ]]; then
        VERSION="$INPUT_VERSION"
    fi
    read -p "6. Project description (optional): " PROJECT_DESC
fi

# ── Validate required values ────────────────────────────────
if [[ -z "$PROJECT_TYPE" ]] || [[ -z "$LANGUAGE" ]] || [[ -z "$FRAMEWORK" ]] || [[ -z "$PROJECT_NAME" ]]; then
    echo "❌ Required values missing."
    echo "   --type, --language, --framework, --name are required."
    exit 1
fi

# Validate project name (allow only alphanumeric and hyphens)
if [[ ! "$PROJECT_NAME" =~ ^[a-zA-Z0-9-]+$ ]]; then
    echo "❌ Project name can only contain alphanumeric characters and hyphens (-)."
    exit 1
fi

PROJECT_PATH="$PROJECTS_DIR/$PROJECT_NAME"

# ── Check for existing project ──────────────────────────────
if [[ -d "$PROJECT_PATH" ]]; then
    echo ""
    echo "⚠️  Project already exists: $PROJECT_NAME"
    read -p "Overwrite? (yes/no): " OVERWRITE

    if [[ "$OVERWRITE" != "yes" ]]; then
        echo "❌ Initialization cancelled"
        exit 0
    fi

    rm -rf "$PROJECT_PATH"
fi

# ── Create project directory ────────────────────────────────
echo ""
echo "📝 Creating project directory: $PROJECT_PATH"
mkdir -p "$PROJECT_PATH"

# ── Generate project metadata ───────────────────────────────
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "📝 Creating project metadata: .project-meta.json"

# For web-fullstack, get additional frontend/backend input
if [[ "$PROJECT_TYPE" == "web-fullstack" ]]; then
    if [[ "$INTERACTIVE" == true ]]; then
        echo ""
        echo "Frontend configuration:"
        read -p "  Language (javascript/typescript): " FE_LANGUAGE
        read -p "  Framework (nextjs, vite-react, nuxt, etc.): " FE_FRAMEWORK
        echo ""
        echo "Backend configuration:"
        echo "  Language: $LANGUAGE"
        echo "  Framework: $FRAMEWORK"
        read -p "  Database (postgresql, mysql, mongodb, etc.): " DATABASE
    fi

    cat > "$PROJECT_PATH/.project-meta.json" <<EOF
{
  "project_name": "$PROJECT_NAME",
  "project_type": "$PROJECT_TYPE",
  "stack": {
    "type": "$PROJECT_TYPE",
    "backend": {
      "language": "$LANGUAGE",
      "framework": "$FRAMEWORK",
      "version": "$VERSION",
      "database": "${DATABASE:-postgresql}"
    },
    "frontend": {
      "language": "${FE_LANGUAGE:-typescript}",
      "framework": "${FE_FRAMEWORK:-nextjs}",
      "version": "latest"
    }
  },
  "project_description": "$PROJECT_DESC",
  "created_at": "$TIMESTAMP",
  "directory_structure": "$PROJECT_TYPE",
  "active": true
}
EOF
else
    # Other project types
    cat > "$PROJECT_PATH/.project-meta.json" <<EOF
{
  "project_name": "$PROJECT_NAME",
  "project_type": "$PROJECT_TYPE",
  "stack": {
    "type": "$PROJECT_TYPE",
    "language": "$LANGUAGE",
    "framework": "$FRAMEWORK",
    "version": "$VERSION"
  },
  "project_description": "$PROJECT_DESC",
  "created_at": "$TIMESTAMP",
  "directory_structure": "$PROJECT_TYPE",
  "active": true
}
EOF
fi

# ── Create planning/ directory (type-specific structure) ────
echo "📁 Creating planning/ directory..."

mkdir -p "$PROJECT_PATH/planning/tickets"

case "$PROJECT_TYPE" in
    web-fullstack)
        mkdir -p "$PROJECT_PATH/planning/specs/backend"
        mkdir -p "$PROJECT_PATH/planning/specs/frontend"
        mkdir -p "$PROJECT_PATH/planning/test-cases/backend"
        mkdir -p "$PROJECT_PATH/planning/test-cases/frontend"
        ;;
    web-mvc)
        mkdir -p "$PROJECT_PATH/planning/specs/endpoints"
        mkdir -p "$PROJECT_PATH/planning/specs/templates"
        mkdir -p "$PROJECT_PATH/planning/test-cases"
        ;;
    cli-tool)
        mkdir -p "$PROJECT_PATH/planning/specs"
        mkdir -p "$PROJECT_PATH/planning/test-cases"
        ;;
    desktop-app)
        mkdir -p "$PROJECT_PATH/planning/specs/screens"
        mkdir -p "$PROJECT_PATH/planning/specs/state"
        mkdir -p "$PROJECT_PATH/planning/specs/ipc"
        mkdir -p "$PROJECT_PATH/planning/test-cases/unit"
        mkdir -p "$PROJECT_PATH/planning/test-cases/integration"
        mkdir -p "$PROJECT_PATH/planning/test-cases/e2e"
        ;;
    mobile-app)
        mkdir -p "$PROJECT_PATH/planning/specs/screens"
        mkdir -p "$PROJECT_PATH/planning/specs/navigation"
        mkdir -p "$PROJECT_PATH/planning/specs/state"
        mkdir -p "$PROJECT_PATH/planning/test-cases"
        ;;
    library)
        mkdir -p "$PROJECT_PATH/planning/specs/api"
        mkdir -p "$PROJECT_PATH/planning/specs/examples"
        mkdir -p "$PROJECT_PATH/planning/test-cases"
        ;;
    data-pipeline)
        mkdir -p "$PROJECT_PATH/planning/specs/dags"
        mkdir -p "$PROJECT_PATH/planning/specs/transforms"
        mkdir -p "$PROJECT_PATH/planning/specs/schedules"
        mkdir -p "$PROJECT_PATH/planning/test-cases"
        ;;
esac

# ── Create src/ directory (framework-specific initial structure) ──
echo "📁 Creating src/ directory..."
mkdir -p "$PROJECT_PATH/src"

# Framework-specific initial files created by Stack Initializer Agent
# Only create base directory here

# ── Create logs/ directory ──────────────────────────────────
echo "📁 Creating logs/ directory..."
mkdir -p "$PROJECT_PATH/logs/stack-initializer"
mkdir -p "$PROJECT_PATH/logs/project-planner"
mkdir -p "$PROJECT_PATH/logs/pm"
mkdir -p "$PROJECT_PATH/logs/coding"
mkdir -p "$PROJECT_PATH/logs/qa"

# ── Generate README.md ──────────────────────────────────────
echo "📝 Creating README.md..."
cat > "$PROJECT_PATH/README.md" <<EOF
# $PROJECT_NAME

$PROJECT_DESC

---

## Project Information

- **Type**: $PROJECT_TYPE
- **Language**: $LANGUAGE
- **Framework**: $FRAMEWORK
- **Created**: $TIMESTAMP

---

## Directory Structure

\`\`\`
$PROJECT_NAME/
├── .project-meta.json          # Project metadata
├── planning/                   # Planning documents
│   ├── tickets/                # Ticket files
│   ├── specs/                  # Specifications
│   └── test-cases/             # Test cases
├── src/                        # Actual code
├── logs/                       # Agent logs
└── README.md                   # This file
\`\`\`

---

## Workflow

### 1. Create Tickets

\`\`\`bash
cd team
bash scripts/run-agent.sh project-planner --project "Project description"
\`\`\`

### 2. Generate Specifications

\`\`\`bash
bash scripts/run-agent.sh pm --ticket-file projects/$PROJECT_NAME/planning/tickets/PLAN-001-*.md
\`\`\`

### 3. Coding

\`\`\`bash
bash scripts/run-agent.sh coding --ticket PLAN-001
\`\`\`

### 4. Testing

\`\`\`bash
bash scripts/run-agent.sh qa --ticket PLAN-001
\`\`\`

---

## View Logs

\`\`\`bash
bash scripts/show-logs.sh
\`\`\`

---

**Created**: $TIMESTAMP
EOF

# ── Update .project-config.json (set as current project) ───
echo "📝 Updating .project-config.json..."

cat > "$CONFIG_FILE" <<EOF
{
  "current_project": "$PROJECT_NAME",
  "current_project_path": "projects/$PROJECT_NAME",
  "recent_projects": ["$PROJECT_NAME"]
}
EOF

# ── Completion message ──────────────────────────────────────
echo ""
echo "✅ Project initialization complete!"
echo ""
echo "📁 Project path: $PROJECT_PATH"
echo "📊 Project type: $PROJECT_TYPE"
echo "💻 Language/Framework: $LANGUAGE / $FRAMEWORK"
echo ""
echo "📋 Created directories:"
echo "  - planning/tickets/       Ticket files"
echo "  - planning/specs/         Specifications"
echo "  - planning/test-cases/    Test cases"
echo "  - src/                    Source code (Stack Initializer creates structure)"
echo "  - logs/                   Agent logs"
echo ""
echo "🚀 Next steps:"
echo ""
echo "1. Run Stack Initializer (generate coding rules + initialize project structure):"
echo "   bash scripts/run-agent.sh stack-initializer"
echo ""
echo "2. Create tickets:"
echo "   bash scripts/run-agent.sh project-planner --project \"Project description\""
echo ""
echo "3. Generate specifications:"
echo "   bash scripts/run-agent.sh pm --ticket-file projects/$PROJECT_NAME/planning/tickets/PLAN-001-*.md"
echo ""
echo "4. Coding:"
echo "   bash scripts/run-agent.sh coding --ticket PLAN-001"
echo ""
echo "5. Testing:"
echo "   bash scripts/run-agent.sh qa --ticket PLAN-001"
echo ""
