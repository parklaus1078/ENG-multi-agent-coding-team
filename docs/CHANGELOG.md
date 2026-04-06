# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v0.0.2.html).

---

## [Unreleased]

---

## [0.0.2] - 2026-03-12

### Added
- **Tech Stack Agnostic Architecture**: 모든 development type support
  - web-fullstack, web-mvc, cli-tool, desktop-app, mobile-app, library, data-pipeline
- **project 격리 Structure**: `team/projects/{project-name}/`
  - 각 project는 독립적인 Git 리포지토리
  - project별 planning, logs directory
  - multiple project concurrent 관리 가능
- **Stack Initializer Agent**: project type and 스택에 맞는 환경 auto initialize
  - 공식 documentation auto analytics (WebSearch, WebFetch)
  - 코딩 룰 auto create (`.rules/_cache/`)
  - PM/Coding/QA template auto create
  - project 초기 Structure create
- **init-project.sh**: project initialize script
  - 대화형 mode support
  - flag 방식 support
  - Stack Initializer Agent auto call
- **통합 agent Structure**: `coding`, `qa` agent (모든 type support)
- **동적 template system**: `.agents/{agent}/templates/{project_type}.md`
- **코딩 룰 우선ranking system**:
  - `.rules/_verified/`: 사람이 validation한 룰 (최우선)
  - `.rules/_cache/`: auto create 룰 (24time cache)
- **범용 코딩 원칙**: `.rules/general-coding-rules.md` (DRY, SOLID, 보Plan 등)
- **project 메타data**: `.project-meta.json` (각 project)
- **전역 project configuration**: `.project-config.json` (루트)
- **configuration 스키마**: `.project-config.schema.json`
- **Git branch 전략 improvement**:
  - PM/Coding: base_branch (main/dev)에서 분기
  - QA: feature branch에서 분기
  - auto branch create/전환
  - branch명: `{prefix}/{ticket-number}-{slug}`

### Changed
- **directory Structure 전면 재편**:
  - 고정된 `be-`/`fe-` Structure remove
  - project type 기반 동적 Structure create
  - 각 project가 독립적인 Git 리포지토리로 관리
- **run-agent.sh improvement**:
  - auto project 컨text 감지 (`.project-config.json`)
  - auto Git branch create (coding, qa)
  - ticket file에서 slug auto 추출
- **git-branch-helper.sh improvement**:
  - QA Agent는 feature branch를 베이스로 사용
  - agent별 prefix auto configuration (pm: docs, coding: feature, qa: test)
- **documentation 재정리**:
  - docs/: system developer용 documentation
  - logs-agent_dev/: system development 로그
  - team/projects/{name}/logs/: project implementation 로그
- **.gitignore update**:
  - projects/ 하up directory 제외 (독립 리포지토리)

### Removed
- 고정된 directory Structure (FastAPI + Next.js 종속)
- Tech Stack 종속적인 Structure

---

## [1.0.0] - 2026-03-09

### Added
- **Project Planner Agent**: project 분해 and ticket create
  - Phase 분할 execute (컨text 윈도우 관리)
  - 배치 단up ticket create (5개씩)
  - resume feature (`--resume`)
- **PM Agent**: API specification, UI specification, 와이어프레임, test case create
  - 인터랙션 와이어프레임 support (바닐라 JS)
  - ticket 기반 auto file명 create
- **BE Coding Agent**: FastAPI backend implementation
  - Layered Architecture
  - Repository Pattern (Protocol + Implementation)
  - 도메인별 yes외 process
- **FE Coding Agent**: Next.js frontend implementation
  - App Router
  - Server/Client Component 분리
  - type Plan전성 (TypeScript)
- **QA-BE Agent**: pytest test 스up트 작성
- **QA-FE Agent**: Vitest test 스up트 작성
- **Git branch 워크플로우 automation**:
  - `git-branch-helper.sh`
  - `.config/git-workflow.json` configuration file
  - ticket별 auto branch create/전환 (feature/be/PLAN-XXX, feature/fe/PLAN-XXX 등)
- **Rate Limit 관리 system**:
  - `rate-limit-check.sh`
  - `parse_usage.py`
  - Claude Max 5x 티어 기준 (35회 warning, 45회 stop)
- **implementation 로그 system**: 모든 agent가 task completed 시 로그 작성
  - `applications/logs/{agent}/` directory
  - 의사결정 내역, 대Plan compare, 검수자 note사항 포함
- **show-logs.sh**: 로그 조회 script
- **run-agent.sh**: agent execute 래퍼 script

### Documentation
- README.md: all 워크플로우 guide
- 코딩 룰:
  - `.rules/be-coding-rules.md` (FastAPI)
  - `.rules/fe-coding-rules.md` (Next.js)
- development 로그: `logs-agent_dev/`
  - Git 워크플로우 automation 로그
  - 컨text 윈도우 관리 로그

---

## [0.1.0] - 2026-01-15 (초기 베타)

### Added
- default agent Structure
- FastAPI + Next.js 고정 스택
- manual ticket create 워크플로우

---

[Unreleased]: https://github.com/user/repo/compare/v0.0.2...HEAD
[0.0.2]: https://github.com/user/repo/compare/v0.0.1...v0.0.2
[1.0.0]: https://github.com/user/repo/compare/v0.1.0...v0.0.1
[0.1.0]: https://github.com/user/repo/releases/tag/v0.1.0
