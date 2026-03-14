# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v0.0.2.0.html).

---

## [Unreleased]

---

## [0.0.2] - 2026-03-12

### Added
- **Tech Stack Agnostic Architecture**: Support for all development types
  - web-fullstack, web-mvc, cli-tool, desktop-app, mobile-app, library, data-pipeline
- **Project Isolation Structure**: `team/projects/{project-name}/`
  - Each project as independent Git repository
  - Per-project planning and logs directories
  - Multiple projects can be managed simultaneously
- **Stack Initializer Agent**: Auto-initialize environment based on project type and stack
  - Auto-analyze official documentation (WebSearch, WebFetch)
  - Auto-generate coding rules (`.rules/_cache/`)
  - Auto-generate PM/Coding/QA templates
  - Create initial project structure
- **init-project.sh**: Project initialization script
  - Interactive mode support
  - Flag-based mode support
  - Auto-invoke Stack Initializer Agent
- **Unified Agent Structure**: `coding`, `qa` agents (support all types)
- **Dynamic Template System**: `.agents/{agent}/templates/{project_type}.md`
- **Coding Rules Priority System**:
  - `.rules/_verified/`: Human-verified rules (highest priority)
  - `.rules/_cache/`: Auto-generated rules (24-hour cache)
- **Universal Coding Principles**: `.rules/general-coding-rules.md` (DRY, SOLID, security, etc.)
- **Project Metadata**: `.project-meta.json` (per project)
- **Global Project Configuration**: `.project-config.json` (root)
- **Configuration Schema**: `.project-config.schema.json`
- **Git Branch Strategy Improvements**:
  - PM/Coding: Branch from base_branch (main/dev)
  - QA: Branch from feature branch
  - Auto branch creation/switching
  - Branch naming: `{prefix}/{ticket-number}-{slug}`

### Changed
- **Complete Directory Structure Reorganization**:
  - Removed fixed `be-`/`fe-` structure
  - Dynamic structure generation based on project type
  - Each project managed as independent Git repository
- **run-agent.sh Improvements**:
  - Auto project context detection (`.project-config.json`)
  - Auto Git branch creation (coding, qa)
  - Auto slug extraction from ticket file
- **git-branch-helper.sh Improvements**:
  - QA Agent uses feature branch as base
  - Auto-set prefix per agent (pm: docs, coding: feature, qa: test)
- **Documentation Reorganization**:
  - docs/: System developer documentation
  - logs-agent_dev/: System development logs
  - team/projects/{name}/logs/: Project implementation logs
- **.gitignore Update**:
  - Exclude projects/ subdirectories (independent repositories)

### Removed
- Fixed directory structure (FastAPI + Next.js dependency)
- Tech Stack-dependent structure

---

## [1.0.0] - 2026-03-09

### Added
- **Project Planner Agent**: Project decomposition and ticket creation
  - Phase-divided execution (context window management)
  - Batch ticket creation (5 at a time)
  - Resume functionality (`--resume`)
- **PM Agent**: API specs, UI specs, wireframes, test case generation
  - Interactive wireframe support (vanilla JS)
  - Auto filename generation based on tickets
- **BE Coding Agent**: FastAPI backend implementation
  - Layered Architecture
  - Repository Pattern (Protocol + Implementation)
  - Domain-specific exception handling
- **FE Coding Agent**: Next.js frontend implementation
  - App Router
  - Server/Client Component separation
  - Type safety (TypeScript)
- **QA-BE Agent**: pytest test suite creation
- **QA-FE Agent**: Vitest test suite creation
- **Git Branch Workflow Automation**:
  - `git-branch-helper.sh`
  - `.config/git-workflow.json` configuration file
  - Auto branch creation/switching per ticket (feature/be/PLAN-XXX, feature/fe/PLAN-XXX, etc.)
- **Rate Limit Management System**:
  - `rate-limit-check.sh`
  - `parse_usage.py`
  - Based on Claude Max 5x tier (35 requests warning, 45 requests stop)
- **Implementation Log System**: All agents write logs upon work completion
  - `applications/logs/{agent}/` directory
  - Decision history, alternative comparisons, reviewer notes
- **show-logs.sh**: Log viewing script
- **run-agent.sh**: Agent execution wrapper script

### Documentation
- README.md: Complete workflow guide
- Coding rules:
  - `.rules/be-coding-rules.md` (FastAPI)
  - `.rules/fe-coding-rules.md` (Next.js)
- Development logs: `logs-agent_dev/`
  - Git workflow automation logs
  - Context window management logs

---

## [0.1.0] - 2026-01-15 (Initial Beta)

### Added
- Basic agent structure
- Fixed FastAPI + Next.js stack
- Manual ticket creation workflow

---

[Unreleased]: https://github.com/user/repo/compare/v0.0.2...HEAD
[0.0.2]: https://github.com/user/repo/compare/v0.0.1...v0.0.2
[1.0.0]: https://github.com/user/repo/compare/v0.1.0...v0.0.1
[0.1.0]: https://github.com/user/repo/releases/tag/v0.1.0
