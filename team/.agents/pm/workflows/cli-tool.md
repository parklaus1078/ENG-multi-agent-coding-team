# CLI Tool Workflow

> **Project Type**: cli-tool (e.g., Go Cobra, Python Click, Rust Clap)
>
> **Applicable When**: `project_type` in `.project-meta.json` is `"cli-tool"`

---

## 📂 Deliverable Structure

```
projects/{current_project}/planning/specs/
├── PLAN-{number}-command-spec.md        # Command spec
└── test-cases/
    └── PLAN-{number}-command.md          # Command test cases
```

---

## 🔨 Work Process

### Step 1: Ticket Analysis

Extract the following from ticket:
- [ ] Command name (e.g., `mycli init`, `mycli search`)
- [ ] Flags/Options (e.g., `--name`, `--verbose`)
- [ ] Arguments (e.g., `<filename>`, `<path>`)
- [ ] Output format (stdout, stderr, exit code)
- [ ] Error cases

**⚠️ Gotcha Check**:
- CLI Tool has no UI → wireframe unnecessary
- Output is text/JSON only → prohibit HTML generation

---

### Step 2: Present Deliverable List

Show users the list of files to be created and get approval.

**Template**:
```
Project: {current_project} (cli-tool)
Ticket: PLAN-{number}-{slug}

Files to be created:
- projects/{current_project}/planning/specs/PLAN-{number}-command-spec.md
- projects/{current_project}/planning/specs/test-cases/PLAN-{number}-command.md

Main command: mycli init
Flags: --name, --template
Output: Project initialization completion message

Continue? (yes/no)
```

---

### Step 3-1: Generate Command Spec

**File**: `specs/PLAN-{number}-command-spec.md`

**Template Structure**:
```markdown
# {Command Name} Spec

## Command
`mycli {command} [subcommand]`

## Description
{What the command does in 2-3 lines}

## Flags
| Flag | Short | Type | Required | Default | Description |
|-------|------|------|------|--------|------|
| --name | -n | string | Y | - | Project name |
| --template | -t | string | N | default | Template type (default, minimal, full) |
| --verbose | -v | boolean | N | false | Output detailed logs |

## Arguments
| Argument | Type | Required | Description |
|------|------|------|------|
| path | string | N | Path to initialize (default: current directory) |

## Output Examples

### On Success
\`\`\`
✅ Project 'my-app' has been initialized.
Created files:
- my-app/config.yaml
- my-app/README.md
- my-app/src/main.go
\`\`\`

### On Failure
\`\`\`
❌ Error: Directory 'my-app' already exists.
   Use --force flag to overwrite.
\`\`\`

## Error Cases
| Situation | Error Code | Message | Standard Stream |
|------|----------|--------|-----------|
| Directory already exists | 1 | Directory already exists. | stderr |
| Invalid template | 2 | Invalid template. | stderr |
| No permission | 3 | No permission to create directory. | stderr |
| Network error (template download) | 4 | Cannot download template. | stderr |

## Exit Codes
| Code | Meaning |
|------|------|
| 0 | Success |
| 1 | File/directory error |
| 2 | Validation failure |
| 3 | Permission error |
| 4 | Network error |

## Environment Variables (Optional)
| Variable Name | Description | Default |
|--------|------|--------|
| MYCLI_TEMPLATE_REPO | Template repository URL | https://github.com/... |
| MYCLI_CONFIG_HOME | Config file path | ~/.mycli |

## Examples

### Basic Usage
\`\`\`bash
mycli init --name my-project
\`\`\`

### Specify Template
\`\`\`bash
mycli init --name my-project --template minimal
\`\`\`

### Create in Specific Path
\`\`\`bash
mycli init --name my-project /path/to/workspace
\`\`\`

### Detailed Logs
\`\`\`bash
mycli init --name my-project --verbose
\`\`\`
```

**⚠️ Gotcha Check**:
- [ ] **Gotcha #10**: Exclude implementation details (which library to use)
- [ ] Specify exit code for all error cases
- [ ] Clearly distinguish stdout vs stderr

---

### Step 3-2: Generate Test Cases

**File**: `specs/test-cases/PLAN-{number}-command.md`

**Template Structure**:
```markdown
# {Command Name} Test Cases

## Normal Cases

| ID | Scenario | Command | Expected Output | Exit Code |
|----|---------|--------|----------|-----------|
| TC-CLI-001 | Basic initialization | `mycli init --name my-app` | "Project 'my-app' initialized" | 0 |
| TC-CLI-002 | Specify template | `mycli init --name my-app --template minimal` | minimal template used message | 0 |
| TC-CLI-003 | Detailed logs | `mycli init --name my-app --verbose` | Step-by-step log output | 0 |
| TC-CLI-004 | Specific path | `mycli init --name my-app /tmp/test` | /tmp/test/my-app created | 0 |

## Exception Cases

| ID | Scenario | Command | Expected Output | Exit Code |
|----|---------|--------|----------|-----------|
| TC-CLI-101 | Directory already exists | `mycli init --name existing` | "Directory already exists" | 1 |
| TC-CLI-102 | Invalid template | `mycli init --name my-app --template invalid` | "Invalid template" | 2 |
| TC-CLI-103 | Missing required flag | `mycli init` | "--name flag is required" | 2 |
| TC-CLI-104 | Path without permission | `mycli init --name my-app /root/forbidden` | "No permission" | 3 |

## Flag Combination Tests

| ID | Scenario | Command | Expected Result |
|----|---------|--------|----------|
| TC-CLI-201 | Short flags | `mycli init -n my-app -t minimal` | Normal operation |
| TC-CLI-202 | Flag order independent | `mycli init --template minimal --name my-app` | Normal operation |

## Output Format Tests

| ID | Scenario | Check Item |
|----|---------|----------|
| TC-CLI-301 | Success message stdout | Message starting with "✅" on stdout |
| TC-CLI-302 | Error message stderr | Message starting with "❌" on stderr |
| TC-CLI-303 | File list output | Created file list displayed on stdout |

## Interactive Tests (If Applicable)

| ID | Scenario | Input | Expected Action |
|----|---------|------|----------|
| TC-CLI-401 | Interactive prompt | `mycli init` (without flags) | Request project name input |
| TC-CLI-402 | Ctrl+C interrupt | Ctrl+C during execution | Immediate exit, clean up partial files |

## Performance Tests (Optional)

| ID | Scenario | Condition | Expected Result |
|----|---------|------|----------|
| TC-CLI-501 | Large template | 1000 file template | Complete within 30 seconds |
| TC-CLI-502 | Network delay | Slow network | Display timeout message |
```

---

## 📝 Write Log

**File**: `projects/{current_project}/logs/pm/{YYYYMMDD-HHmmss}-PLAN-{number}-{command_name}.md`

**Must Include**:
```markdown
# PM Log: {Command Name}

- **Agent**: PM Agent
- **Project**: {current_project}
- **Project Type**: cli-tool
- **Ticket Number**: PLAN-{number}
- **Timestamp**: {YYYY-MM-DD HH:mm:ss}
- **Created Files**:
  - specs/PLAN-{number}-command-spec.md
  - specs/test-cases/PLAN-{number}-command.md

---

## Request Interpretation
{How the ticket was interpreted}

## Applied Gotchas
- ✅ Gotcha #1: Prevent scope creep - [specific details]
- ✅ Gotcha #2: Correct directory - projects/{current_project}/planning/specs/
- ✅ Gotcha #10: Exclude implementation details - define command behavior only

## CLI Special Considerations
- Clearly distinguish stdout/stderr
- Exit code definitions
- Environment variables (if needed)
- Interactive mode (if needed)

## Reviewer Notes
{Arbitrarily decided content due to ambiguity}
```

---

## ✅ Completion Checklist

- [ ] Command spec generation complete
- [ ] All flags/arguments documented
- [ ] Output examples included (success/failure)
- [ ] Exit code defined for each error case
- [ ] stdout/stderr distinction clear
- [ ] Test cases generation complete
- [ ] Log file creation complete
- [ ] "✅ PM Agent task complete" message output

---

## 🔍 CLI Tool Special Checks

### Flag Naming Rules
- Long flags: `--kebab-case` (e.g., `--project-name`)
- Short flags: `-x` single letter (e.g., `-n`)
- Boolean flags: `--verbose` (no value)
- Value-taking flags: `--name <value>` or `--name=<value>`

### Output Format
- Success: Start with `✅`, stdout output
- Error: Start with `❌`, stderr output
- Warning: Start with `⚠️`, stderr output
- Info: Start with `ℹ️`, stdout output

### Exit Code Convention
- `0`: Success
- `1`: General error
- `2`: Validation failure
- `3-9`: Project-specific definitions
- `126`: No execute permission
- `127`: Command not found
- `130`: Interrupted by Ctrl+C

---

**Related Documents**:
- [gotchas.md](../gotchas.md) - Failure patterns
- [CLAUDE.md](../CLAUDE.md) - Main agent definition
