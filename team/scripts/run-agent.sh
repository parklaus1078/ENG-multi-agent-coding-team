#!/bin/bash
# Agent execution wrapper script
#
# Usage:
#   bash scripts/run-agent.sh project-planner --project "Todo management app"
#   bash scripts/run-agent.sh pm              --ticket-file ./tickets/PLAN-001-user-auth.md
#   bash scripts/run-agent.sh be-coding       --ticket PLAN-001
#   bash scripts/run-agent.sh fe-coding       --ticket PLAN-001
#   bash scripts/run-agent.sh qa-be           --ticket PLAN-001
#   bash scripts/run-agent.sh qa-fe           --ticket PLAN-001

set -e

AGENT_NAME="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"

# ── Validation check ─────────────────────────────────────────────
VALID_AGENTS=("project-planner" "pm" "be-coding" "qa-be" "fe-coding" "qa-fe")

if [[ -z "$AGENT_NAME" ]]; then
    echo ""
    echo "Usage: bash scripts/run-agent.sh <agent_name> [options]"
    echo ""
    echo "Agent list:"
    echo "  project-planner  --project <description>      Project breakdown → tickets/ creation"
    echo "  pm               --ticket-file <path>         Ticket → API/UI specs + wireframe creation"
    echo "  be-coding        --ticket <ticket-number>     Backend code implementation"
    echo "  fe-coding        --ticket <ticket-number>     Frontend code implementation"
    echo "  qa-be            --ticket <ticket-number>     Backend test writing"
    echo "  qa-fe            --ticket <ticket-number>     Frontend test writing"
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

# ── Flag parsing ──────────────────────────────────────────────
shift  # Remove agent_name, parse remaining flags
TICKET_FILE=""
TICKET_NUM=""
PROJECT_DESC=""
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

# ── Validate required options per agent and set initial prompt ────────────
case "$AGENT_NAME" in
    project-planner)
        if [[ "$RESUME_MODE" == true ]]; then
            # Resume mode: check for plan file existence
            LATEST_PLAN=$(ls -t "$WORKSPACE_ROOT/tickets/.plan-"*.json 2>/dev/null | head -1)
            if [[ -z "$LATEST_PLAN" ]]; then
                echo "❌ No plan file to resume from."
                echo "   tickets/.plan-*.json file is required."
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
            echo "   Example: bash scripts/run-agent.sh pm --ticket-file ./tickets/PLAN-001-user-auth.md"
            exit 1
        fi
        if [[ ! -f "$TICKET_FILE" ]]; then
            echo "❌ Ticket file not found: $TICKET_FILE"
            exit 1
        fi
        INITIAL_PROMPT="$(cat "$TICKET_FILE")"
        ;;
    be-coding|fe-coding|qa-be|qa-fe)
        if [[ -z "$TICKET_NUM" ]]; then
            echo "❌ $AGENT_NAME requires --ticket option."
            echo "   Example: bash scripts/run-agent.sh $AGENT_NAME --ticket PLAN-001"
            exit 1
        fi
        INITIAL_PROMPT="Working on ticket $TICKET_NUM."
        ;;
esac

# ── Check CLAUDE.md exists ──────────────────────────────────────
AGENT_DIR="$WORKSPACE_ROOT/.agents/$AGENT_NAME"
CLAUDE_MD="$AGENT_DIR/CLAUDE.md"

if [[ ! -f "$CLAUDE_MD" ]]; then
    echo "❌ CLAUDE.md not found: $CLAUDE_MD"
    exit 1
fi

# ── claude CLI check ──────────────────────────────────────────
if ! command -v claude &>/dev/null; then
    echo "❌ claude CLI not found."
    echo "   Check if Claude Code is installed."
    echo "   Installation: https://docs.claude.ai/claude-code"
    exit 1
fi

# ── Rate Limit pre-record ─────────────────────────────────────
python3 "$SCRIPT_DIR/parse_usage.py" "$AGENT_NAME" --log 2>/dev/null || true

# ── Agent start ────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║  Agent start: $AGENT_NAME"
echo "║  Workspace: $WORKSPACE_ROOT"
echo "║  Instruction file: .agents/$AGENT_NAME/CLAUDE.md"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "💡 The agent will automatically perform the Rate Limit check."
echo "   Exit: Ctrl+C"
echo ""

# ── Execute claude ──────────────────────────────────────────────
# --append-system-prompt: Keep Claude Code defaults while adding CLAUDE.md
# (--system-prompt would remove Claude Code's built-in tool descriptions, so don't use it)
echo "📝 Handing over the initial prompt to the agent..."
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
