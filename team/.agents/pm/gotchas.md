# PM Agent Gotchas

> **Purpose**: Records repeated failure patterns of PM Agent to prevent the same mistakes.
>
> **Updates**: Add immediately when new failure patterns are discovered.
>
> **Thariq's Advice**: "The highest-signal content in any skill is the Gotchas section"

---

## 1. Scope Creep

### Symptoms
Including features in specifications that are not mentioned in the ticket

### Actual Failure Case
- **Ticket**: "Implement user login/logout"
- **PM-generated spec**: Login, logout + **OAuth integration** + **Password reset** + **Email verification**
- **Problem**: 3x scope expansion → Coding Agent writes unnecessary code → API call waste

### Root Cause
1. Seeing the word "auth" and interpreting it as "complete authentication system"
2. Applying industry best practices without checking Acceptance Criteria
3. Adding features based on assumption "users would want this"

### Detection Method
```
1. Self-check after generating spec:
   - Cross-reference each feature in spec with ticket Acceptance Criteria
   - Are there any items not mentioned in the ticket?

2. Keyword check:
   - "Also", "Additionally", "Furthermore" → scope creep indicators
   - "Generally", "Usually" → assumption-based decision indicators
```

### Correct Approach
1. ✅ **Ticket Acceptance Criteria is the truth**
2. ✅ Only explicitly mentioned items are In Scope
3. ✅ **Explicitly record excluded features in Out of Scope section**
   ```markdown
   ## Out of Scope
   - OAuth integration (not mentioned in ticket)
   - Password reset (not mentioned in ticket)
   - Email verification (not mentioned in ticket)
   ```
4. ✅ If you think it's really necessary, write rationale in log, **never include in spec**

### Related Automation Mode Rules
```
"Should we also add A-1, A-2 features?" → NO (prevent scope creep)
```

---

## 2. Wrong Project Directory

### Symptoms
Creating spec files in `team/.agents/pm/` or `team/.rules/`

### Actual Failure Case
- **Intended**: Create `projects/my-todo-app/planning/specs/backend/PLAN-001-auth.md`
- **Actual**: Created `team/.agents/pm/specs/backend/PLAN-001-auth.md`
- **Problem**: Separated from project code, missed in Git commit, other agents can't find file

### Root Cause
1. Skipping `.project-config.json` read
2. Confused about relative paths (mistakenly thinking current location is `team/` directory)
3. Accidentally creating in same location while referencing template path

### Detection Method
```bash
# Self-check before creation
echo $FILE_PATH | grep -E "team/\.agents|team/\.rules"

# Valid path patterns:
✅ projects/{current_project}/planning/specs/...
✅ projects/my-todo-app/planning/specs/backend/PLAN-001-auth.md

# Invalid path patterns:
❌ team/.agents/pm/specs/...
❌ team/.rules/...
❌ .agents/...
```

### Correct Approach
```markdown
## Step 0 (Never skip)
1. Read .project-config.json
2. Extract current_project
3. Prefix all paths with projects/{current_project}/

Example:
current_project = "my-todo-app"
→ projects/my-todo-app/planning/specs/backend/PLAN-001-auth.md
```

### Self-Check Questions
```
Q: Does the file path I'm about to create start with projects/?
   → If NO, stop immediately, re-read .project-config.json

Q: Does the path contain .agents/ or .rules/?
   → If YES, it's 100% wrong path
```

---

## 3. Ignoring Project Type

### Symptoms
Generating CLI Tool spec for a Web-Fullstack project

### Actual Failure Case
- **Project Type**: `web-fullstack` (FastAPI + Next.js)
- **PM-generated file**: `PLAN-001-command-spec.md` (CLI spec)
- **Problem**: Coding Agent attempts to implement CLI commands instead of web server

### Root Cause
1. Not reading `.project-meta.json`
2. Inferring project type from ticket content only
3. Reusing template from previous project

### Detection Method
```bash
# Mandatory check in Step 0
cat projects/{current_project}/.project-meta.json
# → Check project_type

# Type-to-file mapping:
web-fullstack → specs/backend/, specs/frontend/
cli-tool      → specs/PLAN-XXX-command-spec.md
desktop-app   → specs/screens/, specs/state/, specs/ipc/
```

### Correct Approach
```markdown
1. Read .project-meta.json → Extract project_type
2. Select deliverable template matching project_type
3. Comply with directory structure for that type
```

---

## 4. External Libraries in HTML Wireframes

### Symptoms
Using Tailwind, React, Vue in wireframe HTML

### Actual Failure Case
```html
<!-- ❌ Wrong example -->
<script src="https://cdn.tailwindcss.com"></script>
<div class="flex justify-center items-center bg-blue-500">
  ...
</div>
```

### Root Cause
1. Mistaking this for writing production code
2. Over-eagerness to show "clean design"
3. Invading Coding Agent's role

### Detection Method
```bash
# Self-check after generation
grep -E "tailwind|react|vue|bootstrap|cdn|import.*from" wireframe.html

# If found, remove immediately
```

### Correct Approach
```html
<!-- ✅ Correct example -->
<!DOCTYPE html>
<html lang="en">
<body>
  <!-- State 1: Login form -->
  <div id="state-login">
    <h1>Login</h1>
    <input id="email" type="email" placeholder="Email" />
    <input id="password" type="password" placeholder="Password" />
    <div id="error-message" style="display:none">
      Email or password is incorrect.
    </div>
    <button onclick="handleLogin()">Login</button>
  </div>

  <!-- State 2: Login success -->
  <div id="state-main" style="display:none">
    <h1>Main Page</h1>
  </div>

  <script>
    // Vanilla JS only
    function handleLogin() {
      const email = document.getElementById('email').value;
      if (email && document.getElementById('password').value) {
        document.getElementById('state-login').style.display = 'none';
        document.getElementById('state-main').style.display = 'block';
      } else {
        document.getElementById('error-message').style.display = 'block';
      }
    }
  </script>
</body>
</html>
```

### Core Principles
- **Structure only, no styling** (minimize inline styles)
- **Vanilla JS only** (no external libraries)
- **Separate each state with divs** (`id="state-{name}"`)
- **Simulate API calls** (no actual fetch)

---

## 5. Missing Actual API Call Simulation

### Symptoms
Actual API call code like `fetch()`, `axios` in wireframes

### Actual Failure Case
```javascript
// ❌ Wrong example
async function handleLogin() {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();
  // ...
}
```

### Root Cause
1. Mistaking wireframe for "prototype"
2. Writing code that Coding Agent should implement

### Correct Approach
```javascript
// ✅ Correct example
function handleLogin() {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  // Simulate success scenario (no actual API call)
  if (email && password) {
    // Success → transition to next state
    document.getElementById('state-login').style.display = 'none';
    document.getElementById('state-main').style.display = 'block';
    return;
  }

  // Failure scenario
  document.getElementById('error-message').style.display = 'block';
}
```

---

## 6. Creating Files Without User Approval

### Symptoms
Starting file creation without showing deliverable list

### Root Cause
1. Mistaking "automation mode" for "skip approval mode"
2. Skipping process steps for faster processing

### Correct Approach
```markdown
## Step 2: Present Deliverable List and Get Approval (Never skip)

Files to be created:
- projects/my-todo-app/planning/specs/backend/PLAN-001-user-auth.md
- projects/my-todo-app/planning/specs/frontend/PLAN-001-user-auth.md
- projects/my-todo-app/planning/specs/frontend/PLAN-001-user-auth.html
- projects/my-todo-app/planning/specs/test-cases/PLAN-001-backend.md
- projects/my-todo-app/planning/specs/test-cases/PLAN-001-frontend.md

Main APIs: POST /auth/login, POST /auth/logout
Main Screens: Login form, Main page

Continue? (yes/no)
```

### No Exceptions in Automation Mode
This step **must** be performed even in automation mode (`auto-pipeline.py`).
However, it's automatically processed as "yes" by auto-response rules.

---

## 7. Skipping Log Writing

### Symptoms
Not writing log file after task completion

### Problems
- Decision rationale disappears
- Cannot learn for next project
- Reviewers can't understand "why it was made this way"

### Correct Approach
```markdown
## Step 4: Write Log (Mandatory, immediately after completion)

File location: projects/{current_project}/logs/pm/{YYYYMMDD-HHmmss}-{ticket_number}-{feature_name}.md

Must include:
- List of all created files
- Request interpretation (how ambiguous parts were decided)
- Decisions by project type (which deliverables were created/omitted, why)
- HTML type decision (reason for choosing static/interaction)
- Reviewer notes (arbitrarily decided content due to ambiguity)
```

---

## 8. Missing Error Responses in API Spec

### Symptoms
Documenting only 200 OK, not recording 4xx/5xx error responses

### Actual Failure Case
```markdown
### POST /auth/login
**Response 200**
| Field | Type | Description |
|------|------|------|
| accessToken | string | JWT token |

<!-- ❌ No 401, 400 responses -->
```

### Root Cause
1. Focusing only on "success cases"
2. Mistakenly thinking error handling is Coding Agent's job

### Correct Approach
```markdown
### POST /auth/login

**Response 200**
| Field | Type | Description |
|------|------|------|
| success | boolean | true |
| data.accessToken | string | JWT access token |
| data.user.id | number | User ID |

**Response 401**
| Field | Type | Description |
|------|------|------|
| success | boolean | false |
| error.code | string | INVALID_CREDENTIALS |
| error.message | string | Email or password is incorrect. |

**Response 400**
| Field | Type | Description |
|------|------|------|
| success | boolean | false |
| error.code | string | VALIDATION_ERROR |
| error.message | string | Email format is invalid. |
```

### Required Error Responses
- **400**: Request parameter errors (format, type, missing required fields)
- **401**: Authentication failure
- **403**: No permission
- **404**: Resource not found
- **409**: Conflict (email duplication, etc.)
- **500**: Server error

---

## 9. Missing Accessibility in Test Cases

### Symptoms
No accessibility items in frontend test cases

### Root Cause
1. Mistaking testing = only checking feature operation
2. Thinking accessibility is "optional"

### Correct Approach
```markdown
### Accessibility
| ID | Scenario | Expected Result |
|----|---------|----------|
| TC-FE-005 | Keyboard navigation | All input elements accessible via Tab |
| TC-FE-006 | Error message screen reader | Error message read with role=alert |
| TC-FE-007 | Focus indication | Focus outline on all interactive elements |
```

### When to Add?
- **Web Fullstack/MVC**: Always include
- **Desktop App**: Always include
- **CLI Tool**: Not necessary
- **Library**: Decide per API

---

## 10. Invading Coding Agent's Role

### Symptoms
Including implementation details in spec (which library to use, file structure, etc.)

### Actual Failure Case
```markdown
<!-- ❌ Wrong example -->
## Implementation Method
- Use bcrypt library (salt rounds=12)
- Generate JWT tokens with jose package
- File location: src/backend/api/auth.py

## Database
- Add password_hash column to users table
- password_hash is VARCHAR(255)
```

### Root Cause
1. Mistaking "more detailed is better"
2. Not knowing what Coding Agent should decide

### PM Agent vs Coding Agent Role Separation
```
PM Agent (What to):
- What API endpoints are needed?
- What input/output fields are needed?
- What error responses are needed?
- What screens are needed?

Coding Agent (How to):
- Which library to use?
- How to structure files?
- Which design pattern to apply?
- How to design database schema?
```

### Correct Approach
```markdown
<!-- ✅ Correct example -->
### POST /auth/login
- **Description**: Login with email/password
- **Input**: email, password
- **Output**: accessToken, user info
- **Security**: Hash and store passwords (refer to coding rules for specific algorithm)
- **Errors**: Email format error, password mismatch, account not found

<!-- Never include implementation details like "use bcrypt", "file location", "VARCHAR(255)" -->
```

---

## 📊 Gotcha Effectiveness Measurement

Track how often each Gotcha is triggered to measure effectiveness.

```json
{
  "gotcha_001_scope_creep": {
    "prevented_count": 12,
    "last_triggered": "2026-03-15",
    "effectiveness": "high"
  },
  "gotcha_002_wrong_directory": {
    "prevented_count": 8,
    "last_triggered": "2026-03-14",
    "effectiveness": "high"
  }
}
```

---

## 🔄 Update History

- **2026-03-19**: Initial version created (10 Gotchas)
- New failure patterns will be added immediately upon discovery

---

**Next Reading**: [workflows/web-fullstack.md](workflows/web-fullstack.md)
