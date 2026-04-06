#!/bin/bash
#
# Skill execution wrapper script
#
# Usage:
#   bash scripts/run-skill.sh validate-spec PLAN-001
#   bash scripts/run-skill.sh validate-spec PLAN-001 --auto-fix
#   bash scripts/run-skill.sh validate-spec --all
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEAM_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SKILL_NAME="$1"
shift

if [ -z "$SKILL_NAME" ]; then
    echo "Usage: bash scripts/run-skill.sh <skill-name> [args...]"
    echo ""
    echo "Available skills:"
    echo ""
    echo "Code Quality:"
    echo "  validate-spec  - Validate PM Agent specifications"
    echo "  review-pr      - Automated PR review"
    echo "  refactor-code  - Code refactoring suggestions"
    echo ""
    echo "Development:"
    echo "  commit         - Auto-generate commit messages"
    echo "  test-runner    - Automated test execution"
    echo "  docs-generator - Automated documentation generation"
    echo ""
    echo "Operations:"
    echo "  deploy         - Deployment automation"
    echo "  benchmark      - Performance benchmarking"
    exit 1
fi

SKILL_DIR="$TEAM_ROOT/.skills/$SKILL_NAME"

if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ Skill not found: $SKILL_NAME"
    echo "Path: $SKILL_DIR"
    exit 1
fi

# Execute skill
case "$SKILL_NAME" in
    validate-spec)
        python3 "$SKILL_DIR/validate.py" "$@"
        ;;
    commit)
        python3 "$SKILL_DIR/commit-message-generator.py" "$@"
        ;;
    review-pr)
        python3 "$SKILL_DIR/review-pr.py" "$@"
        ;;
    refactor-code)
        python3 "$SKILL_DIR/refactor-code.py" "$@"
        ;;
    test-runner)
        python3 "$SKILL_DIR/test-runner.py" "$@"
        ;;
    deploy)
        python3 "$SKILL_DIR/deploy.py" "$@"
        ;;
    benchmark)
        python3 "$SKILL_DIR/benchmark.py" "$@"
        ;;
    docs-generator)
        python3 "$SKILL_DIR/docs-generator.py" "$@"
        ;;
    *)
        echo "❌ Unknown skill: $SKILL_NAME"
        exit 1
        ;;
esac
