# Changelog

## [2026-03-09] Context Window Management Improvements

### Added

#### Project Planner Agent
- **New agent**: `project-planner` that breaks down natural language project descriptions into structured tickets
- **3-Phase execution**: Split work into Planning → Ticket Creation → Logging
- **Batch processing**: Create tickets in batches of 5 (or 3 for 16+ tickets)
- **Resume capability**: Resume from interruption point using `--resume` flag
- **Progress tracking**: Save checkpoints to `.plan-*.json` and `.progress-*.json` files

#### Scripts
- Added `--project` flag to `run-agent.sh` for project-planner
- Added `--resume` flag to `run-agent.sh` for resuming interrupted work
- Updated `run-agent.sh` to support ticket number (`--ticket`) instead of just file paths

#### Documentation
- `team/.agents/project-planner/CLAUDE.md` - Main agent instructions (379 lines)
- `team/.agents/project-planner/CONTEXT_WINDOW_STRATEGY.md` - Detailed strategy documentation (154 lines)
- `.gitignore` - Exclude temporary plan and progress files

### Changed

#### README.md
- Updated workflow to include Project Planner as first step
- Added "Method A" (start with project idea) and "Method B" (start with tickets)
- Updated agent list to include `project-planner`
- Updated project structure to show project-planner directory
- Updated example ticket numbers from `PROJ-123` to `PLAN-001`

#### Workflow
```
Old: Jira Ticket → PM Agent → Coding → QA
New: Project Idea → Project Planner → Tickets → PM Agent → Coding → QA
```

### Benefits

✅ **Context window protection**: Large projects can be handled safely
✅ **Resumability**: Work can continue from interruption point
✅ **Transparency**: Progress visible via checkpoint files
✅ **Scalability**: Handles any number of tickets reliably
✅ **Token efficiency**: Selective loading via JSON format

### Usage Examples

**New workflow (Method A):**
```bash
# Step 1: Break down project
bash scripts/run-agent.sh project-planner --project "E-commerce platform with user auth, product catalog, cart, checkout"

# Step 2: Generate specs
bash scripts/run-agent.sh pm --ticket-file ./tickets/PLAN-001-user-auth.md

# Step 3: Implement
bash scripts/run-agent.sh be-coding --ticket PLAN-001
bash scripts/run-agent.sh fe-coding --ticket PLAN-001

# Step 4: Test
bash scripts/run-agent.sh qa-be --ticket PLAN-001
bash scripts/run-agent.sh qa-fe --ticket PLAN-001
```

**Resume from interruption:**
```bash
bash scripts/run-agent.sh project-planner --resume
```

### Technical Details

**Phase 1: Planning**
- Analyze project requirements
- Break down into features
- Set priorities and dependencies
- Get user approval
- Save to `tickets/.plan-{timestamp}.json`

**Phase 2: Ticket Creation**
- Read plan from JSON file
- Create tickets in batches (5 or 3 at a time)
- Save progress to `tickets/.progress-{timestamp}.json` after each batch
- Clean up temporary files after completion

**Phase 3: Logging**
- Write implementation log to `logs/project-planner/{timestamp}.md`

### File Structure

```
team/tickets/
├── PLAN-001-user-auth.md          # Final output
├── PLAN-002-product-crud.md
├── .plan-20260309-103000.json     # Temporary (auto-deleted)
└── .progress-20260309-103000.json # Temporary (auto-deleted)
```

### Migration Notes

- Existing workflows using PM Agent directly are still supported (Method B)
- No breaking changes to existing agents
- Project Planner is optional but recommended for new projects
