#!/bin/bash
# Project switch script
#
# Usage:
#   bash scripts/switch-project.sh my-cli-tool
#   bash scripts/switch-project.sh --list

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$WORKSPACE_ROOT/.project-config.json"
PROJECTS_DIR="$WORKSPACE_ROOT/projects"

# ── Show project list ─────────────────────────────────────────
show_projects() {
    echo ""
    echo "╔══════════════════════════════════════════════╗"
    echo "║  Project List                                ║"
    echo "╚══════════════════════════════════════════════╝"
    echo ""

    if [[ ! -d "$PROJECTS_DIR" ]] || [[ -z "$(ls -A "$PROJECTS_DIR" 2>/dev/null)" ]]; then
        echo "No projects found."
        echo ""
        echo "Create a new project:"
        echo "  bash scripts/init-project.sh --interactive"
        exit 0
    fi

    # Check current active project
    CURRENT_PROJECT=""
    if [[ -f "$CONFIG_FILE" ]]; then
        CURRENT_PROJECT=$(grep -o '"current_project": *"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4 2>/dev/null || echo "")
    fi

    for project_dir in "$PROJECTS_DIR"/*; do
        if [[ -d "$project_dir" ]]; then
            project_name=$(basename "$project_dir")
            meta_file="$project_dir/.project-meta.json"

            # Mark current project
            if [[ "$project_name" == "$CURRENT_PROJECT" ]]; then
                echo "  → $project_name (current)"
            else
                echo "    $project_name"
            fi

            # Show metadata
            if [[ -f "$meta_file" ]]; then
                project_type=$(grep -o '"project_type": *"[^"]*"' "$meta_file" | cut -d'"' -f4 2>/dev/null || echo "unknown")
                echo "      Type: $project_type"
            fi
            echo ""
        fi
    done
}

# ── Argument check ────────────────────────────────────────────
if [[ $# -eq 0 ]] || [[ "$1" == "--list" ]] || [[ "$1" == "-l" ]]; then
    show_projects
    exit 0
fi

PROJECT_NAME="$1"
PROJECT_PATH="$PROJECTS_DIR/$PROJECT_NAME"

# ── Check project existence ──────────────────────────────────
if [[ ! -d "$PROJECT_PATH" ]]; then
    echo "❌ Project not found: $PROJECT_NAME"
    echo ""
    echo "Available projects:"
    show_projects
    exit 1
fi

# ── Read project metadata ─────────────────────────────────────
META_FILE="$PROJECT_PATH/.project-meta.json"
if [[ ! -f "$META_FILE" ]]; then
    echo "❌ Project metadata not found: $META_FILE"
    exit 1
fi

PROJECT_TYPE=$(grep -o '"project_type": *"[^"]*"' "$META_FILE" | cut -d'"' -f4 2>/dev/null || echo "unknown")
CREATED_AT=$(grep -o '"created_at": *"[^"]*"' "$META_FILE" | cut -d'"' -f4 2>/dev/null || echo "unknown")

# ── Update .project-config.json ───────────────────────────────
echo ""
echo "Switching project: $PROJECT_NAME"
echo "  Type: $PROJECT_TYPE"
echo "  Created at: $CREATED_AT"
echo ""

# Read existing recent_projects array (simple JSON parsing without jq)
RECENT_PROJECTS=()
if [[ -f "$CONFIG_FILE" ]]; then
    # Extract existing project names (simple grep)
    while IFS= read -r line; do
        RECENT_PROJECTS+=("$line")
    done < <(grep -o '"[^"]*"' "$CONFIG_FILE" | grep -v "current_project\|current_project_path\|recent_projects" | tr -d '"' | head -5)
fi

# Add current project to the front (remove duplicates)
NEW_RECENT=("$PROJECT_NAME")
for proj in "${RECENT_PROJECTS[@]}"; do
    if [[ "$proj" != "$PROJECT_NAME" ]] && [[ ${#NEW_RECENT[@]} -lt 5 ]]; then
        NEW_RECENT+=("$proj")
    fi
done

# Build JSON for recent_projects array
RECENT_JSON=""
for i in "${!NEW_RECENT[@]}"; do
    if [[ $i -eq 0 ]]; then
        RECENT_JSON="\"${NEW_RECENT[$i]}\""
    else
        RECENT_JSON="$RECENT_JSON, \"${NEW_RECENT[$i]}\""
    fi
done

cat > "$CONFIG_FILE" <<EOF
{
  "current_project": "$PROJECT_NAME",
  "current_project_path": "projects/$PROJECT_NAME",
  "recent_projects": [$RECENT_JSON]
}
EOF

echo "✅ Project switch complete"
echo ""
echo "Next steps:"
echo "  1. Create ticket: bash scripts/run-agent.sh project-planner --project \"Project description\""
echo "  2. Create spec: bash scripts/run-agent.sh pm --ticket-file projects/$PROJECT_NAME/planning/tickets/PLAN-001-*.md"
echo "  3. Coding: bash scripts/run-agent.sh coding --ticket PLAN-001"
echo "  4. Testing: bash scripts/run-agent.sh qa --ticket PLAN-001"
echo ""
