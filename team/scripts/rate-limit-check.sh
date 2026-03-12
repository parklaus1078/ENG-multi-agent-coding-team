#!/bin/bash
# Rate limit pre-check script
# Usage: bash scripts/rate-limit-check.sh <agent_name>
#
# Exit codes:
#   0 = OK (available)
#   1 = WARN (warning, user decision needed)
#   2 = STOP (halt recommended)

AGENT_NAME="${1:-unknown}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Rate Limit Check | Agent: $AGENT_NAME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "❌ python3 not found."
    exit 0  # Allow proceed if check unavailable (conservative failure prevention)
fi

# Execute parse_usage.py
python3 "$SCRIPT_DIR/parse_usage.py" "$AGENT_NAME"
EXIT_CODE=$?

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

exit $EXIT_CODE
