# Commit Skill

> **Purpose**: Automatically generate semantic commit messages according to project conventions
>
> **Type**: Code Quality Skill
>
> **Thariq's Lesson**: "Skills for repetitive workflows"

---

## 🎯 Triggers

### Automatic Triggers
- Auto-pipeline: After Coding Agent + QA Agent completion
- Git pre-commit hook: Automatically executed before commit

### Manual Triggers
```bash
# Command
bash scripts/run-skill.sh commit PLAN-001

# Or directly
python3 .skills/commit/commit-message-generator.py --ticket PLAN-001
```

---

## 📋 Process

### 1. Git Diff Analysis

```bash
# Check changes
git diff --cached --stat
git diff --cached --name-status
```

**Extracted Information**:
- List of changed files
- File type (added/modified/deleted)
- Number of changed lines

### 2. Determine Commit Type

**Rules**:
- **feat**: New feature addition (A file, new function/class)
- **fix**: Bug fix (M file, error handling added)
- **test**: Test addition/modification (test/, spec/ files)
- **docs**: Documentation only (README, *.md)
- **refactor**: Refactoring (M file, no functionality change)
- **style**: Formatting (whitespace, semicolons, etc.)
- **chore**: Build/configuration changes (package.json, .gitignore)

**Automatic Decision Logic**:
```python
def determine_type(changed_files):
    if any("test" in f or "spec" in f for f in changed_files):
        return "test"
    elif all(f.endswith(".md") for f in changed_files):
        return "docs"
    elif any(f in ["package.json", ".gitignore", "tsconfig.json"] for f in changed_files):
        return "chore"
    else:
        # Analyze Git diff content
        added_lines = count_added_lines()
        modified_lines = count_modified_lines()

        if added_lines > modified_lines * 2:
            return "feat"
        else:
            return "fix"  # default
```

### 3. Extract Scope

**Ticket Number Based**:
```python
scope = ticket_num  # PLAN-001
```

**Or File Path Based**:
```python
# src/auth/login.js changed → scope: auth
# src/user/profile.js changed → scope: user
```

### 4. Generate Subject

**Rules**:
- Imperative mood (implement, fix, add, update)
- 70 characters or less
- Start with lowercase letter
- No period

**Generation Logic**:
```python
def generate_subject(commit_type, changed_files, ticket_description):
    if commit_type == "feat":
        verb = "implement" or "add"
    elif commit_type == "fix":
        verb = "fix"
    elif commit_type == "test":
        verb = "add tests for"

    # Extract key keywords from ticket description
    keywords = extract_keywords(ticket_description)

    subject = f"{verb} {keywords}"

    # 70 character limit
    if len(subject) > 70:
        subject = subject[:67] + "..."

    return subject
```

### 5. Generate Body (Optional)

**Contents Included**:
- Reason for change (why)
- Main changes (what)
- File paths (if needed)

**Generation Conditions**:
- 3 or more files changed
- Or 100+ lines changed
- Or complex changes (refactoring, migration)

### 6. Add Footer

**Required**:
```
Closes #PLAN-001
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Optional**:
```
Breaking-Change: API endpoint changed
Refs: #PLAN-002, #PLAN-003
```

---

## 📤 Output Format

### Basic Template

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Example 1: Feature

```
feat(PLAN-001): implement JWT authentication

Added login/logout endpoints with token generation.
Password hashing uses bcrypt with salt rounds=12.

Closes #PLAN-001
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Example 2: Bug Fix

```
fix(PLAN-003): resolve null pointer in user profile

Fixed crash when user has no avatar image.
Added null check before accessing avatar.url property.

Closes #PLAN-003
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Example 3: Test

```
test(PLAN-005): add unit tests for payment module

Covers success cases, edge cases, and error handling.

Closes #PLAN-005
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## 🧠 Memory Utilization

### commit-history.json

**Purpose**: Learn consistent vocabulary per project

```json
{
  "project": "my-todo-app",
  "vocabulary": {
    "auth": ["authentication", "login", "logout", "token"],
    "user": ["profile", "settings", "preferences"],
    "task": ["todo", "item", "completion"]
  },
  "frequent_verbs": {
    "feat": ["implement", "add", "create"],
    "fix": ["fix", "resolve", "correct"],
    "refactor": ["refactor", "improve", "optimize"]
  },
  "recent_commits": [
    {
      "hash": "abc123",
      "message": "feat(PLAN-001): implement user authentication",
      "files": ["src/auth/login.js", "src/auth/token.js"],
      "timestamp": "2026-03-19T10:00:00Z"
    }
  ]
}
```

**Learning Method**:
```python
def learn_from_history():
    # Analyze last 50 commits from Git log
    commits = git_log(limit=50)

    # Extract frequently used words
    vocabulary = extract_vocabulary(commits)

    # Check consistency (use same terms for same scope)
    consistency_score = check_consistency(commits)

    # Update commit-history.json
```

---

## ⚠️ Gotchas

### 1. Don't Include File Paths in Subject

❌ **Wrong Example**:
```
feat(PLAN-001): implement src/auth/login.js
```

✅ **Correct Example**:
```
feat(PLAN-001): implement user authentication

Files modified:
- src/auth/login.js
- src/auth/token.js
```

### 2. Don't Commit When Tests Fail

**Validation**:
```bash
# Run tests before commit
npm test || exit 1
pytest || exit 1
```

**Auto-pipeline Integration**:
```python
# Commit after QA Agent completion
if qa_result["all_tests_passed"]:
    run_skill("commit", ticket_num)
else:
    print("Tests failed - skipping commit")
```

### 3. Don't Mix Changes from Multiple Tickets

**Detection**:
```python
# Extract ticket numbers from changed files
files_tickets = extract_tickets_from_files(changed_files)

if len(files_tickets) > 1:
    print("⚠️  Multiple tickets detected. Commit per ticket.")
    sys.exit(1)
```

### 4. Prevent Empty Commits

**Validation**:
```bash
git diff --cached --quiet
if [ $? -eq 0 ]; then
    echo "No changes - skipping commit"
    exit 0
fi
```

---

## 🔧 Usage

### Manual Execution

```bash
# Basic
bash scripts/run-skill.sh commit PLAN-001

# Dry-run (no actual commit)
bash scripts/run-skill.sh commit PLAN-001 --dry-run

# Generate message only (commit after approval)
bash scripts/run-skill.sh commit PLAN-001 --generate-only
```

### Auto-pipeline Integration

```python
# auto_pipeline.py

# After QA Agent completion
result_qa = self.run_agent("qa", qa_prompt, ticket_num)

# Execute Commit Skill
commit_result = self.run_skill("commit", ticket_num)

if commit_result["success"]:
    print(f"✅ Commit completed: {commit_result['commit_hash']}")
else:
    print(f"❌ Commit failed: {commit_result['error']}")
```

### Git Hook Integration

```bash
# .git/hooks/prepare-commit-msg
#!/bin/bash

# Commit message file
COMMIT_MSG_FILE=$1

# Execute Commit Skill to generate message
python3 .skills/commit/commit-message-generator.py --ticket $TICKET_NUM > $COMMIT_MSG_FILE
```

---

## 📊 Expected Results

### Before (Manual Commit Messages)

```
Manual writing → Inconsistency
    ↓
"fix bug"
"update code"
"wip"
```

**Problems**:
- ❌ No consistency
- ❌ Lack of information
- ❌ Time consuming

### After (Commit Skill)

```
Auto-generated → Consistency
    ↓
"feat(PLAN-001): implement user authentication"
"fix(PLAN-002): resolve login validation error"
"test(PLAN-003): add integration tests for API"
```

**Improvements**:
- ✅ Consistent format
- ✅ Clear information
- ✅ Automated

### Numeric Goals

| Item | Goal |
|------|------|
| **Commit Message Quality** | **+60%** |
| **Writing Time** | **-90%** (vs manual) |
| **Cross-Project Reuse** | **100%** |
| **Git History Readability** | **+80%** |

---

## 🔗 Integration

### Coordination with Other Skills

**validate-spec → commit**:
```
Spec validation passed → Coding Agent → QA Agent → Commit Skill
```

**refactor-code → commit**:
```
Refactoring suggestion → Apply → Commit Skill (type=refactor)
```

### Memory System Integration

**Reference patterns.json**:
```python
# Utilize successful commit message patterns from the past
patterns = load_patterns("commit")

if patterns:
    # Similar changes → use similar message structure
    similar_commit = find_similar(current_changes, patterns)
    message_template = similar_commit["message_template"]
```

---

## 📝 Logs

**Commit Log**: `projects/{project}/logs/commit/{timestamp}-{ticket}.json`

```json
{
  "ticket": "PLAN-001",
  "timestamp": "2026-03-19T10:30:00Z",
  "commit_hash": "abc123def456",
  "commit_type": "feat",
  "scope": "PLAN-001",
  "subject": "implement user authentication",
  "changed_files": ["src/auth/login.js", "src/auth/token.js"],
  "added_lines": 150,
  "deleted_lines": 10,
  "confidence": 0.92,
  "auto_generated": true
}
```

---

**Related Documents**:
- [commit-message-generator.py](commit-message-generator.py) - Actual implementation
- [commit-history.json](../../.memory/commit-history.json) - Learning data
- [Phase 3.1 documentation](../../../docs/phase3.1-complete.md)
