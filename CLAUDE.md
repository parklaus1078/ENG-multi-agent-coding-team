# Multi-Agent Coding Team - Development Agent

> **role**: Multi-Agent Coding Team system 자체를 development하고 improvement하는 agent
>
> **range**: system 아키텍처, agent improvement, API development, web dashboard, documentation
>
> **version**: v0.0.3

---

## 🎯 미션

이 system은 **Tech Stack Agnostic 멀티 agent development 플랫폼**입니다.
user가 어떤 project든 automation된 pipeline으로 can development 있도록 support.

---

## 📂 project Structure 이해

### 핵심 directory

```
KR-multi-agent-coding-team/
├── CLAUDE.md                    # ← 이 파일 (시스템 개발 가이드)
├── README.md                    # 사용자 문서
├── docs/                        # 아키텍처 문서
├── logs-agent_dev/              # 수정사항 로그 문서
└── team/                        # ← 핵심 작업 디렉토리
    ├── .agents/                 # 5개 에이전트 정의
    │   ├── pm/CLAUDE.md
    │   ├── coding/CLAUDE.md
    │   ├── qa/CLAUDE.md
    │   ├── project-planner/CLAUDE.md
    │   └── stack-initializer/CLAUDE.md
    ├── .skills/                 # 8개 재사용 가능 스킬
    │   ├── validate-spec/
    │   ├── commit/
    │   ├── review-pr/
    │   ├── refactor-code/
    │   ├── test-runner/
    │   ├── deploy/
    │   ├── benchmark/
    │   └── docs-generator/
    ├── .config/                 # 시스템 설정
    │   ├── git-workflow.json
    │   ├── auto-responses.json
    │   └── log-schema.json
    ├── .memory/                 # 학습 시스템
    │   ├── patterns.json
    │   ├── commit-history.json
    │   └── review-history.json
    ├── api/                     # FastAPI REST API (Phase 4)
    │   ├── main.py
    │   ├── routers/
    │   ├── services/
    │   └── models/
    ├── web/                     # 웹 대시보드 (Phase 4)
    │   ├── index.html
    │   └── static/
    ├── scripts/                 # CLI 도구
    │   ├── run-agent.sh
    │   ├── run-skill.sh
    │   └── auto_pipeline.py
    └── projects/                # 사용자 프로젝트 작업 공간
        └── {project-name}/
```

---

## 🏗️ 아키텍처 원칙

### 1. Agent vs Skill 분리

**Agent (복잡한 의사결정)**
- PM, Coding, QA, Project Planner, Stack Initializer
- 컨text 이해 required
- CLAUDE.md로 정의
- status 유지 (session)

**Skill (반복 task automation)**
- validate-spec, commit, review-pr, refactor-code 등
- Stateless (status none)
- 재available
- skill.md로 정의

### 2. Tech Stack Agnostic

**never 하드코딩 금지:**
```python
# ❌ 나쁜 예
if language == "python":
    run_pytest()
elif language == "go":
    run_go_test()

# ✅ 좋은 예
framework = meta.get("framework")
test_command = get_test_command(framework)  # 동적 감지
```

**project 메타data 활용:**
```json
{
  "project_type": "web-fullstack",
  "language": "python",
  "framework": "fastapi"
}
```

### 3. project 격리

- system code: `KR-multi-agent-coding-team/`
- user project: `team/projects/{name}/` (독립 Git 리포)
- **never 섞이면 Plan 됨**

---

## 🔧 development 시 required confirmation사항

### task 전 체크리스트

1. **currently version confirmation**
   ```bash
   grep "version" README.md
   # 현재: v0.0.3
   ```

2. **change range 파악**
   - Agent fix? → `.agents/{agent}/CLAUDE.md`
   - Skill add? → `.skills/{skill}/skill.md`
   - API endpoint? → `api/routers/`
   - web UI? → `web/`

3. **test 환경**
   ```bash
   cd team
   # API 테스트
   uvicorn api.main:app --reload --port 8000

   # CLI 테스트
   bash scripts/run-agent.sh pm --ticket PLAN-001
   ```

4. **마이그레이션 체크**
   - KR version fix → ENG version도 fix required
   - A_coding-team도 sync required한지 confirmation

---

## 📝 코딩 rule

**important**: 상세한 코딩 rule은 별도 documentation reference

- **all 코딩 rule**: `CODING-RULES.md` (이 file과 같은 location)
  - Python (FastAPI, Services)
  - Shell Scripts
  - JavaScript (Web Dashboard)
  - DRY, SRP, KISS, YAGNI 등 원칙
  - 선언적 코딩 우선
  - error 핸들링 pattern

- **범용 원칙**: `team/.rules/general-coding-rules.md`
- **Backend 상세**: `team/.rules/_verified/web-fullstack/backend-fastapi-python.md`
- **Frontend 상세**: `team/.rules/_verified/web-fullstack/frontend-nextjs-typescript.md`

### 핵심 원칙만 요약

1. **DRY**: 중복 code를 function로 추출
2. **SRP**: function/class는 한 가지 책임만
3. **명시적 type 힌팅** (Python)
4. **선언적 코딩 우선** (SQLAlchemy, JavaScript)
5. **function size 제한**: 50줄 초과 시 분리
6. **error 핸들링**: 모든 yes외 명시적 process
7. **logging**: `print()` 금지, `logger` 사용

---

## 🎨 Phase별 development 전략

### Phase 1-2: default 멀티 agent system ✅ completed
- 5개 agent
- Git branch auto 관리
- Rate limit 추적

### Phase 3: Skills 아키텍처 ✅ completed
- 8개 재available 스킬
- Agent-Skill 분리
- Memory system

### Phase 4: web 플랫폼 ✅ completed
- FastAPI REST API (25+ endpoint)
- web dashboard
- Discord 연동
- GitHub Webhook

### Phase 5: 향후 Plan (reference용)
- Database 연동 (PostgreSQL)
- Authentication (JWT)
- WebSocket (실time update)
- Docker/Kubernetes deployment

---

## 🚨 important 제약사항

### never 하면 Plan 되는 것

1. **하드코딩된 언어/framework 가정**
   ```python
   # ❌ 절대 금지
   if framework == "fastapi":
       # FastAPI 전용 코드
   ```

2. **project directory 오염**
   ```bash
   # ❌ 절대 금지
   cp system-file.md projects/user-project/
   ```

3. **agent CLAUDE.md 무단 fix**
   - PM, Coding, QA 등의 CLAUDE.md는 신중하게 fix
   - test required

4. **하up 호환성 깨기**
   - 기존 ticket/specification 형식 유지
   - API endpoint change 시 version 관리

### 반드시 해야 하는 것

1. **error 핸들링**
   ```python
   try:
       result = execute_agent()
   except FileNotFoundError:
       logger.error("Ticket file not found")
       return {"error": "Ticket not found"}
   except Exception as e:
       logger.error(f"Unexpected error: {e}")
       return {"error": str(e)}
   ```

2. **logging**
   ```python
   import logging
   logger = logging.getLogger(__name__)

   logger.info(f"Starting agent: {agent_name}")
   logger.error(f"Failed to execute: {error}")
   ```

3. **type 힌트 (Python)**
   ```python
   def run_pipeline(
       ticket: str,
       project: str,
       resume: bool = False
   ) -> PipelineStatusResponse:
   ```

4. **documentation**
   - file에 대한 fluctuation(create/fix/delete) 사항이 있을 때, 해당 file이 속한 directory 내에 `README.md` file이 있는 directory라면 해당 README.md file을 꼭 fix해주어야 함.
   - feature fluctuation(create/fix/delete) 사항 생길 시, 무조건 `README.md` fix
   - 새 API endpoint → `api/README.md`에 add
   - 새 스킬 → `docs/skills-guide.md`에 add
   - 주요 change사항 → `logs-agent_dev/`에 기록
     - 언제나 file을 create/fix/delete한 내역이 있다면 `logs-agent_dev/{today's date}-{task name}.md` pattern을 따르는 마크다운 file에 관련 content 작성
     - 로그를 작성할 때는 육하원칙에 따라 누가 언제 무엇을 어떻게 왜 fix했는지를 꼭 기록할 것
       - 누가: 누가 create/fix/delete하였는지
       - 언제: 언제 create/fix/delete하였는지
       - 어디서: 제외
       - 무엇: 어떤 file들을 create/fix/delete하였는지
       - 왜: 왜 create/fix/delete하였는지
     - 해당 directory에 작성되는 로그들은 
       1. 이 multi agent coding team project의 developer가 development 히스토리를 추적하기 용이하게 하기 up함.
       2. 이 multi agent coding team project development Agent 가 development 히스토리를 추적하기 용이하게 하고, 컨text 파악을 용이하게 하기 up함.

---

## 🔍 debugging guide

### API debugging

```bash
# 1. 로그 확인
tail -f logs/api.log

# 2. Swagger UI로 테스트
# http://localhost:8000/api/docs

# 3. curl로 직접 테스트
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{"ticket": "PLAN-001", "project": "test"}'
```

### Agent debugging

```bash
# 1. 직접 실행
cd team/.agents/pm
claude

# 2. 스크립트로 실행 (verbose)
# 모든 에이전트 동일한 방식
bash -x scripts/run-agent.sh pm --ticket PLAN-001
bash -x scripts/run-agent.sh coding --ticket PLAN-001
bash -x scripts/run-agent.sh qa --ticket PLAN-001

# Project Planner는 2가지 방식
bash -x scripts/run-agent.sh project-planner --project "프로젝트 설명"
bash -x scripts/run-agent.sh project-planner --req Requirements.md

# 3. 로그 확인
cat projects/{project}/logs/pm/*.md
```

### Skill debugging

```bash
# 1. 직접 실행
bash scripts/run-skill.sh commit PLAN-001

# 2. Python으로 직접 호출
python .skills/commit/commit-message-generator.py
```

---

## 📊 test 전략

### 1. API test

```bash
# 헬스 체크
curl http://localhost:8000/api/health

# 프로젝트 목록
curl http://localhost:8000/api/projects/list

# 티켓 목록
curl http://localhost:8000/api/projects/bill-organizer/tickets
```

### 2. Agent test

```bash
# Project Planner (파일 입력)
bash scripts/run-agent.sh project-planner --req test-Requirements.md

# PM Agent
bash scripts/run-agent.sh pm --ticket PLAN-001

# 결과 확인
ls projects/{project}/planning/specs/
ls projects/{project}/planning/test-cases/
```

### 3. Skill test

```bash
# validate-spec
bash scripts/run-skill.sh validate-spec PLAN-001

# commit
bash scripts/run-skill.sh commit PLAN-001
```

### 4. web dashboard test

```
1. 브라우저: http://localhost:8000
2. 프로젝트 선택
3. 티켓 목록 확인
4. 파이프라인 실행
5. Discord 알림 확인
```

---

## 🔄 마이그레이션 체크리스트

새 feature add 시:

- [ ] KR version에 implementation
- [ ] ENG version에 마이그레이션 (번역)
- [ ] A_coding-team에 required하면 적용
- [ ] README.md update (KR + ENG)
- [ ] API documentation update (`api/README.md`)
- [ ] change 로그 작성 (`logs-agent_dev/`)

---

## 📚 주요 file reference
**핵심 원칙**: user의 request 사항에 따라 fix의 여지가 exists. 별도의 관련 지시가 없을 시에는 reference하고, 별도의 지사가 있을 때에는 fix 가능

### 설계 documentation
- `docs/architecture-final.md` - 최종 아키텍처
- `docs/supported-tech-stacks.md` - support 스택
- `docs/phase4-complete.md` - Phase 4 completed 보고서

### agent guide
- `team/.agents/project-planner/CALUDE.md` - Project Planner Agent(project 파악 and all ticket create)
- `team/.agents/pm/CLAUDE.md` - PM Agent(각 ticket 별 세부 specification, Requirements, test case 정의)
- `team/.agents/coding/CLAUDE.md` - Coding Agent(specification and Requirements에 따라 코딩)
- `team/.agents/qa/CLAUDE.md` - QA Agent(test case에 따라 Coding Agent가 implementation한 content을 test하는 test code를 작성)

### 스킬 guide
- `team/docs/skills-guide.md` - Skills 사용 guide
- `team/.skills/*/skill.md` - individual 스킬 documentation

### API documentation
- `team/api/README.md` - REST API all documentation

---

## 🎯 task 우선ranking

### P0 (immediately)
- agent CLAUDE.md improvement
- bug fix
- 보Plan issue

### P1 (important)
- 새 스킬 add
- API endpoint improvement
- web dashboard feature add

### P2 (later)
- Database 연동
- Authentication
- performance optimization

---

## 💡 development 팁

### 1. 점진적 development
```
1. KR 버전에서 먼저 구현
2. 테스트
3. ENG 버전 마이그레이션
4. 문서화
```

### 2. agent fix 시
```
1. .agents/{agent}/CLAUDE.md 백업
2. 수정
3. 테스트 (실제 티켓으로)
4. 문제 없으면 커밋
```

### 3. API development 시
```
1. models/ (Pydantic) 먼저 정의
2. services/ 비즈니스 로직
3. routers/ 엔드포인트
4. main.py에 등록
5. Swagger UI 확인
```

### 4. web dashboard development 시
```
1. HTML Structure 먼저
2. CSS 스타일
3. JavaScript 로직
4. API 연동
5. 에러 핸들링
```

---

## 🔐 보Plan 고려사항

### API Keys
- `.env` file에만 save
- Git에 never commit Plan 됨 (`.gitignore`)
- `.env.example`은 template만

### GitHub Webhook
- HMAC-SHA256 서명 validation required
- `api/routers/webhooks.py` reference

### Discord Webhook
- URL 노출 note
- 환경 variable로만 관리

---

## 📖 learning 자료

### FastAPI
- 공식 documentation: https://fastapi.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/

### Discord Webhooks
- 공식 documentation: https://discord.com/developers/docs/resources/webhook

### Claude Code
- documentation: https://docs.claude.ai/claude-code
- CLAUDE.md guide: 각 agent folder reference

---

## ✅ task completed 기준

1. **code quality**
   - [ ] type 힌트 add
   - [ ] Docstring 작성
   - [ ] error 핸들링 implementation
   - [ ] logging add

2. **test**
   - [ ] local에서 action confirmation
   - [ ] API endpoint test
   - [ ] web dashboard confirmation

3. **documentation**
   - [ ] README update
   - [ ] API documentation update
   - [ ] change 로그 작성

4. **마이그레이션**
   - [ ] ENG version sync
   - [ ] required 시 A_coding-team sync

---

## 🚀 start하기

```bash
# 1. 프로젝트 루트로 이동
cd /Users/geunwoopark/Desktop/multi_agent_coding_team/KR-multi-agent-coding-team

# 2. 현재 상태 확인
git status

# 3. team 디렉토리로 이동
cd team

# 4. 에이전트 실행 테스트
# 방법 1: 터미널 입력
bash scripts/run-agent.sh project-planner --project "테스트 TODO 앱"

# 방법 2: 파일 입력
cat > Requirements.md <<EOF
# 테스트 프로젝트
간단한 TODO 앱
EOF
bash scripts/run-agent.sh project-planner --req Requirements.md

# PM Agent (티켓 번호만으로 자동 감지)
bash scripts/run-agent.sh pm --ticket PLAN-001

# 5. API 서버 실행 (테스트)
cd team
uvicorn api.main:app --reload --port 8000

# 4. 새 터미널에서 개발 시작
cd team
# 작업 시작...
```

---

**이 file은 Multi-Agent Coding Team system을 development하는 agent를 up한 is guide.**
**user용 guide는 README.md를 please reference.**
