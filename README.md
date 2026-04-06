# Multi-Agent Coding Team

> **Tech Stack Agnostic 멀티 agent development 플랫폼**
>
> project ID어 → ticket 분해 → specification 작성 → code implementation → test 작성까지 automation

[![Version](https://img.shields.io/badge/version-v0.0.3-blue.svg)](https://github.com/your-repo)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production--ready-green.svg)]()

---

## 📖 Table of Contents

1. [project 개요](#-project-개요)
2. [핵심 개념](#-핵심-개념)
3. [system 아키텍처](#-system-아키텍처)
4. [Quick Start](#-quick-start)
5. [사용 방법](#-사용-방법)
6. [project Structure](#-project-Structure)
7. [file 흐름 and 연관성](#-file-흐름-and-연관성)
8. [development guide](#-development-guide)

---

## 🎯 project 개요

### 무엇을 하는 systemauthorization?

**Multi-Agent Coding Team**은 Claude Code 기반의 AI agent들이 협업하여 소프트웨어 development all 사이클을 automation하는 is 플랫폼.

```
아이디어 입력 → 자동 티켓 생성 → 명세서 작성 → 코드 구현 → 테스트 작성 → Git 커밋
         ↓
   완성된 프로젝트
```

### 왜 만들었나?

**problem점:**
- 반복적인 development task (CRUD, test code, specification 작성)
- framework마다 다른 코딩 룰과 best practice
- ticket → specification → code → test의 일관성 부족
- agent 간 문맥 share 어려움

**solution책:**
- **5개 agent**가 role을 분담하여 all pipeline automation
- **Tech Stack Agnostic**: 모든 언어, 모든 framework support
- **session share**: agent 간 문맥 share로 일관성 유지
- **3가지 interface**: web dashboard, REST API, CLI

### 주요 특징

✅ **완전 automation** - ticket 하나로 specification → code → test 완성
✅ **Tech Stack Agnostic** - Python, Go, Rust, TypeScript 등 모든 언어 support
✅ **web dashboard** - CLI 없이 브라우저에서 모든 task 가능
✅ **REST API** - 프로그래밍 방식으로 통합 가능
✅ **Discord/GitHub 연동** - 실time notification and PR auto review
✅ **session share** - agent 간 문맥 share로 일관된 result
✅ **project 격리** - 각 project는 독립 Git 리포지토리

---

## 🧠 핵심 개념

### 1. Agents vs Skills

**Agents (복잡한 의사결정)**
- status를 유지하며 컨text를 이해
- CLAUDE.md로 정의
- yes: PM Agent, Coding Agent, QA Agent

**Skills (반복 task automation)**
- Stateless, 재available
- skill.md로 정의
- yes: validate-spec, commit, review-pr

```
┌─────────────────────────────────────────┐
│  Agent (PM)                             │
│  - 티켓 읽기                             │
│  - 명세서 작성                           │
│  - validate-spec Skill 호출 ←─────┐    │
└─────────────────────────────────────────┘
                                           │
┌─────────────────────────────────────────┤
│  Skill (validate-spec)                  │
│  - 명세서 검증                           │
│  - 에러 리포트                           │
└─────────────────────────────────────────┘
```

### 2. 5개 agent pipeline

```
┌──────────────────────────────────────────────────────────────┐
│  Stack Initializer                                           │
│  - 프로젝트 타입별 코딩 룰 자동 생성                           │
│  - Acronym 생성 (예: "Todo App" → TODO)                      │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│  Project Planner                                             │
│  - 프로젝트 설명 → 티켓 분해                                   │
│  - 산출물: planning/tickets/{ACRONYM}-001-*.md               │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│  PM Agent                                                    │
│  - 티켓 → 명세서 + 테스트 케이스                               │
│  - Project Planner 세션 읽어 전체 맥락 이해                    │
│  - 산출물: planning/specs/, planning/test-cases/             │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│  Coding Agent                                                │
│  - 명세서 → 코드 구현                                          │
│  - PM 세션 읽어 의사결정 준수 (예: OAuth 제외 등)              │
│  - 산출물: src/                                              │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│  QA Agent                                                    │
│  - 테스트 케이스 → 테스트 코드                                 │
│  - PM + Coding 세션 읽어 포괄적 테스트 작성                    │
│  - 산출물: tests/                                            │
└──────────────────────────────────────────────────────────────┘
```

### 3. session share 아키텍처

agent들이 서로의 session을 읽어 문맥을 share:

```
projects/{project}/.sessions/
├── session-map.json              # 세션 ID 맵
├── TODO-001/
│   ├── project-planner.session   # Project Planner 세션 ID
│   ├── pm.session                # PM 세션 ID
│   ├── coding.session            # Coding 세션 ID
│   └── qa.session                # QA 세션 ID
```

**흐름:**
1. **Project Planner** → ticket create + session save
2. **PM** → Project Planner session 읽기 → all 맥락 이해 → specification 작성 + session save
3. **Coding** → PM session 읽기 → 의사결정 준수 → code implementation + session save
4. **QA** → PM + Coding session 읽기 → 포괄적 test 작성

### 4. Tech Stack Agnostic

**하드코딩 금지 원칙:**

```python
# ❌ 나쁜 예
if language == "python":
    run_pytest()
elif language == "go":
    run_go_test()

# ✅ 좋은 예
framework = meta.get("framework")
test_command = get_test_command(framework)  # 동적 감지
subprocess.run(test_command, shell=True)
```

**support project type:**
- **Web Fullstack**: FastAPI+React, Django+Vue, Next.js
- **Web MVC**: Django, Rails, Spring Boot
- **CLI Tool**: Click, Cobra, Clap
- **Desktop App**: Tauri, Electron, Qt
- **Mobile App**: React Native, Flutter
- **Library**: npm, pip, cargo package
- **Data Pipeline**: Airflow, Luigi

### 5. project별 Acronym

각 project는 unique한 Acronym을 가집니다:

```
"Bill Organizer" → BILL
- 티켓: BILL-001, BILL-002
- 브랜치: feature/BILL-001-user-auth

"Todo App" → TODO
- 티켓: TODO-001, TODO-002
- 브랜치: feature/TODO-001-task-crud
```

---

## 🏗️ system 아키텍처

### 레이어 Structure

```
┌─────────────────────────────────────────────────────────────┐
│  Interface Layer (3가지 방법)                                │
├─────────────────────────────────────────────────────────────┤
│  1. Web Dashboard (http://localhost:8000)                   │
│     - 버튼 클릭으로 파이프라인 실행                            │
│     - 실시간 모니터링                                         │
├─────────────────────────────────────────────────────────────┤
│  2. REST API (FastAPI)                                      │
│     - POST /api/pipeline/run                                │
│     - GET /api/pipeline/status/{ticket}                     │
│     - 25+ 엔드포인트                                          │
├─────────────────────────────────────────────────────────────┤
│  3. CLI Scripts                                             │
│     - bash scripts/run-agent.sh pm --ticket TODO-001        │
│     - python scripts/auto_pipeline_v2.py --ticket TODO-001  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Service Layer                                              │
├─────────────────────────────────────────────────────────────┤
│  - AgentService: 에이전트 실행 관리                           │
│  - SkillService: 스킬 실행 관리                               │
│  - PipelineService: 파이프라인 오케스트레이션                  │
│  - DiscordService: Discord 알림                             │
│  - WebhookService: GitHub Webhook 처리                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Execution Layer                                            │
├─────────────────────────────────────────────────────────────┤
│  - 5개 Agents (CLAUDE.md)                                   │
│  - 8개 Skills (skill.md)                                    │
│  - Claude Code CLI 호출 (subprocess)                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Data Layer                                                 │
├─────────────────────────────────────────────────────────────┤
│  - projects/{name}/     사용자 프로젝트 (독립 Git 리포)       │
│  - .config/             시스템 설정                          │
│  - .memory/             학습 데이터                          │
│  - .rules/              코딩 룰                              │
└─────────────────────────────────────────────────────────────┘
```

### file 흐름 yes시 (TODO-001 ticket)

```
1. 사용자 입력
   - 웹 대시보드에서 "Run Pipeline" 클릭
   - Ticket: TODO-001, Project: my-todo-app

2. API 레이어
   POST /api/pipeline/run
   → PipelineService.run_pipeline(ticket="TODO-001", project="my-todo-app")

3. 에이전트 실행
   PM Agent:
     입력: projects/my-todo-app/planning/tickets/TODO-001-user-auth.md
     읽기: projects/my-todo-app/.sessions/TODO-001/project-planner.session
     실행: cd team/.agents/pm && claude --append-system-prompt CLAUDE.md
     출력: projects/my-todo-app/planning/specs/TODO-001-api-spec.md
           projects/my-todo-app/planning/specs/TODO-001-ui-spec.md
           projects/my-todo-app/planning/test-cases/TODO-001-test-cases.md
     저장: projects/my-todo-app/.sessions/TODO-001/pm.session

   Coding Agent:
     입력: planning/specs/TODO-001-*.md
     읽기: projects/my-todo-app/.sessions/TODO-001/pm.session
     실행: cd team/.agents/coding && claude --append-system-prompt CLAUDE.md
     출력: projects/my-todo-app/src/auth.py
           projects/my-todo-app/src/routes/auth.py
     저장: projects/my-todo-app/.sessions/TODO-001/coding.session

   QA Agent:
     입력: planning/test-cases/TODO-001-test-cases.md
     읽기: projects/my-todo-app/.sessions/TODO-001/pm.session
           projects/my-todo-app/.sessions/TODO-001/coding.session
     실행: cd team/.agents/qa && claude --append-system-prompt CLAUDE.md
     출력: projects/my-todo-app/tests/test_auth.py
     저장: projects/my-todo-app/.sessions/TODO-001/qa.session

4. 스킬 실행
   validate-spec:
     입력: planning/specs/TODO-001-*.md
     실행: python team/.skills/validate-spec/validate.py
     출력: 검증 결과 (성공/실패)

   commit:
     입력: Git diff 분석
     실행: python team/.skills/commit/commit-message-generator.py
     출력: 커밋 메시지 생성

5. Git 작업
   - 브랜치 생성: feature/TODO-001-user-auth
   - 코드 커밋
   - (선택) PR 생성

6. 결과 반환
   - 웹 대시보드: 파이프라인 상태 업데이트
   - Discord: Complete 알림
```

---

## 🚀 Quick Start

### 사전 준비

- [Claude Code](https://docs.claude.ai/claude-code) installation and login
- Python 3.10+
- Git
- Claude Pro 플랜 권장

### 방법 1: web dashboard (🎨 추천)

```bash
# 1. 클론
git clone https://github.com/your-username/KR-multi-agent-coding-team.git
cd KR-multi-agent-coding-team/team

# 2. 의존성 설치
pip install -r Requirements.txt

# 3. 환경 변수 설정
cp .env.example .env
# .env 파일 편집:
# - ANTHROPIC_API_KEY=sk-ant-your-key (필수)
# - DISCORD_WEBHOOK_URL=https://... (선택)

# 4. API 서버 실행
uvicorn api.main:app --reload --port 8000

# 5. 브라우저에서 접속
# http://localhost:8000
```

**web dashboard 사용:**
1. **Agents tab** → 각 agent individual execute
2. **Pipelines tab** → all pipeline execute
3. **Skills tab** → 스킬 execute
4. **Statistics tab** → statistics confirmation

### 방법 2: REST API

```bash
# 파이프라인 실행
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{
    "ticket": "TODO-001",
    "project": "my-todo-app"
  }'

# 상태 확인
curl http://localhost:8000/api/pipeline/status/TODO-001

# API 문서
# http://localhost:8000/api/docs
```

### 방법 3: CLI

```bash
cd team

# 프로젝트 초기화
bash scripts/init-project.sh --interactive

# 에이전트 실행
bash scripts/run-agent.sh pm --ticket TODO-001
bash scripts/run-agent.sh coding --ticket TODO-001
bash scripts/run-agent.sh qa --ticket TODO-001

# 자동 파이프라인 (macOS 전용)
python scripts/auto_pipeline_v2.py --ticket TODO-001
```

---

## 📖 사용 방법

### 시나리오 1: 새 project create

**1stage: project initialize**

```bash
cd team
bash scripts/init-project.sh --interactive

# 또는 플래그 모드
bash scripts/init-project.sh \
  --type web-fullstack \
  --language python \
  --framework fastapi \
  --name my-todo-app
```

create되는 것:
- `projects/my-todo-app/` directory
- `.project-meta.json` (project configuration)
- `planning/tickets/` (ticket directory)
- `src/` (소스 code directory)
- 독립 Git 리포지토리 initialize

**2stage: Stack Initializer execute**

```bash
bash scripts/run-agent.sh stack-initializer
```

create되는 것:
- `.rules/_cache/{framework}.md` (코딩 룰)
- `.project-meta.json` update (Acronym add)

**3stage: ticket create**

```bash
bash scripts/run-agent.sh project-planner --project "할일 관리 앱 개발"

# 또는 파일로 입력
bash scripts/run-agent.sh project-planner --req Requirements.md
```

create되는 것:
- `planning/tickets/TODO-001-user-auth.md`
- `planning/tickets/TODO-002-task-crud.md`
- 등등...

**4stage: pipeline execute**

web dashboard에서:
1. Pipelines tab open
2. project optional: my-todo-app
3. ticket optional: TODO-001
4. "Run Pipeline" button click

또는 CLI:
```bash
python scripts/auto_pipeline_v2.py --ticket TODO-001
```

**5stage: result confirmation**

```bash
cd projects/my-todo-app

# 명세서
ls planning/specs/

# 코드
ls src/

# 테스트
ls tests/

# Git 브랜치
git branch
# * feature/TODO-001-user-auth
```

### 시나리오 2: 기존 project에 feature add

```bash
# 1. 프로젝트 전환
cd team
bash scripts/switch-project.sh my-todo-app

# 2. 새 티켓 생성
bash scripts/run-agent.sh project-planner --project "카테고리 기능 추가"

# 3. 파이프라인 실행
# 웹 대시보드에서 TODO-003 티켓 실행

# 4. PR 생성
cd projects/my-todo-app
gh pr create --title "feat: 카테고리 기능 추가"
```

### 시나리오 3: individual agent execute

```bash
cd team

# PM Agent만 실행
bash scripts/run-agent.sh pm --ticket TODO-001

# Coding Agent만 실행
bash scripts/run-agent.sh coding --ticket TODO-001

# QA Agent만 실행
bash scripts/run-agent.sh qa --ticket TODO-001
```

### 시나리오 4: 스킬 execute

```bash
cd team

# 명세서 검증
bash scripts/run-skill.sh validate-spec TODO-001

# 커밋 메시지 생성
cd projects/my-todo-app
bash ../../scripts/run-skill.sh commit TODO-001

# PR 리뷰
bash ../../scripts/run-skill.sh review-pr TODO-001
```

---

## 📁 project Structure

### all Structure

```
KR-multi-agent-coding-team/        (시스템 리포지토리)
├── .claude/                        # Claude Code 설정
├── .github/                        # GitHub 템플릿
├── docs/                           # 아키텍처 문서
│   ├── architecture.md
│   ├── phase1-complete.md
│   ├── phase2-complete.md
│   ├── phase3.3-complete.md
│   └── supported-tech-stacks.md
├── logs-agent_dev/                 # 개발 히스토리 로그
│   ├── 2026-03-20-dashboard-improvements.md
│   └── 2026-03-20-run-agent-improvements.md
├── team/                           # ← 핵심 작업 디렉토리
│   ├── .agents/                    # 5개 에이전트
│   ├── .skills/                    # 8개 스킬
│   ├── .rules/                     # 코딩 룰
│   ├── .config/                    # 시스템 설정
│   ├── .memory/                    # 학습 시스템
│   ├── api/                        # FastAPI REST API
│   ├── web/                        # 웹 대시보드
│   ├── scripts/                    # CLI 도구
│   ├── projects/                   # 사용자 프로젝트
│   └── docs/                       # 사용자 문서
├── CLAUDE.md                       # 시스템 개발 가이드
├── README.md                       # 이 파일
└── LICENSE

총 141개 파일, 약 15,000 라인
```

### team/ directory 상세

#### .agents/ (5개 agent)

```
.agents/
├── stack-initializer/
│   └── CLAUDE.md                   # 스택별 코딩 룰 자동 생성
├── project-planner/
│   └── CLAUDE.md                   # 프로젝트 → 티켓 분해
├── pm/
│   ├── CLAUDE.md                   # 티켓 → 명세서
│   ├── gotchas.md                  # 반복 실패 패턴
│   └── workflows/                  # 프로젝트 타입별 워크플로우
│       ├── web-fullstack.md
│       ├── cli-tool.md
│       ├── desktop-app.md
│       └── library.md
├── coding/
│   └── CLAUDE.md                   # 명세서 → 코드
└── qa/
    └── CLAUDE.md                   # 테스트 케이스 → 테스트 코드
```

#### .skills/ (8개 스킬)

```
.skills/
├── validate-spec/
│   ├── skill.md                    # 스킬 정의
│   ├── validate.py                 # 실행 스크립트
│   └── rules.json                  # 검증 룰
├── commit/
│   ├── skill.md
│   └── commit-message-generator.py
├── review-pr/
│   ├── skill.md
│   ├── review-pr.py
│   └── review-checklist.json
├── refactor-code/
│   ├── skill.md
│   └── refactor-code.py
├── test-runner/
│   └── skill.md
├── deploy/
│   └── skill.md
├── benchmark/
│   └── skill.md
└── docs-generator/
    └── skill.md
```

#### api/ (REST API - FastAPI)

```
api/
├── main.py                         # FastAPI 앱 엔트리포인트
├── config.py                       # 설정 (환경 변수)
├── models/
│   ├── request.py                  # Pydantic 요청 모델
│   └── response.py                 # Pydantic 응답 모델
├── routers/                        # 엔드포인트
│   ├── agents.py                   # POST /api/agents/{name}
│   ├── skills.py                   # POST /api/skills/{name}
│   ├── pipeline.py                 # POST /api/pipeline/run
│   ├── projects.py                 # GET /api/projects/list
│   └── webhooks.py                 # POST /api/webhooks/github
├── services/                       # 비즈니스 로직
│   ├── agent_service.py            # 에이전트 실행 관리
│   ├── skill_service.py            # 스킬 실행 관리
│   ├── pipeline_service.py         # 파이프라인 오케스트레이션
│   ├── discord_service.py          # Discord 알림
│   └── webhook_service.py          # Webhook 처리
└── README.md
```

#### web/ (web dashboard)

```
web/
├── index.html                      # 메인 페이지 (4개 탭)
├── static/
│   ├── css/
│   │   └── styles.css              # 스타일시트
│   └── js/
│       └── app.js                  # 프론트엔드 로직 (API 호출)
└── README.md
```

#### scripts/ (CLI 도구)

```
scripts/
├── init-project.sh                 # 프로젝트 초기화
├── switch-project.sh               # 프로젝트 전환
├── run-agent.sh                    # 에이전트 실행
├── run-skill.sh                    # 스킬 실행
├── auto_pipeline_v2.py             # 자동 파이프라인 (대화형)
├── git-branch-helper.sh            # Git 브랜치 자동 관리
├── rate-limit-check.sh             # Rate Limit 체크
├── .legacy/
│   └── auto_pipeline.py.bak        # v1 (deprecated)
└── README.md
```

#### projects/ (user project)

```
projects/
├── my-todo-app/                    # 프로젝트 A (독립 Git 리포)
│   ├── .git/                       # 독립 Git 리포지토리
│   ├── .project-meta.json          # 프로젝트 설정
│   ├── .sessions/                  # 에이전트 세션
│   │   ├── session-map.json
│   │   ├── TODO-001/
│   │   │   ├── pm.session
│   │   │   ├── coding.session
│   │   │   └── qa.session
│   ├── planning/
│   │   ├── tickets/                # 티켓
│   │   │   ├── TODO-001-user-auth.md
│   │   │   └── TODO-002-task-crud.md
│   │   ├── specs/                  # 명세서
│   │   │   ├── TODO-001-api-spec.md
│   │   │   └── TODO-001-ui-spec.md
│   │   └── test-cases/             # 테스트 케이스
│   │       └── TODO-001-test-cases.md
│   ├── src/                        # 소스 코드
│   ├── tests/                      # 테스트 코드
│   └── logs/                       # 에이전트 로그
└── my-blog/                        # 프로젝트 B
    └── ...
```

#### .config/ (system configuration)

```
.config/
├── git-workflow.json               # Git 브랜치 전략
├── auto-responses.json             # 자동 응답 패턴
└── log-schema.json                 # 로그 스키마
```

#### .memory/ (learning system)

```
.memory/
├── patterns.json                   # 학습된 의사결정 패턴
├── commit-history.json             # 커밋 히스토리
├── review-history.json             # 리뷰 히스토리
├── successes.json                  # 성공 사례
├── failures.json                   # 실패 사례
└── refactor-patterns.json          # 리팩토링 패턴
```

#### .rules/ (코딩 룰)

```
.rules/
├── general-coding-rules.md         # 범용 원칙 (DRY, KISS 등)
├── _cache/                         # AI 자동 생성 (24h TTL)
│   └── {framework}.md
└── _verified/                      # 사람이 검증
    ├── web-fullstack/
    │   ├── backend-fastapi-python.md
    │   └── frontend-nextjs-typescript.md
    └── desktop-app/
        └── qt-cpp-kr.md
```

---

## 🔄 file 흐름 and 연관성

### 1. project initialize 흐름

```
사용자
  ↓ bash scripts/init-project.sh --interactive
init-project.sh
  ↓ 프로젝트 정보 입력 받음
  ↓ projects/{name}/ 디렉토리 생성
  ↓ .project-meta.json 생성
  ↓ git init
Stack Initializer Agent
  ↓ 읽기: .project-meta.json
  ↓ Stack Initializer CLAUDE.md 로드
  ↓ 공식 문서 분석하여 코딩 룰 생성
  ↓ 출력: .rules/_cache/{framework}.md
  ↓ 출력: .project-meta.json (Acronym 추가)
프로젝트 준비 Complete
```

**file 연관성:**
- `scripts/init-project.sh` → project directory create
- `.project-meta.json` → project configuration save
- `.agents/stack-initializer/CLAUDE.md` → agent 지시사항
- `.rules/_cache/` → create된 코딩 룰
- `.config/git-workflow.json` → Git branch 전략 reference

### 2. ticket create 흐름

```
사용자
  ↓ bash scripts/run-agent.sh project-planner --req Requirements.md
run-agent.sh
  ↓ .project-config.json 읽어 현재 프로젝트 확인
  ↓ Requirements.md 읽기
Project Planner Agent
  ↓ Project Planner CLAUDE.md 로드
  ↓ .project-meta.json 읽어 Acronym 확인
  ↓ 프로젝트 분해 (아이디어 → 티켓들)
  ↓ 출력: planning/tickets/{ACRONYM}-001-*.md
  ↓ 출력: planning/tickets/{ACRONYM}-002-*.md
  ↓ 세션 저장: .sessions/{ACRONYM}-001/project-planner.session
티켓 생성 Complete
```

**file 연관성:**
- `Requirements.md` → input (user 작성)
- `.project-config.json` → currently enabled project
- `projects/{name}/.project-meta.json` → Acronym
- `.agents/project-planner/CLAUDE.md` → agent 지시사항
- `planning/tickets/` → output
- `.sessions/` → session save

### 3. pipeline execute 흐름 (web dashboard)

```
사용자 (브라우저)
  ↓ http://localhost:8000 접속
web/index.html
  ↓ 프로젝트 목록 로드
web/static/js/app.js
  ↓ GET /api/projects/list
api/routers/projects.py
  ↓ projects/ 디렉토리 스캔
  ↓ 반환: 프로젝트 목록
사용자
  ↓ 프로젝트 선택 (my-todo-app)
app.js
  ↓ GET /api/projects/my-todo-app/tickets
api/routers/projects.py
  ↓ planning/tickets/ 스캔
  ↓ 반환: 티켓 목록
사용자
  ↓ 티켓 선택 (TODO-001)
  ↓ "Run Pipeline" 클릭
app.js
  ↓ POST /api/pipeline/run {ticket: "TODO-001", project: "my-todo-app"}
api/routers/pipeline.py
  ↓ PipelineService.run_pipeline()
api/services/pipeline_service.py
  ↓ PM Agent 실행
  ↓ Coding Agent 실행
  ↓ QA Agent 실행
  ↓ Discord 알림
Discord
  ↓ 알림 수신 (Complete)
사용자 (브라우저)
  ↓ 실시간 상태 업데이트 (5초마다 폴링)
```

**file 연관성:**
- `web/index.html` → UI Structure
- `web/static/js/app.js` → API call
- `api/main.py` → FastAPI 앱
- `api/routers/pipeline.py` → endpoint
- `api/services/pipeline_service.py` → 비즈니스 로직
- `api/services/agent_service.py` → agent execute
- `api/services/discord_service.py` → Discord notification
- `scripts/run-agent.sh` → 실제 agent execute

### 4. PM Agent execute 흐름

```
PipelineService
  ↓ AgentService.run_agent("pm", ticket="TODO-001")
api/services/agent_service.py
  ↓ 티켓 파일 경로 확인
  ↓ planning/tickets/TODO-001-*.md
  ↓ subprocess로 claude CLI 호출
  ↓ cd .agents/pm && claude --append-system-prompt CLAUDE.md
PM Agent (claude CLI)
  ↓ CLAUDE.md 읽기
  ↓ gotchas.md 읽기 (실패 패턴 학습)
  ↓ .project-meta.json 읽어 project_type 확인
  ↓ workflows/{project_type}.md 읽기
  ↓ .sessions/{ticket}/project-planner.session 읽기 (이전 맥락)
  ↓ 티켓 파일 읽기
  ↓ 명세서 작성
  ↓ 출력: planning/specs/{ticket}-api-spec.md
  ↓ 출력: planning/specs/{ticket}-ui-spec.md
  ↓ 출력: planning/test-cases/{ticket}-test-cases.md
  ↓ validate-spec 스킬 자동 실행
  ↓ 세션 저장: .sessions/{ticket}/pm.session
PM Agent Complete
```

**file 연관성:**
- `planning/tickets/{ticket}.md` → input
- `.agents/pm/CLAUDE.md` → agent 지시사항
- `.agents/pm/gotchas.md` → failure pattern
- `.agents/pm/workflows/{project_type}.md` → project type별 워크플로우
- `.project-meta.json` → project type confirmation
- `.sessions/{ticket}/project-planner.session` → previous session
- `planning/specs/` → output
- `planning/test-cases/` → output
- `.sessions/{ticket}/pm.session` → session save
- `.skills/validate-spec/` → 스킬 call

### 5. Coding Agent execute 흐름

```
PipelineService
  ↓ AgentService.run_agent("coding", ticket="TODO-001")
api/services/agent_service.py
  ↓ subprocess로 claude CLI 호출
Coding Agent
  ↓ CLAUDE.md 읽기
  ↓ .project-meta.json 읽어 language, framework 확인
  ↓ .rules/general-coding-rules.md 읽기
  ↓ .rules/_cache/{framework}.md 또는 _verified/ 읽기
  ↓ .sessions/{ticket}/pm.session 읽기 (PM 의사결정 이해)
  ↓ planning/specs/ 읽기
  ↓ 코드 구현
  ↓ 출력: src/auth.py
  ↓ 출력: src/routes/auth.py
  ↓ Git 브랜치 생성: feature/{ticket}
  ↓ commit 스킬 자동 실행
  ↓ 세션 저장: .sessions/{ticket}/coding.session
Coding Agent Complete
```

**file 연관성:**
- `.agents/coding/CLAUDE.md` → agent 지시사항
- `.project-meta.json` → 언어/framework
- `.rules/general-coding-rules.md` → 범용 코딩 룰
- `.rules/_cache/{framework}.md` → framework별 룰
- `.sessions/{ticket}/pm.session` → PM 의사결정
- `planning/specs/` → input
- `src/` → output
- `.skills/commit/` → 스킬 call
- `.config/git-workflow.json` → branch 전략
- `.sessions/{ticket}/coding.session` → session save

### 6. QA Agent execute 흐름

```
PipelineService
  ↓ AgentService.run_agent("qa", ticket="TODO-001")
api/services/agent_service.py
  ↓ subprocess로 claude CLI 호출
QA Agent
  ↓ CLAUDE.md 읽기
  ↓ .project-meta.json 읽어 test_framework 확인
  ↓ .rules/general-coding-rules.md 읽기 (테스트 원칙)
  ↓ .sessions/{ticket}/pm.session 읽기
  ↓ .sessions/{ticket}/coding.session 읽기
  ↓ planning/test-cases/ 읽기
  ↓ src/ 코드 분석
  ↓ 테스트 코드 작성
  ↓ 출력: tests/test_auth.py
  ↓ test-runner 스킬 자동 실행
  ↓ 세션 저장: .sessions/{ticket}/qa.session
QA Agent Complete
```

**file 연관성:**
- `.agents/qa/CLAUDE.md` → agent 지시사항
- `.project-meta.json` → test framework
- `.rules/general-coding-rules.md` → test 원칙
- `.sessions/{ticket}/pm.session` → PM 맥락
- `.sessions/{ticket}/coding.session` → Coding 맥락
- `planning/test-cases/` → input
- `src/` → analytics 대상
- `tests/` → output
- `.skills/test-runner/` → 스킬 call
- `.sessions/{ticket}/qa.session` → session save

### 7. 스킬 execute 흐름

```
validate-spec 스킬:
  PM Agent
    ↓ bash scripts/run-skill.sh validate-spec {ticket}
  run-skill.sh
    ↓ .skills/validate-spec/skill.md 읽기
    ↓ python .skills/validate-spec/validate.py
  validate.py
    ↓ planning/specs/ 읽기
    ↓ .skills/validate-spec/rules.json 읽기
    ↓ 검증 (완전성, 일관성, 품질)
    ↓ 에러 리포트 생성
    ↓ .memory/failures.json 업데이트 (실패 시)
    ↓ .memory/successes.json 업데이트 (성공 시)
  검증 Complete

commit 스킬:
  Coding Agent
    ↓ bash scripts/run-skill.sh commit {ticket}
  run-skill.sh
    ↓ .skills/commit/skill.md 읽기
    ↓ python .skills/commit/commit-message-generator.py
  commit-message-generator.py
    ↓ git diff 분석
    ↓ .memory/commit-history.json 읽어 패턴 학습
    ↓ Conventional Commits 형식 커밋 메시지 생성
    ↓ git commit 실행
    ↓ .memory/commit-history.json 업데이트
  커밋 Complete
```

**file 연관성:**
- `.skills/{skill}/skill.md` → 스킬 정의
- `.skills/{skill}/*.py` → execute script
- `.skills/{skill}/*.json` → configuration/rule
- `.memory/*.json` → learning data
- `planning/specs/` → input (validate-spec)
- `git diff` → input (commit)

---

## 🛠️ development guide

### system developer용

**CLAUDE.md** (project 루트)를 please reference:
- system 아키텍처 상세
- Agent vs Skill 분리 원칙
- Tech Stack Agnostic implementation 방법
- 코딩 rule (DRY, SRP, KISS 등)
- file create/fix 시 documentation rule

### 새 Agent add

1. `.agents/{new-agent}/` directory create
2. `CLAUDE.md` 작성 (role, input, output, task 순서)
3. `scripts/run-agent.sh`에 케이스 add
4. `api/routers/agents.py`에 endpoint add
5. test

### 새 Skill add

1. `.skills/{new-skill}/` directory create
2. `skill.md` 작성 (정의, input, output)
3. `{skill}.py` execute script 작성
4. `scripts/run-skill.sh`에 케이스 add
5. `api/routers/skills.py`에 endpoint add
6. test

### 새 project type add

1. `docs/supported-tech-stacks.md`에 add
2. `.agents/pm/workflows/{new-type}.md` 작성
3. `.rules/_verified/{new-type}/` 코딩 룰 add
4. Stack Initializer가 auto으로 감지

### API endpoint add

1. `api/models/request.py`에 request model add
2. `api/models/response.py`에 response model add
3. `api/routers/{router}.py`에 endpoint add
4. `api/services/{service}.py`에 비즈니스 로직 add
5. `api/main.py`에 라우터 등록 (이미 되어있으면 생략)
6. `api/README.md`에 documentation
7. Swagger UI에서 test

### web dashboard fix

1. `web/index.html` - HTML Structure fix
2. `web/static/js/app.js` - 로직 fix
3. `web/static/css/styles.css` - style fix
4. `web/README.md` - documentation

---

## 📚 reference documentation

### user documentation
- [API documentation](team/api/README.md) - REST API all guide
- [web dashboard guide](team/web/README.md) - web dashboard usage
- [Skills guide](team/docs/skills-guide.md) - 8개 스킬 상세
- [Auto Pipeline v2 guide](team/docs/auto-pipeline-v2-guide.md) - auto pipeline usage
- [session 관리](team/docs/session-management.md) - session share 아키텍처

### developer documentation
- [CLAUDE.md](CLAUDE.md) - system development guide
- [Architecture](docs/architecture.md) - 아키텍처 상세
- [Supported Tech Stacks](docs/supported-tech-stacks.md) - support 스택 list
- [Phase 4 Complete](team/docs/phase4-complete.md) - Phase 4 completed 보고서

### change 로그
- [logs-agent_dev/](logs-agent_dev/) - development 히스토리 로그

---

## 🔄 version 히스토리

### v0.0.3 (2026-03-20) - Dashboard UX improvement + 워크플로우 improvement

**Dashboard 사용성 improvement:**
- ✅ 각 agent별 optimization된 input 폼
  - Project Planner: Requirements file upload support
  - PM/Coding/QA: project/ticket select box
  - Stack Initializer: project select box만
- ✅ project/ticket auto load (API 연동)
- ✅ Agents tab을 첫 번째 tab으로 change

**CLI 사용성 improvement:**
- ✅ PM Agent: `--ticket PLAN-001` 형식으로 통일
- ✅ Project Planner: `--req Requirements.md` option add

**session share:**
- ✅ agent 간 문맥 share (`.sessions/` directory)
- ✅ PM → Coding → QA sequential적 맥락 전달

**project별 Acronym:**
- ✅ Stack Initializer가 auto create
- ✅ ticket 번호 형식: `{ACRONYM}-XXX`

**비용 optimization:**
- ✅ Anthropic API SDK → Claude Code CLI 전환
- ✅ 비용 90% 절감 (yes상)

### v0.0.3 (2026-03-19) - web 플랫폼 완성

**Backend:**
- ✅ FastAPI REST API (25+ endpoint)
- ✅ Pydantic model (Request/Response)
- ✅ Background Tasks

**Integration:**
- ✅ Discord Webhook (6가지 notification type)
- ✅ GitHub Webhook (PR auto review)

**Frontend:**
- ✅ web dashboard (4개 tab)
- ✅ 실time 모니터링 (5초 auto 갱신)

---

## 🤝 기여

### validation된 코딩 룰 기여
`.rules/_verified/`에 new운 스택의 코딩 룰을 can 기여 있습니다.

### new운 스킬 기여
`.skills/` directory에 new운 스킬을 can add 있습니다.

### API endpoint 기여
`team/api/routers/`에 new운 라우터를 can add 있습니다.

---

## 📄 license

MIT License - 자세한 content은 [LICENSE](LICENSE) file reference

---

## 🔗 관련 link

- **Claude Code documentation**: https://docs.claude.ai/claude-code
- **API documentation**: http://localhost:8000/api/docs (서버 execute 후)
- **Discord Developer Portal**: https://discord.com/developers
- **GitHub Webhooks**: https://docs.github.com/en/webhooks

---

**version**: v0.0.3
**최종 update**: 2026-03-20
**총 file**: 141개
**총 라인**: ~15,000 lines

---

**🌟 이제 Multi-Agent Coding Team은 web dashboard, REST API, CLI 3가지 방법으로 can 사용 있습니다!**
