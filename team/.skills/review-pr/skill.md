# Review PR Skill

> **Purpose**: Automated Pull Request Review - Code Quality Inspection and Improvement Suggestions
>
> **Type**: Code Quality Skill
>
> **Thariq's Lesson**: "Validation skills catch errors early"

---

## 🎯 Triggers

### Auto Triggers
- Auto-pipeline: Immediately after PR creation
- GitHub Actions: When PR event occurs
- Git hook: pre-push

### Manual Triggers
```bash
# Review by PR number
bash scripts/run-skill.sh review-pr 123

# Review current branch
bash scripts/run-skill.sh review-pr --current-branch

# Review specific ticket
bash scripts/run-skill.sh review-pr --ticket PLAN-001
```

---

## 📋 Review Checklist

### 1. Completeness Check

**Ticket Requirements Met**:
- [ ] All ticket Acceptance Criteria implemented
- [ ] Out-of-Scope items not implemented
- [ ] Specification matches implementation

**Code Completeness**:
- [ ] All functions implemented (no TODO, FIXME)
- [ ] Error handling present
- [ ] Edge cases handled

**Test Completeness**:
- [ ] Unit tests present
- [ ] Integration tests present (when needed)
- [ ] Test coverage 80%+

### 2. Quality Check

**Code Quality**:
- [ ] Function length < 50 lines
- [ ] Cyclomatic complexity < 10
- [ ] No duplicate code
- [ ] Clear naming (variables, functions, classes)
- [ ] No magic numbers (use constants)

**Architecture**:
- [ ] Single Responsibility Principle (SRP)
- [ ] DRY (Don't Repeat Yourself)
- [ ] Coding rules compliance (.rules/ reference)

**Security**:
- [ ] No hardcoded passwords/API keys
- [ ] SQL Injection protection
- [ ] XSS protection
- [ ] CSRF protection (when needed)
- [ ] Input validation present

### 3. Style Check

**Formatting**:
- [ ] Linter passed (ESLint, Pylint, etc.)
- [ ] Consistent indentation
- [ ] Consistent bracket style
- [ ] No unnecessary whitespace

**Comments**:
- [ ] Comments on complex logic
- [ ] No typos in comments
- [ ] No commented-out code (delete)

### 4. Performance Check

**General**:
- [ ] No N+1 queries
- [ ] No unnecessary loops
- [ ] No memory leaks

**Async**:
- [ ] Async/await used appropriately
- [ ] Promise chains optimized
- [ ] Parallelizable tasks parallelized

### 5. Documentation Check

**Code Documentation**:
- [ ] Public API has docstring/JSDoc
- [ ] Complex algorithms explained

**Change Documentation**:
- [ ] CHANGELOG updated (when needed)
- [ ] README updated (on API changes)

---

## 🔍 Auto Check Items

### Static Analysis

```python
def run_static_analysis(files):
    issues = []

    # Linter
    lint_result = run_linter(files)
    issues.extend(lint_result)

    # Complexity
    complexity = calculate_complexity(files)
    if complexity > 10:
        issues.append({
            "type": "complexity",
            "severity": "warning",
            "message": f"Cyclomatic complexity too high: {complexity}"
        })

    # Security
    security_issues = run_security_scan(files)
    issues.extend(security_issues)

    return issues
```

**Tool Integration**:
- ESLint / Pylint - Style checking
- Bandit / Safety - Security checking
- SonarQube - Code quality
- Coverage.py / Istanbul - Coverage

### Pattern Detection

**Anti-pattern Detection**:
```python
anti_patterns = [
    {
        "name": "God Object",
        "pattern": r"class \w+ {[\s\S]{2000,}}",  # 2000+ line class
        "severity": "error"
    },
    {
        "name": "Magic Number",
        "pattern": r"if.*==\s*\d{2,}",  # 2+ digit numbers
        "severity": "warning"
    },
    {
        "name": "Hardcoded Secret",
        "pattern": r"(password|api_key|secret)\s*=\s*['\"]",
        "severity": "error"
    }
]
```

---

## 📤 Output Format

### Review Report

```markdown
# PR Review: #123 - Implement User Authentication

## Summary
- **Status**: ⚠️ Changes Requested
- **Reviewed Files**: 5
- **Issues Found**: 3 errors, 2 warnings
- **Test Coverage**: 85% ✅
- **Estimated Review Time**: 15 minutes

---

## Critical Issues (3)

### 1. Security: Hardcoded API Key
**File**: `src/auth/api-client.js:12`
**Severity**: 🔴 Error

```javascript
const API_KEY = "sk-1234567890abcdef";  // ❌
```

**Suggestion**:
```javascript
const API_KEY = process.env.API_KEY;  // ✅
```

**Auto-fix**: Available

---

### 2. Code Quality: Function Too Long
**File**: `src/auth/login.js:45-120`
**Severity**: 🔴 Error

Function `handleLogin` is 75 lines long (limit: 50).

**Suggestion**: Extract validation logic to separate function.

**Auto-fix**: Not available (manual refactoring needed)

---

## Warnings (2)

### 1. Style: Inconsistent Naming
**File**: `src/auth/token.js:23`
**Severity**: 🟡 Warning

```javascript
const JWT_token = generateToken();  // mixed camelCase + PascalCase
```

**Suggestion**:
```javascript
const jwtToken = generateToken();  // ✅
```

---

## Suggestions

### Performance Optimization
Consider using parallel API calls in `src/auth/verify.js:34`:
```javascript
// Before
const user = await fetchUser(id);
const permissions = await fetchPermissions(id);

// After
const [user, permissions] = await Promise.all([
  fetchUser(id),
  fetchPermissions(id)
]);
```

---

## Test Coverage

| File | Coverage | Status |
|------|----------|--------|
| src/auth/login.js | 90% | ✅ |
| src/auth/token.js | 85% | ✅ |
| src/auth/verify.js | 75% | ⚠️ |

**Overall**: 85% ✅

---

## Approval Status

❌ **Changes Requested**

Please fix 3 critical issues before approval.

**Auto-fixable**: 1 issue
Run: `bash scripts/run-skill.sh review-pr 123 --auto-fix`
```

---

## 🔧 Auto-Fix Feature

### Fixable Issues

1. **Hardcoded Passwords**:
   ```python
   "password": "admin123" → "password": process.env.PASSWORD
   ```

2. **Import Sorting**:
   ```python
   # Alphabetical sorting
   import z_module
   import a_module
   →
   import a_module
   import z_module
   ```

3. **Unnecessary Whitespace**:
   ```python
   # Remove
   function foo()  {  // 2 spaces
   →
   function foo() {  // 1 space
   ```

4. **Delete Commented Code**:
   ```python
   # const oldCode = ...;
   # console.log(oldCode);
   → (deleted)
   ```

### Auto-fix Execution

```bash
# Apply auto-fix
bash scripts/run-skill.sh review-pr 123 --auto-fix

# Preview changes
bash scripts/run-skill.sh review-pr 123 --auto-fix --dry-run
```

---

## ⚠️ Gotchas

### 1. Block PRs Without Tests

**Validation**:
```python
if not has_tests(changed_files):
    return {
        "status": "blocked",
        "message": "All PRs must include tests."
    }
```

### 2. Prevent Coverage Decrease

**Validation**:
```python
old_coverage = get_coverage("main")
new_coverage = get_coverage("feature-branch")

if new_coverage < old_coverage - 5:  # 5%+ decrease
    return {
        "status": "warning",
        "message": f"Coverage decreased: {old_coverage}% → {new_coverage}%"
    }
```

### 3. Large PR Warning

**Validation**:
```python
if lines_changed > 500:
    return {
        "status": "warning",
        "message": "PR too large (500+ lines). Consider splitting."
    }
```

### 4. Breaking Change Detection

**Validation**:
```python
if has_breaking_changes(diff):
    return {
        "status": "warning",
        "message": "Breaking change detected. Document in CHANGELOG."
    }
```

---

## 🔗 Integration

### GitHub Actions Integration

```yaml
# .github/workflows/review-pr.yml
name: Auto PR Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run review-pr skill
        run: |
          bash scripts/run-skill.sh review-pr ${{ github.event.pull_request.number }}
      - name: Post comment
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review-report.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review
            });
```

### Auto-pipeline Integration

```python
# auto_pipeline.py

# Create PR after QA Agent completes
pr_number = create_pull_request(ticket_num, branch_name)

# Run PR review
review_result = self.run_skill("review-pr", pr_number)

if review_result["status"] == "approved":
    print("✅ PR approved - ready to merge")
elif review_result["auto_fixable_count"] > 0:
    print(f"⚠️  {review_result['auto_fixable_count']} auto-fixable issues")
    # Run auto-fix
    self.run_skill("review-pr", pr_number, auto_fix=True)
else:
    print(f"❌ {review_result['error_count']} issues require manual fix")
```

---

## 🧠 Memory Utilization

### review-history.json

```json
{
  "project": "my-project",
  "common_issues": [
    {
      "issue": "Hardcoded API Key",
      "frequency": 12,
      "auto_fixed": 10,
      "last_seen": "2026-03-15"
    },
    {
      "issue": "Missing Error Handling",
      "frequency": 8,
      "auto_fixed": 0,
      "last_seen": "2026-03-18"
    }
  ],
  "approval_criteria": {
    "min_coverage": 80,
    "max_complexity": 10,
    "max_function_length": 50
  }
}
```

---

## 📊 Expected Impact

### Before (Manual Review)

```
PR Created → Wait for human review (hours to days)
          → Comments
          → Fix
          → Re-review
```

**Problems**:
- ❌ Slow (waiting time)
- ❌ Inconsistent (reviewer differences)
- ❌ Simple issues need human review

### After (Auto Review)

```
PR Created → review-pr skill (immediate)
          → Report generated (1-2 min)
          → Auto-fix applied (optional)
          → Human review (complex logic only)
```

**Improvements**:
- ✅ Fast (immediate feedback)
- ✅ Consistent (checklist-based)
- ✅ Simple issues auto-fixed

### Numeric Goals

| Metric | Target |
|--------|--------|
| **Review Time** | **-80%** (vs manual) |
| **Simple Issue Detection** | **95%+** |
| **Auto-fix Success Rate** | **80%+** |
| **Human Review Burden** | **-60%** |

---

## 📝 Logs

**Review Log**: `projects/{project}/logs/review-pr/{timestamp}-PR-{number}.json`

```json
{
  "pr_number": 123,
  "timestamp": "2026-03-19T10:30:00Z",
  "status": "changes_requested",
  "errors": 3,
  "warnings": 2,
  "suggestions": 1,
  "auto_fixable": 1,
  "files_reviewed": 5,
  "test_coverage": 0.85,
  "review_time_seconds": 45
}
```

---

**Related Documentation**:
- [review-pr.py](review-pr.py) - Actual implementation
- [review-checklist.json](review-checklist.json) - Checklist configuration
- [auto-fix-rules.json](auto-fix-rules.json) - Auto-fix rules
