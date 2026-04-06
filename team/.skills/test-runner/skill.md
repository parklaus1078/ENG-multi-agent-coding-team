# Test Runner Skill

> **Purpose**: Automated test execution and result analysis
>
> **Type**: Testing Skill
>
> **Thariq's Lesson**: "Automate testing to catch bugs early"

---

## 🎯 Triggers

### Auto Trigger
- Auto-pipeline: After QA Agent completion
- Git hook: pre-commit (optional)
- CI/CD: GitHub Actions

### Manual Trigger
```bash
# Run all tests
bash scripts/run-skill.sh test-runner --all

# Test specific file
bash scripts/run-skill.sh test-runner --file tests/auth/test_login.py

# Test specific directory
bash scripts/run-skill.sh test-runner --dir tests/auth/

# Include coverage
bash scripts/run-skill.sh test-runner --all --coverage

# Quick tests only (unit)
bash scripts/run-skill.sh test-runner --unit
```

---

## 🔍 Features

### 1. Automatic Test Framework Detection

**Supported Frameworks**:
- **JavaScript/TypeScript**: Jest, Mocha, Vitest
- **Python**: pytest, unittest
- **Go**: go test
- **Rust**: cargo test

**Detection Logic**:
```python
def detect_test_framework(project_root):
    # Check package.json
    if exists("package.json"):
        package = load_json("package.json")
        if "jest" in package["devDependencies"]:
            return "jest"
        elif "mocha" in package["devDependencies"]:
            return "mocha"

    # Check Python
    if exists("pytest.ini") or exists("setup.py"):
        return "pytest"

    # Check Go
    if exists("go.mod"):
        return "go test"

    return None
```

### 2. Automated Test Execution

**Execution Flow**:
```python
1. Detect test framework
2. Find test files
3. Run tests
4. Parse results
5. Generate report
```

**Parallel Execution**:
```bash
# Jest
npm test -- --maxWorkers=4

# pytest
pytest -n 4

# Go
go test -parallel 4 ./...
```

### 3. Coverage Measurement

**Coverage Tools**:
- **JavaScript**: Istanbul/NYC
- **Python**: coverage.py
- **Go**: go test -cover
- **Rust**: cargo-tarpaulin

**Threshold Checking**:
```python
coverage_thresholds = {
    "statements": 80,
    "branches": 75,
    "functions": 80,
    "lines": 80
}

if coverage < thresholds:
    return {
        "status": "failed",
        "message": f"Insufficient coverage: {coverage}% < {threshold}%"
    }
```

### 4. Test Result Analysis

**Metrics**:
- Total test count
- Passed/Failed/Skipped
- Execution time
- Slow tests (> 1s)
- Flaky tests

**Analysis Example**:
```python
{
    "total": 150,
    "passed": 145,
    "failed": 3,
    "skipped": 2,
    "duration": "12.5s",
    "slow_tests": [
        {"name": "test_large_dataset", "duration": "3.2s"},
        {"name": "test_api_integration", "duration": "2.1s"}
    ],
    "flaky_tests": [
        {"name": "test_async_timeout", "failure_rate": 0.15}
    ]
}
```

---

## 📤 Output Format

### Test Report

```markdown
# Test Report

## Summary
- **Total Tests**: 150
- **Passed**: ✅ 145 (96.7%)
- **Failed**: ❌ 3 (2.0%)
- **Skipped**: ⏭️ 2 (1.3%)
- **Duration**: 12.5s
- **Coverage**: 85% ✅

---

## Failed Tests

### 1. test_login_with_invalid_credentials
**File**: `tests/auth/test_login.py:45`
**Error**: AssertionError: Expected 401, got 500
**Duration**: 0.3s

```python
def test_login_with_invalid_credentials():
    response = client.post("/login", json={"email": "wrong@example.com"})
    assert response.status_code == 401  # ❌ Got 500
```

**Suggestion**: Server returned 500 error - check error handling

---

### 2. test_user_profile_update
**File**: `tests/user/test_profile.py:78`
**Error**: Timeout after 5s
**Duration**: 5.0s

**Suggestion**: Improve API response time or increase timeout

---

## Slow Tests (> 1s)

| Test | Duration | File |
|------|----------|------|
| test_large_dataset | 3.2s | tests/data/test_processing.py:120 |
| test_api_integration | 2.1s | tests/integration/test_api.py:55 |
| test_db_migration | 1.8s | tests/db/test_migrations.py:30 |

**Suggestion**: Consider parallelization or reducing test data

---

## Coverage Report

| File | Coverage | Missing Lines |
|------|----------|---------------|
| src/auth/login.js | 95% | 45-47, 89 |
| src/auth/token.js | 88% | 23-25 |
| src/user/profile.js | 72% ⚠️ | 34-50, 78-90 |

**Overall**: 85% ✅ (threshold: 80%)

---

## Recommendations

1. 🔴 **Fix failing tests** (3 tests)
2. 🟡 **Improve coverage** for user/profile.js (72% → 80%+)
3. 🟡 **Optimize slow tests** (3 tests > 1s)
4. 🟢 **Consider mocking** for API integration tests
```

---

## 🧠 Memory Utilization

### test-history.json

```json
{
  "version": "0.0.1",
  "project": "multi-agent-coding-team",

  "test_runs": [
    {
      "timestamp": "2026-03-19T11:00:00Z",
      "total": 150,
      "passed": 145,
      "failed": 3,
      "duration": 12.5,
      "coverage": 0.85
    }
  ],

  "flaky_tests": [
    {
      "name": "test_async_timeout",
      "file": "tests/async/test_timeout.py",
      "failure_rate": 0.15,
      "last_failures": [
        "2026-03-18T10:00:00Z",
        "2026-03-17T14:00:00Z"
      ]
    }
  ],

  "slow_tests": [
    {
      "name": "test_large_dataset",
      "avg_duration": 3.2,
      "trend": "increasing"
    }
  ],

  "coverage_trend": [
    {"date": "2026-03-15", "coverage": 0.82},
    {"date": "2026-03-18", "coverage": 0.84},
    {"date": "2026-03-19", "coverage": 0.85}
  ],

  "common_failures": [
    {
      "error": "Timeout",
      "frequency": 8,
      "tests": ["test_api_integration", "test_async_timeout"]
    },
    {
      "error": "AssertionError",
      "frequency": 5,
      "tests": ["test_login_with_invalid_credentials"]
    }
  ]
}
```

---

## ⚠️ Gotchas

### 1. No Test Order Dependencies

**Verification**:
```python
# Run tests in random order
pytest --random-order

# If it fails, there is order dependency
if random_run_failed and sequential_run_passed:
    raise Error("Tests depend on execution order")
```

### 2. Test Environment Isolation

**Principles**:
- Each test is independent
- DB uses transaction rollback or temporary DB
- File system uses temporary directory

**Example**:
```python
# ✅ Correct
@pytest.fixture
def db_session():
    session = create_session()
    yield session
    session.rollback()  # Isolate with rollback

# ❌ Wrong
def test_create_user():
    # Permanent DB change - affects other tests
    db.users.insert({"name": "test"})
```

### 3. Flaky Test Tracking

**Detection**:
```python
# Run the same test 10 times
for i in range(10):
    result = run_test("test_async_timeout")
    if result != "passed":
        flaky_count += 1

if flaky_count > 0:
    mark_as_flaky("test_async_timeout", flaky_count / 10)
```

### 4. Prevent Coverage Regression

**Verification**:
```python
old_coverage = get_coverage_from_history()
new_coverage = run_tests_with_coverage()

if new_coverage < old_coverage - 5:  # 5%+ decrease
    raise Error(f"Coverage regression: {old_coverage}% → {new_coverage}%")
```

---

## 🔧 Advanced Features

### 1. Automatic Test Retry

**Flaky Test Retry**:
```python
# pytest
@pytest.mark.flaky(reruns=3, reruns_delay=1)
def test_async_timeout():
    # Retry up to 3 times, 1 second delay
    pass
```

### 2. Parallel Testing

**Configuration**:
```python
# Jest
{
  "jest": {
    "maxWorkers": "50%"
  }
}

# pytest
pytest -n auto  # Use number of CPU cores
```

### 3. Selective Test Execution

**Based on Changed Files**:
```bash
# Find changed files with git diff
changed_files=$(git diff --name-only HEAD~1)

# Run only related tests
jest --findRelatedTests $changed_files
```

### 4. Mutation Testing

**Concept**: Mutate code to verify tests can detect the changes

**Tools**:
- JavaScript: Stryker
- Python: mutmut

**Example**:
```python
# Original code
def is_adult(age):
    return age >= 18

# Mutation
def is_adult(age):
    return age > 18  # >= → >

# Test should fail
def test_is_adult():
    assert is_adult(18) == True  # Mutation detected!
```

---

## 📊 Expected Benefits

### Before (Manual Testing)

```
Write code → Manual test run (5 min)
          → Check failures
          → Fix
          → Re-run
```

**Problems**:
- ❌ Time consuming
- ❌ Tests can be skipped
- ❌ Coverage not measured
- ❌ Flaky tests ignored

### After (Automated Testing)

```
Write code → test-runner skill (automatic)
          → Generate report (1 min)
          → Analyze failure causes
          → Track flaky tests
```

**Improvements**:
- ✅ Immediate feedback
- ✅ 100% test execution
- ✅ Automatic coverage measurement
- ✅ Flaky test detection

### Numerical Goals

| Item | Goal |
|------|------|
| **Test execution time** | **-50%** (parallelization) |
| **Coverage tracking** | **100%** |
| **Flaky test detection** | **90%+** |
| **Failure analysis** | **Automatic** |

---

## 🔗 Integration

### Auto-pipeline Integration

```python
# auto_pipeline.py

# After QA Agent completion
result_qa = self.run_agent("qa", qa_prompt, ticket_num)

# Execute Test Runner Skill
test_result = self.run_skill("test-runner", {
    "mode": "all",
    "coverage": True
})

if not test_result["all_passed"]:
    print(f"❌ Tests failed: {test_result['failed']} tests")
    print(f"   Details: {test_result['report_path']}")

    # Re-run QA Agent
    retry_prompt = self._build_test_retry_prompt(test_result)
    result_qa = self.run_agent("qa", retry_prompt, ticket_num)

    # Re-test
    test_retry = self.run_skill("test-runner", {"mode": "all"})

    if not test_retry["all_passed"]:
        raise Exception("Re-test failed - manual intervention required")

if test_result["coverage"] < 80:
    print(f"⚠️  Insufficient coverage: {test_result['coverage']}%")
else:
    print(f"✅ All tests passed, coverage: {test_result['coverage']}%")
```

### GitHub Actions Integration

```yaml
# .github/workflows/test.yml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run test-runner skill
        run: |
          bash scripts/run-skill.sh test-runner --all --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

---

## 📝 Logs

**Test Logs**: `projects/{project}/logs/test-runner/{timestamp}.json`

```json
{
  "timestamp": "2026-03-19T11:00:00Z",
  "framework": "pytest",
  "total_tests": 150,
  "passed": 145,
  "failed": 3,
  "skipped": 2,
  "duration_seconds": 12.5,
  "coverage": 0.85,
  "failed_tests": [
    {
      "name": "test_login_with_invalid_credentials",
      "file": "tests/auth/test_login.py",
      "line": 45,
      "error": "AssertionError: Expected 401, got 500",
      "duration": 0.3
    }
  ],
  "slow_tests": [
    {
      "name": "test_large_dataset",
      "duration": 3.2
    }
  ]
}
```

---

**Related Documents**:
- [test-runner.py](test-runner.py) - Actual implementation
- [test-history.json](../../.memory/test-history.json) - Test history
