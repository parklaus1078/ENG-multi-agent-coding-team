#!/bin/bash
# Git branch management helper script
# Utility called by coding agents before and after work

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$WORKSPACE_ROOT/.config/git-workflow.json"

# ── Read configuration file ─────────────────────────────────
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "⚠️  Configuration file not found: $CONFIG_FILE"
    echo "   Proceeding with default settings."
    BASE_BRANCH="dev"
    ENABLED=true
else
    BASE_BRANCH=$(jq -r '.branch_strategy.base_branch // "dev"' "$CONFIG_FILE")
    ENABLED=$(jq -r '.branch_strategy.enabled // true' "$CONFIG_FILE")
    AUTO_CREATE=$(jq -r '.branch_strategy.auto_create // true' "$CONFIG_FILE")
    AUTO_CHECKOUT=$(jq -r '.branch_strategy.auto_checkout // true' "$CONFIG_FILE")
    CHECK_UNCOMMITTED=$(jq -r '.safety.check_uncommitted_changes // true' "$CONFIG_FILE")
    STASH_BEFORE=$(jq -r '.safety.stash_before_checkout // true' "$CONFIG_FILE")
fi

# ── Handle subcommands ──────────────────────────────────────

case "${1:-}" in
    # ── prepare: Prepare branch before work ────────────────
    prepare)
        AGENT_NAME="${2:-}"
        TICKET_NUM="${3:-}"
        SLUG="${4:-}"

        if [[ "$ENABLED" != "true" ]]; then
            echo "ℹ️  Git branch auto-management is disabled."
            exit 0
        fi

        if [[ -z "$AGENT_NAME" || -z "$TICKET_NUM" ]]; then
            echo "❌ Usage: bash scripts/git-branch-helper.sh prepare <agent-name> <ticket-number> [slug]"
            exit 1
        fi

        # Determine prefix by agent and set base branch
        case "$AGENT_NAME" in
            # v0.0.2 unified agents
            coding)
                PREFIX="feature"
                # coding branches from base_branch (main/dev)
                ;;
            qa)
                PREFIX="test"
                # qa branches from same ticket's feature branch
                FEATURE_BRANCH="feature/$TICKET_NUM"
                if [[ -n "$SLUG" ]]; then
                    FEATURE_BRANCH="feature/$TICKET_NUM-$SLUG"
                fi
                # Check if feature branch exists
                if git show-ref --verify --quiet "refs/heads/$FEATURE_BRANCH"; then
                    BASE_BRANCH="$FEATURE_BRANCH"
                    echo "📌 QA branch will be created from feature branch: $FEATURE_BRANCH"
                else
                    echo "⚠️  Feature branch not found: $FEATURE_BRANCH"
                    echo "   Run coding agent first."
                    echo "   Or using default base branch: $BASE_BRANCH"
                fi
                ;;
            pm)
                PREFIX="docs"
                # pm branches from base_branch
                ;;
            *)
                echo "⚠️  Unknown agent: $AGENT_NAME"
                PREFIX="feature"
                ;;
        esac

        # Generate branch name
        if [[ -n "$SLUG" ]]; then
            BRANCH_NAME="$PREFIX/$TICKET_NUM-$SLUG"
        else
            BRANCH_NAME="$PREFIX/$TICKET_NUM"
        fi

        echo ""
        echo "╔══════════════════════════════════════════════╗"
        echo "║  Git Branch Preparation"
        echo "║  Base: $BASE_BRANCH"
        echo "║  Target: $BRANCH_NAME"
        echo "╚══════════════════════════════════════════════╝"
        echo ""

        # Check current branch
        CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

        if [[ "$CURRENT_BRANCH" == "$BRANCH_NAME" ]]; then
            echo "✅ Already on target branch: $BRANCH_NAME"
            exit 0
        fi

        # Check uncommitted changes
        if [[ "$CHECK_UNCOMMITTED" == "true" ]]; then
            if ! git diff-index --quiet HEAD -- 2>/dev/null; then
                if [[ "$STASH_BEFORE" == "true" ]]; then
                    echo "⚠️  Uncommitted changes detected. Saving to stash."
                    git stash push -m "Auto-stash before switching to $BRANCH_NAME"
                    echo "💾 Stash saved. Restore later with 'git stash pop'."
                else
                    echo "❌ Uncommitted changes detected."
                    echo "   Commit or stash first."
                    echo "   Or set stash_before_checkout to true in .config/git-workflow.json."
                    exit 1
                fi
            fi
        fi

        # Update base branch
        echo "📥 Updating base branch: $BASE_BRANCH"
        git fetch origin "$BASE_BRANCH" 2>/dev/null || true

        # Check if branch exists
        if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
            # Branch exists → checkout
            echo "🔀 Switching to existing branch: $BRANCH_NAME"
            git checkout "$BRANCH_NAME"
        else
            # Branch doesn't exist
            if [[ "$AUTO_CREATE" == "true" ]]; then
                echo "🌿 Creating new branch: $BRANCH_NAME (from $BASE_BRANCH)"
                git checkout -b "$BRANCH_NAME" "origin/$BASE_BRANCH" 2>/dev/null || \
                git checkout -b "$BRANCH_NAME" "$BASE_BRANCH"
                echo "✅ Branch created"
            else
                echo "❌ Branch doesn't exist and auto_create is disabled."
                echo "   Enable auto_create in .config/git-workflow.json or"
                echo "   Create branch manually: git checkout -b $BRANCH_NAME $BASE_BRANCH"
                exit 1
            fi
        fi

        echo ""
        echo "✅ Branch ready: $BRANCH_NAME"
        echo ""
        ;;

    # ── status: Check current Git status ───────────────────
    status)
        CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
        echo ""
        echo "📍 Current branch: $CURRENT_BRANCH"
        echo "📌 Base branch (configured): $BASE_BRANCH"
        echo ""

        if ! git diff-index --quiet HEAD -- 2>/dev/null; then
            echo "📝 Uncommitted changes:"
            git status --short
        else
            echo "✅ Working directory clean (no uncommitted changes)"
        fi
        echo ""
        ;;

    # ── cleanup: Clean up after work completion ────────────
    cleanup)
        echo "🧹 Branch cleanup must be done manually."
        echo "   - Delete unnecessary branches: git branch -d <branch-name>"
        echo "   - Delete remote branches: git push origin --delete <branch-name>"
        ;;

    # ── config: View configuration ──────────────────────────
    config)
        if [[ -f "$CONFIG_FILE" ]]; then
            echo ""
            echo "📋 Current Git Workflow Configuration:"
            echo ""
            cat "$CONFIG_FILE" | jq '.'
            echo ""
        else
            echo "⚠️  Configuration file not found: $CONFIG_FILE"
        fi
        ;;

    # ── help ────────────────────────────────────────────────
    *)
        echo ""
        echo "Git Branch Management Helper Script"
        echo ""
        echo "Usage:"
        echo "  bash scripts/git-branch-helper.sh prepare <agent-name> <ticket-number> [slug]"
        echo "    → Prepare branch before work (create or switch)"
        echo ""
        echo "  bash scripts/git-branch-helper.sh status"
        echo "    → Check current Git status"
        echo ""
        echo "  bash scripts/git-branch-helper.sh config"
        echo "    → View current configuration"
        echo ""
        echo "Examples:"
        echo "  bash scripts/git-branch-helper.sh prepare coding PLAN-001 user-auth"
        echo "  → Create/switch to feature/PLAN-001-user-auth branch"
        echo ""
        echo "  bash scripts/git-branch-helper.sh prepare qa PLAN-001"
        echo "  → Create/switch to test/PLAN-001 branch"
        echo ""
        exit 1
        ;;
esac
