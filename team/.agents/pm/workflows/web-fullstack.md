# Web-Fullstack Workflow

> **Project Type**: web-fullstack (e.g., FastAPI + Next.js, Express + React, Django + Vue)
>
> **Applied When**: `.project-meta.json` has `project_type` set to `"web-fullstack"`

---

## 📂 Deliverable Structure

```
projects/{current_project}/planning/specs/
├── backend/
│   └── PLAN-{number}-{slug}.md          # API specification
├── frontend/
│   ├── PLAN-{number}-{slug}.md          # UI requirements
│   └── PLAN-{number}-{slug}.html        # Wireframe
└── test-cases/
    ├── PLAN-{number}-backend.md         # Backend test cases
    └── PLAN-{number}-frontend.md        # Frontend test cases
```

---

## 🔨 Workflow Steps

### Step 1: Analyze Ticket

Extract from ticket:
- [ ] Feature name
- [ ] Acceptance Criteria
- [ ] API endpoints (explicit or inferred)
- [ ] UI screens (explicit or inferred)

**⚠️ Gotcha Check**:
- Features **not** in Acceptance Criteria should be classified as Out-of-Scope
- Document rationale for any inferences in logs

---

### Step 2: Present Deliverables List

Show the list of files to be created and get user approval.

**Template**:
```
Project: {current_project} (web-fullstack)
Ticket: PLAN-{number}-{slug}

Files to be created:
- projects/{current_project}/planning/specs/backend/PLAN-{number}-{slug}.md
- projects/{current_project}/planning/specs/frontend/PLAN-{number}-{slug}.md
- projects/{current_project}/planning/specs/frontend/PLAN-{number}-{slug}.html
- projects/{current_project}/planning/specs/test-cases/PLAN-{number}-backend.md
- projects/{current_project}/planning/specs/test-cases/PLAN-{number}-frontend.md

Main APIs: POST /auth/login, POST /auth/logout
Main Screens: Login form, Main page (after successful login)
User Flow: Login success → Enter main / Failure → Show error message

Continue? (yes/no)
```

---

### Step 3-1: Generate API Specification

**File**: `specs/backend/PLAN-{number}-{slug}.md`

**Template Structure**:
```markdown
# {Feature Name} API Specification

## Endpoint List

### POST /auth/login
- **Description**: Login with email/password
- **Auth Required**: No

**Request Body**
| Field | Type | Required | Description |
|------|------|------|------|
| email | string | Y | Email address |
| password | string | Y | Password (min 8 characters) |

**Response 200**
| Field | Type | Description |
|------|------|------|
| success | boolean | Success status |
| data.accessToken | string | JWT access token |
| data.user.id | number | User ID |
| data.user.email | string | User email |

**Response 401**
| Field | Type | Description |
|------|------|------|
| success | boolean | false |
| error.code | string | INVALID_CREDENTIALS |
| error.message | string | Invalid email or password. |

**Response 400**
| Field | Type | Description |
|------|------|------|
| success | boolean | false |
| error.code | string | VALIDATION_ERROR |
| error.message | string | Invalid email format. |
```

**⚠️ Gotcha Check**:
- [ ] **Gotcha #8**: Include error responses (400, 401, 403, 404, 500) for all endpoints
- [ ] **Gotcha #10**: Exclude implementation details (libraries, file locations)
- [ ] **Gotcha #1**: Specify excluded features in Out-of-Scope section

---

### Step 3-2: Generate UI Requirements

**File**: `specs/frontend/PLAN-{number}-{slug}.md`

**Template Structure**:
```markdown
# {Feature Name} UI Requirements

## Screen List
- Login form (default state)
- Login form (error state)
- Main page (after successful login)

## User Flow
1. Enter login form
2. Input email/password and click login button
   - Success: Navigate to main page
   - Failure: Display error message, keep form

## Component Structure

### Login Form
- Email Input
- Password Input
- Login Button (including loading state)
- Error message area (shown on failure)
- Sign up link
- Forgot password link

## Connected APIs
- Login button click → POST /auth/login

## Edge Cases
- Invalid email format → Client-side validation
- Password less than 8 characters → Client-side validation
- During API call → Disable button + show loading indicator
```

---

### Step 3-3: Generate Wireframe

**File**: `specs/frontend/PLAN-{number}-{slug}.html`

**HTML Type Decision**:

| Situation | HTML Type |
|------|----------|
| Simple information display, layout check only | Static HTML |
| Screen transition after form submission | With interaction |
| Different states shown on success/failure | With interaction |
| Overlays like modals, toasts, drawers | With interaction |
| Tab, step, wizard transitions | With interaction |

**HTML Writing Rules**:
- ✅ Structure only, no styling (minimize inline styles)
- ✅ Vanilla JS only (no external libraries)
- ✅ Separate each state with `id="state-{name}"` div
- ✅ Hidden states use `style="display:none"`
- ✅ Simulate API calls (no actual fetch)
- ✅ Document component roles with comments

**⚠️ Gotcha Check**:
- [ ] **Gotcha #4**: No Tailwind, React, Vue, Bootstrap
- [ ] **Gotcha #5**: No fetch(), axios or actual API calls

**Interactive HTML Template**:
```html
<!DOCTYPE html>
<html lang="en">
<body>

  <!-- State 1: Login Form -->
  <div id="state-login">
    <h1>Login</h1>
    <input id="email" type="email" placeholder="Email" />
    <input id="password" type="password" placeholder="Password" />
    <!-- Error message shown on failure -->
    <div id="error-message" style="display:none">
      Invalid email or password.
    </div>
    <button onclick="handleLogin()">Login</button>
    <a href="/signup">Sign Up</a>
  </div>

  <!-- State 2: Main Page After Login Success -->
  <div id="state-main" style="display:none">
    <h1>Main Page</h1>
    <p>Welcome!</p>
  </div>

  <script>
    function handleLogin() {
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      // Success scenario (if email/password entered)
      if (email && password) {
        document.getElementById('state-login').style.display = 'none';
        document.getElementById('state-main').style.display = 'block';
        return;
      }

      // Failure scenario
      document.getElementById('error-message').style.display = 'block';
    }
  </script>

</body>
</html>
```

---

### Step 3-4: Generate Test Cases

#### Backend Test Cases

**File**: `specs/test-cases/PLAN-{number}-backend.md`

```markdown
# {Feature Name} BE Test Cases

## POST /auth/login

### Normal Cases
| ID | Scenario | Input | Expected Result |
|----|---------|------|---------|
| TC-BE-001 | Login with valid email/password | email: test@example.com, password: password123 | 200, return accessToken |

### Exception Cases
| ID | Scenario | Input | Expected Result |
|----|---------|------|---------|
| TC-BE-002 | Non-existent email | email: wrong@example.com | 401, INVALID_CREDENTIALS |
| TC-BE-003 | Password mismatch | password: wrongpass | 401, INVALID_CREDENTIALS |
| TC-BE-004 | Invalid email format | email: notanemail | 400, VALIDATION_ERROR |
| TC-BE-005 | Password less than 8 characters | password: short | 400, VALIDATION_ERROR |
```

#### Frontend Test Cases

**File**: `specs/test-cases/PLAN-{number}-frontend.md`

```markdown
# {Feature Name} FE Test Cases

## Login Form

### Normal Cases
| ID | Scenario | Action | Expected Result |
|----|---------|------|---------|
| TC-FE-001 | Successful login | Input valid email/password and click login | Navigate to main page |

### Exception Cases
| ID | Scenario | Action | Expected Result |
|----|---------|------|---------|
| TC-FE-002 | Login failure | Input wrong password and click login | Display error message, keep form |
| TC-FE-003 | Invalid email format | Input invalid format and click | Show client-side validation error |
| TC-FE-004 | Loading state | Immediately after clicking login button | Disable button, show loading |

### Accessibility
| ID | Scenario | Expected Result |
|----|---------|----------|
| TC-FE-005 | Keyboard navigation | All input elements accessible via Tab |
| TC-FE-006 | Screen reader error messages | Error messages announced with role=alert |
```

**⚠️ Gotcha Check**:
- [ ] **Gotcha #9**: Include accessibility test cases

---

## 📝 Log Writing

**File**: `projects/{current_project}/logs/pm/{YYYYMMDD-HHmmss}-PLAN-{number}-{feature-name}.md`

**Required Content**:
```markdown
# PM Log: {Feature Name}

- **Agent**: PM Agent
- **Project**: {current_project}
- **Project Type**: web-fullstack
- **Ticket Number**: PLAN-{number}
- **Timestamp**: {YYYY-MM-DD HH:mm:ss}
- **Created Files**:
  - specs/backend/PLAN-{number}-{slug}.md
  - specs/frontend/PLAN-{number}-{slug}.md
  - specs/frontend/PLAN-{number}-{slug}.html
  - specs/test-cases/PLAN-{number}-backend.md
  - specs/test-cases/PLAN-{number}-frontend.md

---

## Request Interpretation
{How the ticket was interpreted, how ambiguous parts were judged}

## Applied Gotchas
- ✅ Gotcha #1: Scope creep prevention - [specific details]
- ✅ Gotcha #2: Correct directory - projects/{current_project}/planning/specs/
- ✅ Gotcha #4: No external libraries in HTML - Vanilla JS only
- ✅ Gotcha #8: Document error responses - Include 4xx/5xx for all endpoints
- ✅ Gotcha #9: Accessibility tests - Keyboard navigation, screen reader included

## HTML Type Decision
{Reason for choosing Static HTML / Interactive HTML, list of implemented states}

## Project Type Decisions
- Created: backend API spec, frontend UI spec, wireframe, test cases
- Omitted: None (web-fullstack requires all deliverables)

## Reviewer Notes
{Ambiguous content decided arbitrarily, items requiring additional confirmation}
```

---

## ✅ Completion Checklist

- [ ] Verified against ticket Acceptance Criteria
- [ ] All 5 files created (backend, frontend, html, test-cases x2)
- [ ] All API endpoints include error responses
- [ ] HTML uses no external libraries
- [ ] Accessibility test cases included
- [ ] Out-of-Scope section completed
- [ ] Log file created
- [ ] "✅ PM Agent work complete" message displayed

---

**Related Documents**:
- [gotchas.md](../gotchas.md) - Failure patterns
- [CLAUDE.md](../CLAUDE.md) - Main agent definition
