#!/bin/bash
# Agent implementation log viewer script v2.0
# Usage:
#   bash scripts/show-logs.sh              # All logs for current project
#   bash scripts/show-logs.sh coding       # Specific agent only
#   bash scripts/show-logs.sh --all        # All projects

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$WORKSPACE_ROOT/.project-config.json"
FILTER="${1:-}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Agent Implementation Logs (v2.0)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── All projects mode ───────────────────────────────────────
if [[ "$FILTER" == "--all" ]]; then
    PROJECTS_DIR="$WORKSPACE_ROOT/projects"

    if [[ ! -d "$PROJECTS_DIR" ]] || [[ -z "$(ls -A "$PROJECTS_DIR" 2>/dev/null)" ]]; then
        echo ""
        echo "No projects found."
        echo ""
        exit 0
    fi

    for project_dir in "$PROJECTS_DIR"/*; do
        if [[ -d "$project_dir" ]]; then
            project_name=$(basename "$project_dir")
            echo ""
            echo "📦 Project: $project_name"
            echo "   Path: $project_dir"

            LOGS_DIR="$project_dir/logs"
            if [[ ! -d "$LOGS_DIR" ]]; then
                echo "   (No logs directory)"
                continue
            fi

            AGENTS=("stack-initializer" "project-planner" "pm" "coding" "qa")
            for agent in "${AGENTS[@]}"; do
                LOG_DIR="$LOGS_DIR/$agent"
                COUNT=$(find "$LOG_DIR" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')

                if [[ "$COUNT" -gt 0 ]]; then
                    echo ""
                    echo "   📁 [$agent] — $COUNT logs"
                    find "$LOG_DIR" -name "*.md" | sort -r | head -3 | while read -r f; do
                        BASENAME=$(basename "$f")
                        echo "      - $BASENAME"
                    done
                    if [[ "$COUNT" -gt 3 ]]; then
                        echo "      ... (and $((COUNT - 3)) more)"
                    fi
                fi
            done
        fi
    done

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 0
fi

# ── Current project mode ────────────────────────────────────

# Check current project
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo ""
    echo "❌ .project-config.json not found."
    echo "   Initialize project first:"
    echo "   bash scripts/init-project-v2.sh --interactive"
    echo ""
    exit 1
fi

CURRENT_PROJECT=$(grep -o '"current_project": *"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4 2>/dev/null)

if [[ -z "$CURRENT_PROJECT" ]]; then
    echo ""
    echo "❌ No active project."
    echo ""
    exit 1
fi

PROJECT_PATH="$WORKSPACE_ROOT/projects/$CURRENT_PROJECT"
LOGS_DIR="$PROJECT_PATH/logs"

echo ""
echo "📦 Current project: $CURRENT_PROJECT"
echo "   Path: $PROJECT_PATH"

if [[ ! -d "$LOGS_DIR" ]]; then
    echo ""
    echo "   (No logs directory)"
    echo ""
    exit 0
fi

# v2.0 agent list
AGENTS=("stack-initializer" "project-planner" "pm" "coding" "qa")

for agent in "${AGENTS[@]}"; do
    # Filtering
    if [[ -n "$FILTER" && "$agent" != "$FILTER" ]]; then
        continue
    fi

    LOG_DIR="$LOGS_DIR/$agent"
    COUNT=$(find "$LOG_DIR" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')

    echo ""
    echo "📁 [$agent] — $COUNT logs"

    if [[ "$COUNT" -gt 0 ]]; then
        find "$LOG_DIR" -name "*.md" | sort -r | while read -r f; do
            BASENAME=$(basename "$f")
            # Display file size
            SIZE=$(du -h "$f" | cut -f1)
            echo "   - $BASENAME ($SIZE)"
        done
    else
        echo "   (No logs)"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Rate Limit Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 "$SCRIPT_DIR/parse_usage.py" "status" 2>/dev/null || echo "  (No usage history)"
echo ""
echo "💡 Tips:"
echo "   All project logs: bash scripts/show-logs.sh --all"
echo "   Specific agent:   bash scripts/show-logs.sh coding"
echo "   Switch project:   bash scripts/switch-project.sh <project-name>"
echo ""
