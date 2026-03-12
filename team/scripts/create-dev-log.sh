#!/bin/bash
# Agent system development log creation script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
LOGS_DIR="$WORKSPACE_ROOT/../logs-agent_dev"

TOPIC="$1"

if [[ -z "$TOPIC" ]]; then
    echo ""
    echo "Usage: bash scripts/create-dev-log.sh <topic>"
    echo ""
    echo "Examples:"
    echo "  bash scripts/create-dev-log.sh git-branch-automation"
    echo "  bash scripts/create-dev-log.sh rate-limit-optimization"
    echo "  bash scripts/create-dev-log.sh new-agent-implementation"
    echo ""
    exit 1
fi

DATE=$(date +%Y%m%d)
FILENAME="$LOGS_DIR/${DATE}-${TOPIC}.md"

# Create logs directory if it doesn't exist
if [[ ! -d "$LOGS_DIR" ]]; then
    mkdir -p "$LOGS_DIR"
    echo "📁 logs-agent_dev/ directory created"
fi

# Warn if file already exists
if [[ -f "$FILENAME" ]]; then
    echo "⚠️  File already exists: $FILENAME"
    echo "   Overwrite? (y/N)"
    read -r CONFIRM
    if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
        echo "❌ Cancelled."
        exit 0
    fi
fi

# Create template
cat > "$FILENAME" <<EOF
# [${DATE}] ${TOPIC}

## Overview

{2-3 line summary of what was improved}

## Problem

{What problems existed previously}

## Solution

### 1. {Method 1}

{Description}

### 2. {Method 2}

{Description}

## Changed Files

### KR Version
- \`path/to/file1.md\` - {Changes}
- \`path/to/file2.sh\` - {Changes}

### ENG Version
- \`path/to/file1.md\` - {Changes}

## Newly Created Files

### KR Version
- \`path/to/new-file.json\` - {Purpose}

### ENG Version
- \`path/to/new-file.json\` - {Purpose}

## Usage Example

\`\`\`bash
# Example command
\`\`\`

## Workflow

\`\`\`
1. {Step 1}
   ↓
2. {Step 2}
   ↓
3. {Step 3}
\`\`\`

## Impact Scope

- [ ] KR version (\`KR-multi-agent-coding-team/\`)
- [ ] ENG version (\`ENG-multi-agent-coding-team/\`)
- [ ] Compatibility: {Impact on existing users}

## Test Checklist

- [ ] {Test item 1}
- [ ] {Test item 2}
- [ ] {Test item 3}
- [ ] Test agent execution in actual project (user)

## Related Issues/Requests

**User Request:**
> {Request content}

**GitHub Issue:**
- #{Issue number}

## Reference Documentation

- \`path/to/doc.md\` - {Description}

## Key Configuration (if applicable)

\`\`\`json
{
  "key": "value"
}
\`\`\`

## Future Improvement Plan

- [ ] {Improvement item 1}
- [ ] {Improvement item 2}

## Known Limitations

1. **{Limitation 1}**: {Description}
2. **{Limitation 2}**: {Description}

## Notes

- {Additional note 1}
- {Additional note 2}
EOF

echo ""
echo "✅ Development log template created!"
echo ""
echo "📄 File: $FILENAME"
echo ""
echo "Next steps:"
echo "  1. Open file in editor and write content."
echo "  2. Commit to Git after writing."
echo ""
echo "  code \"$FILENAME\""
echo ""
