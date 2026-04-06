# Docs Generator Skill

> **Purpose**: Automatic documentation generation from code
>
> **Type**: Documentation Skill
>
> **Thariq Lesson**: "Keep documentation in sync with code"

---

## 🎯 Triggers

### Auto Triggers
- Auto-pipeline: After Coding Agent completion (optional)
- Git hook: pre-commit (on API changes)
- CI/CD: Documentation update on PR

### Manual Triggers
```bash
# Generate all documentation
bash scripts/run-skill.sh docs-generator --all

# API documentation only
bash scripts/run-skill.sh docs-generator --api

# Update README
bash scripts/run-skill.sh docs-generator --readme

# Specific module
bash scripts/run-skill.sh docs-generator --module auth
```

---

## 🔍 Features

### 1. API Documentation Auto-Generation

**Supported Formats**:
- **OpenAPI/Swagger**: REST API
- **GraphQL Schema**: GraphQL API
- **JSDoc/TSDoc**: JavaScript/TypeScript
- **Sphinx/reStructuredText**: Python
- **GoDoc**: Go
- **RustDoc**: Rust

**Example (OpenAPI)**:
```python
def generate_openapi_spec(routes):
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "My API",
            "version": "1.0.0"
        },
        "paths": {}
    }

    for route in routes:
        spec["paths"][route.path] = {
            route.method.lower(): {
                "summary": route.summary,
                "parameters": route.parameters,
                "responses": route.responses
            }
        }

    return spec
```

**Extract from Code**:
```python
# Source code
@app.post("/api/login")
async def login(email: str, password: str):
    """
    User login

    Args:
        email: User email
        password: Password

    Returns:
        {"token": "jwt_token", "user": {...}}

    Raises:
        401: Invalid credentials
    """
    pass

# Auto-generated documentation
"""
POST /api/login

User login

Parameters:
  - email (string, required): User email
  - password (string, required): Password

Responses:
  - 200: {"token": "jwt_token", "user": {...}}
  - 401: Invalid credentials
"""
```

### 2. README Auto-Update

**Auto-Generated Sections**:
```markdown
# My Project

> Auto-generated from code and git history

## Features

- ✅ User authentication (JWT)
- ✅ Profile management
- ✅ Search functionality
- 🚧 Payment integration (in progress)

## Installation

```bash
npm install
```

## API Endpoints

### Authentication

- `POST /api/login` - User login
- `POST /api/logout` - Logout
- `POST /api/register` - Register

### User

- `GET /api/user/me` - Current user info
- `PUT /api/user/me` - Update profile

## Environment Variables

- `DATABASE_URL` - Database connection URL (required)
- `JWT_SECRET` - JWT signing secret (required)
- `API_KEY` - External API key (optional)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT
```

**Auto Detection**:
```python
def update_readme():
    # 1. Extract features
    features = extract_features_from_code()

    # 2. Extract API endpoints
    endpoints = extract_endpoints()

    # 3. Extract environment variables
    env_vars = extract_env_vars_from_code()

    # 4. Update README
    update_readme_sections({
        "Features": features,
        "API Endpoints": endpoints,
        "Environment Variables": env_vars
    })
```

### 3. Changelog Auto-Generation

**Generated from Git Commits**:
```markdown
# Changelog

## [1.3.0] - 2026-03-19

### Added
- feat(PLAN-001): implement JWT authentication
- feat(PLAN-003): add user profile API

### Fixed
- fix(PLAN-002): resolve login validation error
- fix(PLAN-005): fix memory leak in session storage

### Changed
- refactor(PLAN-004): optimize database queries

## [1.2.0] - 2026-03-12

### Added
- feat: add search functionality
```

**Generation Logic**:
```python
def generate_changelog(from_version, to_version):
    # 1. Get commit log
    commits = git_log(f"{from_version}..{to_version}")

    # 2. Group by commit type
    changelog = {
        "Added": [],
        "Fixed": [],
        "Changed": [],
        "Removed": []
    }

    for commit in commits:
        if commit.message.startswith("feat"):
            changelog["Added"].append(commit.message)
        elif commit.message.startswith("fix"):
            changelog["Fixed"].append(commit.message)
        elif commit.message.startswith("refactor"):
            changelog["Changed"].append(commit.message)

    return format_changelog(changelog, to_version)
```

### 4. Code Comment Validation

**Detect Missing Comments**:
```python
def validate_docstrings(files):
    issues = []

    for file in files:
        functions = extract_functions(file)

        for func in functions:
            # Public functions require docstrings
            if func.is_public and not func.has_docstring:
                issues.append({
                    "file": file,
                    "function": func.name,
                    "line": func.line,
                    "severity": "warning",
                    "message": "Missing docstring for public function"
                })

            # Complex functions should have docstrings
            if func.complexity > 10 and not func.has_docstring:
                issues.append({
                    "file": file,
                    "function": func.name,
                    "line": func.line,
                    "severity": "info",
                    "message": "Docstring recommended for complex function"
                })

    return issues
```

### 5. Example Code Auto-Generation

**API Usage Examples**:
```python
# API definition
@app.post("/api/login")
async def login(email: str, password: str):
    pass

# Auto-generated examples
"""
### Example: User Login

```python
import requests

response = requests.post(
    "https://api.example.com/api/login",
    json={
        "email": "user@example.com",
        "password": "password123"
    }
)

if response.status_code == 200:
    token = response.json()["token"]
    print(f"Login successful: {token}")
else:
    print(f"Login failed: {response.text}")
```

```javascript
fetch('https://api.example.com/api/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
})
  .then(res => res.json())
  .then(data => console.log('Token:', data.token))
  .catch(err => console.error('Error:', err));
```

```bash
curl -X POST https://api.example.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```
"""
```

---

## 📤 Output Format

### Documentation Generation Report

```markdown
# Documentation Report

## Summary
- **Files Processed**: 45
- **API Endpoints**: 28
- **Docstrings Added**: 12
- **README Updated**: Yes
- **Changelog Generated**: Yes

---

## Generated Files

✅ `docs/api/openapi.yaml` - OpenAPI 3.0 spec (28 endpoints)
✅ `docs/api/README.md` - API documentation
✅ `README.md` - Updated Features, API, Environment Variables
✅ `CHANGELOG.md` - v1.2.0 → v1.3.0
✅ `docs/examples/` - 14 code examples

---

## API Documentation

### Endpoints by Module

| Module | Endpoints | Documented |
|--------|-----------|------------|
| auth | 5 | ✅ 5/5 |
| user | 8 | ✅ 8/8 |
| search | 3 | ✅ 3/3 |
| admin | 12 | ⚠️ 10/12 |

---

## Missing Documentation

### 1. admin.delete_user (admin/user.py:45)
**Severity**: Warning
**Reason**: Missing docstring for public function

**Suggestion**:
```python
def delete_user(user_id: int):
    """
    Delete user

    Args:
        user_id: User ID to delete

    Returns:
        True if successful

    Raises:
        ValueError: User not found
    """
    pass
```

---

### 2. search.advanced_search (search/engine.py:120)
**Severity**: Info
**Reason**: Complex function (complexity: 15)

---

## README Changes

### Features Section
+ ✅ User authentication (JWT)
+ ✅ Profile management
+ ✅ Search functionality

### API Endpoints Section
+ POST /api/login - User login
+ GET /api/user/me - Current user info
+ ... (28 endpoints total)

### Environment Variables Section
+ DATABASE_URL (required)
+ JWT_SECRET (required)
+ API_KEY (optional)

---

## Changelog (v1.3.0)

### Added (3)
- feat(PLAN-001): implement JWT authentication
- feat(PLAN-003): add user profile API
- feat(PLAN-007): add search functionality

### Fixed (2)
- fix(PLAN-002): resolve login validation error
- fix(PLAN-005): fix memory leak

---

## Next Steps

1. ⚠️ Add docstrings to 2 functions
2. ✅ Review generated API docs
3. ✅ Publish to documentation site
```

---

## 🧠 Memory Usage

### docs-history.json

```json
{
  "version": "0.0.1",
  "project": "multi-agent-coding-team",

  "documentation_coverage": {
    "api_endpoints": {
      "total": 28,
      "documented": 28,
      "coverage": 1.0
    },
    "public_functions": {
      "total": 150,
      "documented": 138,
      "coverage": 0.92
    }
  },

  "generated_files": [
    {
      "file": "docs/api/openapi.yaml",
      "timestamp": "2026-03-19T14:00:00Z",
      "endpoints": 28
    },
    {
      "file": "CHANGELOG.md",
      "timestamp": "2026-03-19T14:00:00Z",
      "version": "1.3.0"
    }
  ],

  "missing_docs_trend": [
    {"date": "2026-03-01", "count": 25},
    {"date": "2026-03-15", "count": 8},
    {"date": "2026-03-19", "count": 2}
  ],

  "common_patterns": [
    {
      "pattern": "API endpoint without examples",
      "frequency": 5
    }
  ]
}
```

---

## ⚠️ Gotchas

### 1. Code and Documentation Sync

**Principle**: Documentation generated from code (Single Source of Truth)

```python
# ❌ Wrong: Manual documentation
# Manually write API description in docs/api.md

# ✅ Correct: Generated from code
@app.post("/api/login")
async def login(email: str, password: str):
    """
    User login

    This docstring is auto-generated into documentation
    """
    pass
```

### 2. Example Code Testing

**Validation**:
```python
# Test that generated example code actually works
def test_generated_examples():
    examples = load_generated_examples()

    for example in examples:
        # Execute example code
        result = execute_code(example.code)

        if not result.success:
            raise Error(f"Example code failed: {example.name}")
```

### 3. Changelog Duplication Prevention

**Validation**:
```python
# Check if version already exists in Changelog
if version_exists_in_changelog(new_version):
    print(f"⚠️ {new_version} already exists in Changelog")
    return
```

### 4. Exclude Sensitive Information

**Validation**:
```python
# Remove sensitive information from example code
sensitive_patterns = [
    r'api_key\s*=\s*["\'][^"\']+["\']',
    r'password\s*=\s*["\'][^"\']+["\']',
    r'sk-[a-zA-Z0-9]+'
]

for pattern in sensitive_patterns:
    if re.search(pattern, example_code):
        # Replace with placeholder
        example_code = re.sub(pattern, 'api_key = "YOUR_API_KEY"', example_code)
```

---

## 📊 Expected Benefits

### Before (Manual Documentation)

```
Write code → Manual documentation (30 min)
          → Modify code
          → Forget to update docs
          → Code and docs out of sync
```

**Problems**:
- ❌ Time consuming
- ❌ Sync issues
- ❌ Missing docs
- ❌ Outdated examples

### After (Auto Documentation)

```
Write code → docs-generator skill (auto)
          → Auto-generate docs (1 min)
          → Auto-generate examples
          → 100% in sync
```

**Improvements**:
- ✅ Instant generation
- ✅ Always in sync
- ✅ No missing docs
- ✅ Up-to-date examples

### Target Metrics

| Metric | Target |
|--------|--------|
| **Documentation Time** | **-90%** |
| **Sync Issues** | **0%** |
| **API Doc Coverage** | **100%** |
| **Example Code Accuracy** | **100%** |

---

## 🔗 Integration

### Auto-pipeline Integration

```python
# auto_pipeline.py

# After Coding Agent completion (detect API changes)
if api_changed(changed_files):
    print("📝 Updating API documentation...")

    docs_result = self.run_skill("docs-generator", {
        "api": True,
        "readme": True,
        "changelog": True
    })

    if docs_result["success"]:
        print(f"✅ Documentation generated:")
        print(f"   - API docs: {docs_result['api_endpoints']} endpoints")
        print(f"   - README updated: {docs_result['readme_updated']}")
        print(f"   - Changelog: {docs_result['changelog_version']}")

        # Commit documentation
        self.run_skill("commit", {
            "ticket": ticket_num,
            "type": "docs"
        })
```

### GitHub Actions Integration

```yaml
# .github/workflows/docs.yml
name: Generate Documentation

on:
  push:
    branches: [main]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Generate docs
        run: |
          bash scripts/run-skill.sh docs-generator --all

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

---

**Related Documentation**:
- [docs-generator.py](docs-generator.py) - Actual implementation
- [docs-history.json](../../.memory/docs-history.json) - Documentation history
- [docs-config.json](docs-config.json) - Documentation configuration
