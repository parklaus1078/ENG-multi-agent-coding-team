# 멀티 agent system 아키텍처

> Tech Stack Agnostic 범용 멀티 agent development 워크플로우

**version**: v0.0.2
**최종 update**: 2026-03-12
**대상**: system developer

---

## 🎯 핵심 설계 원칙

### 1. **동적 directory Structure**
- project type에 따라 required한 directory만 create
- 고정된 directory Structure none (project type에 따라 동적 create)
- 모든 산출물은 project type 기반으로 조직화

### 2. **project 격리**
- 각 project는 독립된 directory (`team/projects/{project-name}/`)
- **각 project는 독립적인 Git 리포지토리**로 관리
- project별 planning, project별 logs
- multiple project concurrent 관리 가능

### 3. **type 기반 Structure화**
- web-fullstack → `backend/`, `frontend/` 분리
- web-mvc → single `src/` directory
- cli-tool → `cmd/`, `internal/` (Go) 또는 framework별 Structure
- desktop-app → 플랫폼별 Structure

---

## 📂 최종 directory Structure

```
team/
├── .project-config.json                    # 현재 활성 프로젝트 설정
├── .project-config.schema.json             # 설정 스키마
│
├── .agents/                                 # 에이전트 지시 파일
│   ├── stack-initializer/
│   │   └── CLAUDE.md
│   ├── project-planner/
│   │   └── CLAUDE.md
│   ├── pm/
│   │   ├── CLAUDE.md
│   │   └── templates/                       # 타입별 PM 템플릿
│   │       ├── web-fullstack.md
│   │       ├── web-mvc.md
│   │       ├── cli-tool.md
│   │       ├── desktop-app.md
│   │       ├── mobile-app.md
│   │       ├── library.md
│   │       └── data-pipeline.md
│   ├── coding/
│   │   ├── CLAUDE.md
│   │   └── templates/                       # 타입별 코딩 템플릿
│   │       ├── web-fullstack.md
│   │       ├── web-mvc.md
│   │       ├── cli-tool.md
│   │       ├── desktop-app.md
│   │       ├── mobile-app.md
│   │       ├── library.md
│   │       └── data-pipeline.md
│   └── qa/
│       ├── CLAUDE.md
│       └── templates/                       # 타입별 QA 템플릿
│           ├── web-fullstack.md
│           ├── web-mvc.md
│           ├── cli-tool.md
│           ├── desktop-app.md
│           ├── mobile-app.md
│           ├── library.md
│           └── data-pipeline.md
│
├── .rules/                                  # 코딩 룰
│   ├── README.md
│   ├── general-coding-rules.md              # 범용 원칙
│   ├── _verified/                           # 사람이 검증한 룰
│   │   ├── web-fullstack/
│   │   │   ├── backend-fastapi-python.md
│   │   │   └── frontend-nextjs-typescript.md
│   │   ├── web-mvc/
│   │   │   ├── django-python.md
│   │   │   └── springboot-java.md
│   │   ├── cli-tool/
│   │   │   ├── click-python.md
│   │   │   └── cobra-go.md
│   │   ├── desktop-app/
│   │   │   ├── tauri-rust.md
│   │   │   └── electron-typescript.md
│   │   └── ...
│   └── _cache/                              # 자동 생성 룰 (24시간)
│       └── (동적 생성)
│
├── .config/
│   └── git-workflow.json                    # Git 브랜치 전략
│
├── scripts/
│   ├── init-project.sh                      # 프로젝트 초기화
│   ├── run-agent.sh                         # 에이전트 실행
│   ├── rate-limit-check.sh
│   ├── parse_usage.py
│   ├── show-logs.sh
│   ├── git-branch-helper.sh
│   └── create-dev-log.sh
│
├── projects/                                # 🆕 프로젝트 루트 (applications 대체)
│   ├── my-todo-app/                         # 예시: Web Fullstack
│   │   ├── .project-meta.json               # 프로젝트 메타데이터
│   │   ├── planning/                        # 기획 문서
│   │   │   ├── tickets/
│   │   │   │   ├── PLAN-001-user-auth.md
│   │   │   │   └── PLAN-002-todo-crud.md
│   │   │   ├── specs/                       # 명세서 (타입별 Structure)
│   │   │   │   ├── backend/
│   │   │   │   │   ├── PLAN-001-api-spec.md
│   │   │   │   │   └── PLAN-002-api-spec.md
│   │   │   │   └── frontend/
│   │   │   │       ├── PLAN-001-ui-spec.md
│   │   │   │       ├── PLAN-001-wireframe.html
│   │   │   │       ├── PLAN-002-ui-spec.md
│   │   │   │       └── PLAN-002-wireframe.html
│   │   │   └── test-cases/                  # 테스트 케이스
│   │   │       ├── backend/
│   │   │       │   ├── PLAN-001-tests.md
│   │   │       │   └── PLAN-002-tests.md
│   │   │       └── frontend/
│   │   │           ├── PLAN-001-tests.md
│   │   │           └── PLAN-002-tests.md
│   │   ├── src/                             # 실제 코드
│   │   │   ├── backend/
│   │   │   │   ├── src/
│   │   │   │   ├── tests/
│   │   │   │   ├── Requirements.txt
│   │   │   │   └── .env.example
│   │   │   └── frontend/
│   │   │       ├── src/
│   │   │       ├── public/
│   │   │       ├── package.json
│   │   │       └── .env.example
│   │   ├── logs/                            # 프로젝트별 로그
│   │   │   ├── stack-initializer/
│   │   │   ├── project-planner/
│   │   │   ├── pm/
│   │   │   ├── coding/
│   │   │   └── qa/
│   │   └── README.md
│   │
│   ├── file-search-cli/                     # 예시: CLI Tool
│   │   ├── .project-meta.json
│   │   ├── planning/
│   │   │   ├── tickets/
│   │   │   │   ├── PLAN-001-search-cmd.md
│   │   │   │   └── PLAN-002-filter-cmd.md
│   │   │   ├── specs/                       # CLI 전용 Structure
│   │   │   │   ├── PLAN-001-command-spec.md
│   │   │   │   └── PLAN-002-command-spec.md
│   │   │   └── test-cases/
│   │   │       ├── PLAN-001-tests.md
│   │   │       └── PLAN-002-tests.md
│   │   ├── src/                             # Go Cobra Structure
│   │   │   ├── cmd/
│   │   │   │   ├── root.go
│   │   │   │   ├── search.go
│   │   │   │   └── filter.go
│   │   │   ├── internal/
│   │   │   ├── go.mod
│   │   │   ├── go.sum
│   │   │   └── main.go
│   │   ├── logs/
│   │   └── README.md
│   │
│   └── admin-dashboard/                     # 예시: Web MVC (Django)
│       ├── .project-meta.json
│       ├── planning/
│       │   ├── tickets/
│       │   ├── specs/                       # MVC 전용 Structure
│       │   │   ├── PLAN-001-endpoint-spec.md
│       │   │   ├── PLAN-001-template-spec.md
│       │   │   └── PLAN-002-endpoint-spec.md
│       │   └── test-cases/
│       │       ├── PLAN-001-tests.md
│       │       └── PLAN-002-tests.md
│       ├── src/                             # Django Structure
│       │   ├── manage.py
│       │   ├── config/
│       │   ├── apps/
│       │   ├── templates/
│       │   ├── static/
│       │   └── Requirements.txt
│       ├── logs/
│       └── README.md
│
└── docs/                                    # 시스템 문서
    ├── architecture.md                      # 이 파일
    ├── git-branch-strategy.md
    └── supported-tech-stacks.md
```

---

## 🔑 핵심 change사항

### 1. project 격리 Structure

**핵심 원칙**:
- 각 project는 독립적인 directory
- project type에 따라 동적으로 Structure create
- project별 완전 격리

**Structure**:
```
projects/
└── {project-name}/
    ├── .project-meta.json        # 프로젝트 메타데이터
    ├── planning/                 # 기획 문서 (프로젝트별)
    ├── src/                      # 실제 코드
    └── logs/                     # 로그 (프로젝트별)
```

### 2. `.project-meta.json` (project별 메타data)

각 project directory에 location:

```json
{
  "project_name": "my-todo-app",
  "project_type": "web-fullstack",
  "stack": {
    "backend": {
      "language": "python",
      "framework": "fastapi",
      "version": "0.110.0"
    },
    "frontend": {
      "language": "typescript",
      "framework": "nextjs",
      "version": "14.0.0"
    }
  },
  "created_at": "2026-03-12T10:00:00Z",
  "directory_structure": "web-fullstack",
  "active": true
}
```

### 3. `.project-config.json` (루트 level, currently enabled project)

```json
{
  "current_project": "my-todo-app",
  "current_project_path": "projects/my-todo-app",
  "recent_projects": [
    "my-todo-app",
    "file-search-cli",
    "admin-dashboard"
  ]
}
```

### 4. `planning/` directory Structure (type별 동적 create)

#### Web Fullstack

```
planning/
├── tickets/
├── specs/
│   ├── backend/                  # API 명세서
│   └── frontend/                 # UI 명세서 + 와이어프레임
└── test-cases/
    ├── backend/
    └── frontend/
```

#### Web MVC

```
planning/
├── tickets/
├── specs/
│   ├── endpoints/                # 엔드포인트 명세서
│   └── templates/                # 템플릿 명세서
└── test-cases/
```

#### CLI Tool

```
planning/
├── tickets/
├── specs/                        # 커맨드 명세서 (플랫 Structure)
│   ├── PLAN-001-command-spec.md
│   └── PLAN-002-command-spec.md
└── test-cases/
    ├── PLAN-001-tests.md
    └── PLAN-002-tests.md
```

#### Desktop App

```
planning/
├── tickets/
├── specs/
│   ├── screens/                  # 화면 명세서
│   ├── state/                    # 상태 관리 명세서
│   └── ipc/                      # IPC 명세서 (Electron/Tauri)
└── test-cases/
    ├── unit/
    ├── integration/
    └── e2e/
```

#### Library

```
planning/
├── tickets/
├── specs/
│   ├── api/                      # API 시그니처
│   └── examples/                 # 사용 예시
└── test-cases/
```

#### Data Pipeline

```
planning/
├── tickets/
├── specs/
│   ├── dags/                     # DAG 정의
│   ├── transforms/               # 데이터 변환 로직
│   └── schedules/                # 스케줄 정의
└── test-cases/
```

---

## 🚀 워크플로우 (최종)

### 1. project initialize

```bash
cd team
bash scripts/init-project.sh --interactive
```

**input**:
- project type: `cli-tool`
- 언어: `go`
- framework: `cobra`
- project name: `file-search-cli`

**Stack Initializer Agent가 perform**:

1. `projects/file-search-cli/` directory create
2. `.project-meta.json` create
3. `planning/` directory create (CLI Tool Structure)
   ```
   planning/
   ├── tickets/
   ├── specs/
   └── test-cases/
   ```
4. `src/` directory create (Go Cobra Structure)
   ```
   src/
   ├── cmd/
   │   └── root.go
   ├── internal/
   ├── go.mod
   └── main.go
   ```
5. `logs/` directory create
6. `.rules/_cache/cli-tool/cobra-go.md` create (또는 _verified 사용)
7. 루트의 `.project-config.json` update (currently project configuration)

### 2. ticket create

```bash
bash scripts/run-agent.sh project-planner \
  --project "파일명 검색 + 콘텐츠 검색 CLI"
```

**산출물**:
```
projects/file-search-cli/planning/tickets/
├── PLAN-001-search-by-name.md
└── PLAN-002-search-by-content.md
```

### 3. PM (specification create)

```bash
bash scripts/run-agent.sh pm \
  --ticket-file projects/file-search-cli/planning/tickets/PLAN-001-search-by-name.md
```

**PM Agent action**:
1. `.project-config.json` 읽기 → currently project: `file-search-cli`
2. `projects/file-search-cli/.project-meta.json` 읽기 → type: `cli-tool`
3. `.agents/pm/templates/cli-tool.md` template load
4. specification create:
   ```
   projects/file-search-cli/planning/specs/
   └── PLAN-001-command-spec.md

   projects/file-search-cli/planning/test-cases/
   └── PLAN-001-tests.md
   ```

### 4. 코딩

```bash
bash scripts/run-agent.sh coding --ticket PLAN-001
```

**Coding Agent action**:
1. `.project-config.json` → currently project confirmation
2. `.project-meta.json` → type, 스택 confirmation
3. `.agents/coding/templates/cli-tool.md` template load
4. `.rules/_verified/cli-tool/cobra-go.md` 또는 `_cache` load
5. code create:
   ```
   projects/file-search-cli/src/
   ├── cmd/
   │   ├── root.go
   │   └── search.go        # 🆕 생성
   └── internal/
       └── search/          # 🆕 생성
           └── finder.go
   ```
6. 로그 create:
   ```
   projects/file-search-cli/logs/coding/
   └── 20260312-143000-PLAN-001-search.md
   ```

### 5. QA

```bash
bash scripts/run-agent.sh qa --ticket PLAN-001
```

**산출물**:
```
projects/file-search-cli/src/
└── internal/
    └── search/
        └── finder_test.go   # 🆕 생성

projects/file-search-cli/logs/qa/
└── 20260312-150000-PLAN-001-search.md
```

---

## 📋 project type별 directory Structure template

### Web Fullstack

```
projects/{name}/
├── .project-meta.json
├── planning/
│   ├── tickets/
│   ├── specs/
│   │   ├── backend/
│   │   └── frontend/
│   └── test-cases/
│       ├── backend/
│       └── frontend/
├── src/
│   ├── backend/
│   │   ├── src/
│   │   ├── tests/
│   │   └── Requirements.txt (or package.json)
│   └── frontend/
│       ├── src/
│       ├── public/
│       └── package.json
├── logs/
└── README.md
```

### Web MVC

```
projects/{name}/
├── .project-meta.json
├── planning/
│   ├── tickets/
│   ├── specs/
│   │   ├── endpoints/
│   │   └── templates/
│   └── test-cases/
├── src/
│   ├── manage.py (Django) or build.gradle (Spring)
│   ├── apps/ or controllers/
│   ├── templates/ or views/
│   ├── static/
│   └── tests/
├── logs/
└── README.md
```

### CLI Tool

```
projects/{name}/
├── .project-meta.json
├── planning/
│   ├── tickets/
│   ├── specs/
│   └── test-cases/
├── src/
│   ├── cmd/ (Go) or cli/ (Python)
│   ├── internal/ (Go) or lib/ (Python)
│   ├── go.mod (Go) or setup.py (Python)
│   └── main.go or __main__.py
├── logs/
└── README.md
```

### Desktop App

```
projects/{name}/
├── .project-meta.json
├── planning/
│   ├── tickets/
│   ├── specs/
│   │   ├── screens/
│   │   ├── state/
│   │   └── ipc/
│   └── test-cases/
│       ├── unit/
│       ├── integration/
│       └── e2e/
├── src/
│   ├── src-tauri/ (Tauri) or main/ (Electron)
│   ├── src/ (Frontend)
│   └── public/
├── logs/
└── README.md
```

### Library

```
projects/{name}/
├── .project-meta.json
├── planning/
│   ├── tickets/
│   ├── specs/
│   │   ├── api/
│   │   └── examples/
│   └── test-cases/
├── src/
│   ├── src/ or lib/
│   ├── tests/
│   ├── package.json (npm) or setup.py (pip)
│   └── README.md
├── logs/
└── README.md
```

### Data Pipeline

```
projects/{name}/
├── .project-meta.json
├── planning/
│   ├── tickets/
│   ├── specs/
│   │   ├── dags/
│   │   ├── transforms/
│   │   └── schedules/
│   └── test-cases/
├── src/
│   ├── dags/
│   ├── plugins/
│   ├── tests/
│   └── Requirements.txt
├── logs/
└── README.md
```

---

## 🔄 multiple project 관리

### project 전환

```bash
# 프로젝트 목록 확인
ls projects/

# 특정 프로젝트로 전환
bash scripts/switch-project.sh file-search-cli
```

**switch-project.sh**가 perform:
1. `.project-config.json` update (`current_project` change)
2. 해당 project의 `.project-meta.json` 읽기
3. 환경 configuration (required 시)

### project별 독립 task

```bash
# 프로젝트 A 작업
cd projects/my-todo-app
bash ../../scripts/run-agent.sh coding --ticket PLAN-001

# 프로젝트 B 작업 (별도 터미널)
cd projects/file-search-cli
bash ../../scripts/run-agent.sh coding --ticket PLAN-001
```

---

## 🛠️ agent template Structure

### PM Agent template yes시

**`.agents/pm/templates/cli-tool.md`**:

```markdown
# PM Agent - CLI Tool 템플릿

## 산출물 Structure

### 1. 커맨드 명세서
- 위치: `projects/{project_name}/planning/specs/PLAN-XXX-command-spec.md`
- 내용:
  - 커맨드 이름
  - 서브커맨드 (있는 경우)
  - 플래그/옵션
  - 입력 파라미터
  - 출력 형식
  - 예시

### 2. 테스트 케이스
- 위치: `projects/{project_name}/planning/test-cases/PLAN-XXX-tests.md`
- 내용:
  - 정상 케이스
  - 예외 케이스
  - 엣지 케이스
  - 통합 테스트 시나리오

## 템플릿

(생략 - 실제 템플릿 내용)
```

### Coding Agent template yes시

**`.agents/coding/templates/cli-tool.md`**:

```markdown
# Coding Agent - CLI Tool 템플릿

## 작업 순서

1. `.project-config.json` 읽기
2. `projects/{current_project}/.project-meta.json` 읽기
3. `projects/{current_project}/planning/specs/PLAN-XXX-command-spec.md` 읽기
4. 코딩 룰 로드 (`.rules/_verified/` 또는 `_cache`)
5. 코드 생성:
   - Go Cobra: `cmd/`, `internal/`
   - Python Click: `cli/`, `lib/`
   - Rust clap: `src/cli.rs`, `src/lib.rs`
6. 로그 작성: `projects/{current_project}/logs/coding/`

## 프레임워크별 Structure

(생략 - 실제 템플릿 내용)
```

---

---

## ✅ change 요약

### remove됨
- ❌ 고정된 directory Structure (be-/fe- 등)
- ❌ Tech Stack 종속적인 Structure

### add됨
- ✅ `projects/{name}/` (project별 격리)
- ✅ `.project-meta.json` (project 메타data)
- ✅ `planning/` (project별 기획 documentation)
- ✅ type별 동적 `specs/` Structure
- ✅ `coding`, `qa` 통합 agent
- ✅ project 전환 feature (`switch-project.sh`)

### 유지됨
- ✅ `.agents/` Structure (template add)
- ✅ `.rules/` Structure (_verified, _cache)
- ✅ `scripts/` (partial script add)
- ✅ Git branch 워크플로우

---

**version**: v0.0.2
**최종 검토**: 2026-03-12
