# Refactor Code Skill

> **Purpose**: Code improvement suggestions - automatic detection and application of refactoring patterns
>
> **Type**: Code Quality Skill
>
> **Thariq's Lesson**: "Scripts for repetitive refactoring"

---

## 🎯 Triggers

### Auto Triggers
- Auto-pipeline: After Coding Agent completes (optional)
- Git hook: pre-commit (optional)
- Weekly cron: Full codebase analysis

### Manual Triggers
```bash
# Refactor specific file
bash scripts/run-skill.sh refactor-code --file src/auth/login.js

# Refactor specific directory
bash scripts/run-skill.sh refactor-code --dir src/auth/

# Refactor entire project
bash scripts/run-skill.sh refactor-code --all

# Dry-run (suggestions only)
bash scripts/run-skill.sh refactor-code --file src/auth/login.js --dry-run
```

---

## 🔍 Detection Patterns

### 1. Code Smells

#### Long Method
**Detection**:
- Function length > 50 lines
- Nesting depth > 3

**Suggestion**:
```javascript
// Before
function processUser(user) {
  // 80 lines of code...
}

// After
function processUser(user) {
  validateUser(user);
  enrichUserData(user);
  saveUser(user);
}

function validateUser(user) { ... }
function enrichUserData(user) { ... }
function saveUser(user) { ... }
```

#### Duplicate Code
**Detection**:
- Duplicate code > 6 lines

**Suggestion**:
```javascript
// Before
function loginUser(credentials) {
  const token = jwt.sign(credentials, SECRET);
  const expiry = Date.now() + 3600000;
  return { token, expiry };
}

function refreshToken(oldToken) {
  const token = jwt.sign(payload, SECRET);
  const expiry = Date.now() + 3600000;
  return { token, expiry };
}

// After
function createTokenResponse(data) {
  const token = jwt.sign(data, SECRET);
  const expiry = Date.now() + 3600000;
  return { token, expiry };
}

function loginUser(credentials) {
  return createTokenResponse(credentials);
}

function refreshToken(oldToken) {
  return createTokenResponse(payload);
}
```

#### Magic Numbers
**Detection**:
- Numeric literals with 2+ digits

**Suggestion**:
```javascript
// Before
if (user.age > 18) { ... }
setTimeout(callback, 3600000);

// After
const ADULT_AGE = 18;
const ONE_HOUR_MS = 3600000;

if (user.age > ADULT_AGE) { ... }
setTimeout(callback, ONE_HOUR_MS);
```

#### Large Class / God Object
**Detection**:
- Class > 300 lines
- Methods > 20

**Suggestion**:
```javascript
// Before
class UserManager {
  // 500 lines
  // 30 methods
}

// After
class UserManager {
  constructor() {
    this.validator = new UserValidator();
    this.repository = new UserRepository();
    this.notifier = new UserNotifier();
  }
}

class UserValidator { ... }
class UserRepository { ... }
class UserNotifier { ... }
```

### 2. Refactoring Patterns

#### Extract Function
**Scenario**: Long functions, duplicate logic

```python
# Before
def process_order(order):
    # Validation
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")

    # Processing
    for item in order.items:
        item.calculate_tax()
        item.apply_discount()

    # Saving
    db.save(order)
    send_confirmation(order)

# After
def process_order(order):
    validate_order(order)
    process_items(order.items)
    finalize_order(order)

def validate_order(order):
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")

def process_items(items):
    for item in items:
        item.calculate_tax()
        item.apply_discount()

def finalize_order(order):
    db.save(order)
    send_confirmation(order)
```

#### Replace Conditional with Polymorphism
**Scenario**: Repeated type checks

```javascript
// Before
function getArea(shape) {
  if (shape.type === 'circle') {
    return Math.PI * shape.radius ** 2;
  } else if (shape.type === 'rectangle') {
    return shape.width * shape.height;
  } else if (shape.type === 'triangle') {
    return 0.5 * shape.base * shape.height;
  }
}

// After
class Shape {
  getArea() { throw new Error('Not implemented'); }
}

class Circle extends Shape {
  getArea() { return Math.PI * this.radius ** 2; }
}

class Rectangle extends Shape {
  getArea() { return this.width * this.height; }
}

class Triangle extends Shape {
  getArea() { return 0.5 * this.base * this.height; }
}
```

#### Simplify Conditional
**Scenario**: Complex conditionals

```python
# Before
if user.age >= 18 and user.country == 'US' and user.verified == True:
    allow_access()

# After
def is_eligible_user(user):
    return (
        user.age >= 18 and
        user.country == 'US' and
        user.verified
    )

if is_eligible_user(user):
    allow_access()
```

#### Replace Loop with Pipeline
**Scenario**: Imperative loops → Declarative

```javascript
// Before
const adults = [];
for (let i = 0; i < users.length; i++) {
  if (users[i].age >= 18) {
    adults.push(users[i].name);
  }
}

// After
const adults = users
  .filter(user => user.age >= 18)
  .map(user => user.name);
```

### 3. Performance Improvements

#### Avoid N+1 Queries
```python
# Before
users = User.all()
for user in users:
    user.posts  # N+1 query

# After
users = User.includes(:posts).all()
```

#### Use Caching
```javascript
// Before
function getExpensiveData(id) {
  return database.query(`SELECT * FROM large_table WHERE id = ${id}`);
}

// After
const cache = new Map();

function getExpensiveData(id) {
  if (cache.has(id)) {
    return cache.get(id);
  }

  const data = database.query(`SELECT * FROM large_table WHERE id = ${id}`);
  cache.set(id, data);
  return data;
}
```

#### Parallel Processing
```javascript
// Before
const result1 = await fetchData1();
const result2 = await fetchData2();
const result3 = await fetchData3();

// After
const [result1, result2, result3] = await Promise.all([
  fetchData1(),
  fetchData2(),
  fetchData3()
]);
```

---

## 📤 Output Format

### Refactoring Report

```markdown
# Refactoring Report: src/auth/login.js

## Summary
- **Issues Found**: 5
- **Auto-fixable**: 2
- **Complexity Reduction**: 15 → 8
- **Estimated Time**: 30 minutes

---

## Suggestions

### 1. Extract Function: Separate Validation Logic
**Severity**: 🟡 Medium
**Lines**: 45-65
**Complexity**: 12 → 6

**Current Code**:
```javascript
function handleLogin(credentials) {
  // 20 lines of validation
  if (!credentials.email) throw new Error('Email required');
  if (!credentials.password) throw new Error('Password required');
  if (credentials.password.length < 8) throw new Error('Password too short');
  // ... more validation

  // 15 lines of login logic
  const user = await findUser(credentials.email);
  // ...
}
```

**Suggested**:
```javascript
function handleLogin(credentials) {
  validateCredentials(credentials);
  return performLogin(credentials);
}

function validateCredentials(credentials) {
  if (!credentials.email) throw new Error('Email required');
  if (!credentials.password) throw new Error('Password required');
  if (credentials.password.length < 8) throw new Error('Password too short');
}

function performLogin(credentials) {
  const user = await findUser(credentials.email);
  // ...
}
```

**Benefits**:
- Complexity: 12 → 6
- Readability: +++
- Testability: +++

**Auto-fix**: ❌ Manual refactoring needed

---

### 2. Replace Magic Number
**Severity**: 🟢 Low
**Line**: 23

**Current**:
```javascript
if (user.loginAttempts > 5) {
  lockAccount(user);
}
```

**Suggested**:
```javascript
const MAX_LOGIN_ATTEMPTS = 5;

if (user.loginAttempts > MAX_LOGIN_ATTEMPTS) {
  lockAccount(user);
}
```

**Auto-fix**: ✅ Available

---

### 3. Use Parallel Processing
**Severity**: 🟡 Medium
**Lines**: 78-80

**Current**:
```javascript
const user = await fetchUser(id);
const permissions = await fetchPermissions(id);
const settings = await fetchSettings(id);
```

**Suggested**:
```javascript
const [user, permissions, settings] = await Promise.all([
  fetchUser(id),
  fetchPermissions(id),
  fetchSettings(id)
]);
```

**Benefits**:
- Performance: 3x faster (serial → parallel)

**Auto-fix**: ✅ Available

---

## Auto-fix Available (2)

Run: `bash scripts/run-skill.sh refactor-code --file src/auth/login.js --auto-fix`

Fixes:
1. Replace magic number (line 23)
2. Use parallel processing (lines 78-80)
```

---

## 🔧 Auto-Fix Feature

### Fixable Patterns

1. **Magic Numbers → Constants**
2. **Serial → Parallel Async**
3. **Import sorting**
4. **Remove unnecessary else**
5. **var → const/let**

### Running Auto-fix

```bash
# Apply auto-fixes
bash scripts/run-skill.sh refactor-code --file src/auth/login.js --auto-fix

# Dry-run
bash scripts/run-skill.sh refactor-code --file src/auth/login.js --auto-fix --dry-run
```

---

## 🧠 Memory Utilization

### refactor-patterns.json

```json
{
  "project": "my-project",
  "applied_patterns": [
    {
      "pattern": "extract_function",
      "file": "src/auth/login.js",
      "before_complexity": 12,
      "after_complexity": 6,
      "timestamp": "2026-03-19T10:00:00Z",
      "success": true
    }
  ],
  "common_smells": [
    {
      "smell": "long_method",
      "frequency": 15,
      "avg_length": 75
    }
  ],
  "metrics": {
    "avg_complexity_before": 10.5,
    "avg_complexity_after": 7.2,
    "improvement": "31%"
  }
}
```

---

## ⚠️ Gotchas

### 1. Maintain Test Coverage

**Validation**:
```python
# Coverage before refactoring
before_coverage = run_tests()

# Apply refactoring
apply_refactoring()

# Coverage after refactoring
after_coverage = run_tests()

if after_coverage < before_coverage:
    rollback_refactoring()
    raise Error("Refactoring decreased coverage")
```

### 2. Prevent Breaking Changes

**Validation**:
```python
# Prevent public API signature changes
if is_public_api(function) and signature_changed(function):
    raise Error("Cannot change public API signature")
```

### 3. Avoid Over-Abstraction

**Rules**:
- Don't extract if function/class is used only in one place
- Extract only when duplicated 3+ times ("Rule of Three")

---

## 📊 Expected Benefits

### Before (Manual Refactoring)

```
Detect code smell → Manual analysis → Manual fix
    ↓
- Time-consuming (hours)
- Inconsistent
- Many missed patterns
```

### After (Automated Refactoring)

```
Write code → refactor-code skill
         ↓
       Suggestions (1-2 min)
         ↓
       Auto-fix or manual application
```

### Target Metrics

| Metric | Target |
|------|------|
| **Complexity Reduction** | **-30%** |
| **Refactoring Time** | **-70%** |
| **Code Smell Detection** | **90%+** |
| **Maintainability** | **+50%** |

---

## 🔗 Integration

### Integration with Coding Agent

```python
# auto_pipeline.py

# After Coding Agent completes
result_coding = self.run_agent("coding", coding_prompt, ticket_num)

# Run Refactor Skill (optional)
refactor_result = self.run_skill("refactor-code", {
    "files": result_coding["changed_files"]
})

if refactor_result["suggestions"]:
    print(f"💡 {len(refactor_result['suggestions'])} refactoring suggestions")

    if refactor_result["auto_fixable"]:
        # Apply auto-fixes
        self.run_skill("refactor-code", auto_fix=True)
```

---

**Related Documents**:
- [refactor-code.py](refactor-code.py) - Actual implementation
- [refactor-patterns.json](../../.memory/refactor-patterns.json) - Pattern data
