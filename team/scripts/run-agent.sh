#!/bin/bash
# Agent execution wrapper script
#
# Usage:
#   bash scripts/run-agent.sh project-planner --project "Todo management app"
#   bash scripts/run-agent.sh pm              --ticket-file ./tickets/PLAN-001-user-auth.md

set -e

AGENT_NAME="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
PROJECT_CONFIG="$WORKSPACE_ROOT/.project-config.json"

# ── Check current project ───────────────────────────────────
if [[ ! -f "$PROJECT_CONFIG" ]]; then
    echo "❌ Project configuration file not found: .project-config.json"
    echo "   Initialize project first:"
    echo "   bash scripts/init-project.sh --interactive"
    exit 1
fi

CURRENT_PROJECT=$(grep -o '"current_project": *"[^"]*"' "$PROJECT_CONFIG" | cut -d'"' -f4 2>/dev/null)
if [[ -z "$CURRENT_PROJECT" ]]; then
    echo "❌ No active project."
    echo "   Initialize or switch project:"
    echo "   bash scripts/init-project.sh --interactive"
    echo "   bash scripts/switch-project.sh <project-name>"
    exit 1
fi

PROJECT_PATH="$WORKSPACE_ROOT/projects/$CURRENT_PROJECT"
if [[ ! -d "$PROJECT_PATH" ]]; then
    echo "❌ Project directory not found: $PROJECT_PATH"
    exit 1
fi

echo ""
echo "📍 Current project: $CURRENT_PROJECT"
echo "📂 Path: $PROJECT_PATH"
echo ""

# ── Validation check ────────────────────────────────────────
VALID_AGENTS=("stack-initializer" "project-planner" "pm" "coding" "qa")

if [[ -z "$AGENT_NAME" ]]; then
    echo ""
    echo "Usage: bash scripts/run-agent.sh <agent_name> [options]"
    echo ""
    echo "Agent list:"
    echo "  stack-initializer --config <path>           Stack initialization"
    echo "  project-planner   --project <description>   Project breakdown → create tickets/"
    echo "  pm                --ticket-file <path>      Ticket → generate specifications"
    echo "  coding            --ticket <ticket-number>  Code implementation (all types)"
    echo "  qa                --ticket <ticket-number>  Write tests (all types)"
    echo ""
    exit 1
fi

VALID=false
for a in "${VALID_AGENTS[@]}"; do
    [[ "$AGENT_NAME" == "$a" ]] && VALID=true && break
done

if [[ "$VALID" == false ]]; then
    echo "❌ Unknown agent: '$AGENT_NAME'"
    echo "   Available: ${VALID_AGENTS[*]}"
    exit 1
fi

# ── Parse flags ─────────────────────────────────────────────
shift  # Remove agent_name, parse remaining flags
TICKET_FILE=""
TICKET_NUM=""
PROJECT_DESC=""
CONFIG_FILE=""
RESUME_MODE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --ticket-file)
            TICKET_FILE="$2"
            shift 2
            ;;
        --ticket)
            TICKET_NUM="$2"
            shift 2
            ;;
        --project)
            PROJECT_DESC="$2"
            shift 2
            ;;
        --config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        --resume)
            RESUME_MODE=true
            shift
            ;;
        *)
            echo "❌ Unknown option: '$1'"
            exit 1
            ;;
    esac
done

# ── Validate agent-specific required options and set initial prompt ──
case "$AGENT_NAME" in
    stack-initializer)
        if [[ -z "$CONFIG_FILE" ]]; then
            # Use .project-config.json if it exists
            if [[ -f "$WORKSPACE_ROOT/.project-config.json" ]]; then
                CONFIG_FILE="$WORKSPACE_ROOT/.project-config.json"
            else
                echo "❌ stack-initializer requires --config option."
                echo "   Or .project-config.json file must exist."
                echo "   Example: bash scripts/init-project.sh"
                exit 1
            fi
        fi
        if [[ ! -f "$CONFIG_FILE" ]]; then
            echo "❌ Configuration file not found: $CONFIG_FILE"
            exit 1
        fi
        INITIAL_PROMPT="Read project configuration file and initialize stack: $CONFIG_FILE"
        ;;
    project-planner)
        if [[ "$RESUME_MODE" == true ]]; then
            # Resume mode: check if plan file exists
            LATEST_PLAN=$(ls -t "$PROJECT_PATH/planning/tickets/.plan-"*.json 2>/dev/null | head -1)
            if [[ -z "$LATEST_PLAN" ]]; then
                echo "❌ Plan file to resume not found."
                echo "   $PROJECT_PATH/planning/tickets/.plan-*.json file required."
                exit 1
            fi
            INITIAL_PROMPT="Resume: Generate ticket files from Phase 2. Plan file: $LATEST_PLAN"
        else
            if [[ -z "$PROJECT_DESC" ]]; then
                echo "❌ project-planner requires --project option."
                echo "   Example: bash scripts/run-agent.sh project-planner --project \"Todo management app\""
                echo "   Resume: bash scripts/run-agent.sh project-planner --resume"
                exit 1
            fi
            INITIAL_PROMPT="$PROJECT_DESC"
        fi
        ;;
    pm)
        if [[ -z "$TICKET_FILE" ]]; then
            echo "❌ pm requires --ticket-file option."
            echo "   Example: bash scripts/run-agent.sh pm --ticket-file $PROJECT_PATH/planning/tickets/PLAN-001-user-auth.md"
            exit 1
        fi
        # Convert relative path to absolute path
        if [[ ! "$TICKET_FILE" =~ ^/ ]]; then
            TICKET_FILE="$WORKSPACE_ROOT/$TICKET_FILE"
        fi
        if [[ ! -f "$TICKET_FILE" ]]; then
            echo "❌ Ticket file not found: $TICKET_FILE"
            exit 1
        fi

        # Auto-create Git branch (extract ticket number and slug from ticket file)
        FILENAME=$(basename "$TICKET_FILE")
        # Extract PLAN-001 from PLAN-001-user-auth.md
        TICKET_NUM=$(echo "$FILENAME" | grep -o '^PLAN-[0-9]*')
        # Extract user-auth
        SLUG=$(echo "$FILENAME" | sed "s/${TICKET_NUM}-//" | sed 's/\.md$//')

        if [[ -n "$TICKET_NUM" ]] && [[ -n "$SLUG" ]]; then
            echo "🌿 Auto-creating Git branch..."
            if bash "$SCRIPT_DIR/git-branch-helper.sh" prepare "pm" "$TICKET_NUM" "$SLUG" 2>/dev/null; then
                echo "✅ Branch ready"
            else
                echo "⚠️  Branch creation failed (check Git settings, work continues)"
            fi
            echo ""
        fi

        INITIAL_PROMPT="$(cat "$TICKET_FILE")"
        ;;
    coding|qa)
        if [[ -z "$TICKET_NUM" ]]; then
            echo "❌ $AGENT_NAME requires --ticket option."
            echo "   Example: bash scripts/run-agent.sh $AGENT_NAME --ticket PLAN-001"
            exit 1
        fi

        # Auto-create Git branch (extract slug from ticket file)
        TICKET_FILE_PATTERN="$PROJECT_PATH/planning/tickets/${TICKET_NUM}-*.md"
        TICKET_FILE_FOUND=$(ls $TICKET_FILE_PATTERN 2>/dev/null | head -1)

        if [[ -n "$TICKET_FILE_FOUND" ]]; then
            # Extract slug from filename (PLAN-001-user-auth.md → user-auth)
            FILENAME=$(basename "$TICKET_FILE_FOUND")
            SLUG=$(echo "$FILENAME" | sed "s/${TICKET_NUM}-//" | sed 's/\.md$//')

            echo "🌿 Auto-creating Git branch..."
            if bash "$SCRIPT_DIR/git-branch-helper.sh" prepare "$AGENT_NAME" "$TICKET_NUM" "$SLUG" 2>/dev/null; then
                echo "✅ Branch ready"
            else
                echo "⚠️  Branch creation failed (check Git settings, work continues)"
            fi
            echo ""
        fi

        INITIAL_PROMPT="Working on ticket $TICKET_NUM."
        ;;
esac

# ── Check CLAUDE.md existence ───────────────────────────────
AGENT_DIR="$WORKSPACE_ROOT/.agents/$AGENT_NAME"
CLAUDE_MD="$AGENT_DIR/CLAUDE.md"

if [[ ! -f "$CLAUDE_MD" ]]; then
    echo "❌ CLAUDE.md not found: $CLAUDE_MD"
    exit 1
fi

# ── Check claude CLI ────────────────────────────────────────
if ! command -v claude &>/dev/null; then
    echo "❌ claude CLI not found."
    echo "   Verify Claude Code is installed."
    echo "   Installation: https://docs.claude.ai/claude-code"
    exit 1
fi

# ── Pre-log rate limit ──────────────────────────────────────
python3 "$SCRIPT_DIR/parse_usage.py" "$AGENT_NAME" --log 2>/dev/null || true

# ── Start agent ─────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║  Agent starting: $AGENT_NAME"
echo "║  Workspace: $WORKSPACE_ROOT"
echo "║  Instruction file: .agents/$AGENT_NAME/CLAUDE.md"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "💡 Agent will automatically perform rate limit check."
echo "   Exit: Ctrl+C"
echo ""

# ── Execute claude ──────────────────────────────────────────
# --append-system-prompt: Keep Claude Code defaults while adding CLAUDE.md
# (Using --system-prompt removes Claude Code built-in tool descriptions, so prohibited)

# Start in interactive mode (removed --print)
echo "📝 Sending initial prompt..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$INITIAL_PROMPT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

exec claude \
    --model claude-sonnet-4-5 \
    --append-system-prompt "$(cat "$CLAUDE_MD")" \
    --allowedTools "Bash" "Read" "Edit" "Write" \
    <<EOF
$INITIAL_PROMPT
EOF
