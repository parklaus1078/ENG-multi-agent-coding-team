2.3# Multi-Agent Coding Team improvement Plan
## Thariq의 Skills guide 기반

> **Date**: 2026-03-19
> **reference**: [Lessons from Building Claude Code - How We Use Skills](https://x.com/trq212/status/2033949937936085378)

---

## 📊 currently status 진단

### ✅ 강점
- **5개 통합 agent**: stack-initializer, project-planner, pm, coding, qa
- **Tech-stack 독립성**: project type별 동적 directory Structure
- **auto pipeline**: 무인 execute 가능한 Python 오케스트레이션
- **session 관리**: Claude CLI session resume로 반복 fix 가능
- **Rate Limit 추적**: API 사용량 사전 모니터링
- **Git automation**: branch create, commit template

### ❌ 주요 problem점

#### 1. **워크플로우 정확성 부족**
- **증상**: agent가 ticket range를 벗어나 불required한 feature add
- **영향**: API call 낭비, code review 부담 increase
- **yes시**: "login" ticket에 OAuth, password 재configuration까지 implementation

#### 2. **Self-learning 메커니즘 부재**
- **currently**: 로그는 작성하지만 재사용 Plan 됨 (`projects/{name}/logs/`)
- **problem**: 같은 실수를 반복함 (project path mistake, range zoom in 등)
- **Thariq 교훈**: "storing data within them... the next time you run it, Claude reads its own history"

#### 3. **컨text 효율성 저하**
- **currently**: PM Agent CLAUDE.md = 833줄, Coding = 428줄
- **problem**: 매번 all load → token 낭비
- **Thariq 교훈**: "Progressive Disclosure - tell Claude what files are in your skill"

#### 4. **Gotchas section 부재**
- **currently**: 47개의 "금지 사항" 산재 (부정형 rule)
- **problem**: "왜 failure하는지" pattern 미기록
- **Thariq 교훈**: "The highest-signal content in any skill is the Gotchas section"

#### 5. **validation 후크 none**
- **currently**: Auto-pipeline이 quality 게이트 없이 execute
- **problem**: 잘못된 specification → 잘못된 code → API call 낭비
- **Thariq 교훈**: "blocks rm -rf, DROP TABLE, force-push via PreToolUse matcher"

---

## 🎯 improvement load맵

### **Phase 1: Quick Wins (1-2일)**
> 즉각적인 정확성 improvement, 아키텍처 change none

#### 1.1 금지사항 → Gotchas file 전환
**난이도**: 🟢 Low
**영향**: 🔴 High - range 이탈 40% decrease

**create할 file**:
```
team/.agents/pm/gotchas.md
team/.agents/coding/gotchas.md
team/.agents/qa/gotchas.md
team/.agents/project-planner/gotchas.md
```

**Structure** (Thariq pattern):
```markdown
# PM Agent Gotchas

## 1. 범위 확대 패턴 (Scope Creep)
❌ **증상**: 티켓에 없는 기능 추가
🔍 **원인**: "user auth" → OAuth, 이메일 인증까지 해석
✅ **해결**: 티켓 Acceptance Criteria 먼저 확인
📝 **실패 사례**: PLAN-001이 로그인/로그아웃만 요청 → PM이 비밀번호 재설정까지 추가
🎯 **올바른 접근**: 티켓 항목만 구현, 추가는 "Out of Scope"에 기록

## 2. 잘못된 디렉토리 생성
❌ **증상**: team/.agents/ 에 명세서 생성
🔍 **원인**: .project-config.json 체크 생략
🚨 **탐지**: 경로에 "team/.agents" 또는 "team/.rules" 포함
✅ **해결**: mkdir 전에 항상 .project-config.json → current_project 읽기

## 3. HTML 와이어프레임에 외부 라이브러리
❌ **증상**: Tailwind, React 사용
🔍 **원인**: 프로덕션 코드 작성으로 착각
✅ **해결**: 바닐라 JS만, Structure만 표현
📝 **검증**: grep -E "tailwind|react|vue" 으로 체크
```

**task 순서**:
1. 모든 CLAUDE.md의 "금지 사항" 추출
2. 각 금지사항을 Gotcha로 변환 (failure pattern + 근본 원인 + 탐지법 + solution책)
3. 각 CLAUDE.md를 ~200줄 zoom out

**기대 효과**:
- agent당 token 사용량: **-15%**
- range 이탈 error: **-40%**
- 엣지 케이스 process 명확성: **+60%**

---

#### 1.2 Progressive Disclosure refactoring
**난이도**: 🟡 Medium
**영향**: 🔴 High - 컨text 사용량 30% decrease

**새 Structure**:
```
team/.agents/pm/
├── CLAUDE.md (100줄 - 핵심 역할 + 파일 인벤토리)
├── gotchas.md (1.1에서 생성)
├── workflows/
│   ├── web-fullstack.md
│   ├── cli-tool.md
│   └── desktop-app.md
└── templates/ (기존)
```

**새 CLAUDE.md Structure** (~100줄):
```markdown
# PM Agent

티켓을 Structure화된 명세서로 변환하는 에이전트.

## 📂 파일 Structure
- `gotchas.md` - **먼저 읽기**. 일반적인 실패 패턴과 회피법
- `workflows/{project_type}.md` - .project-meta.json의 project_type 기반으로 읽기
- `templates/{project_type}.md` - 명세서 생성 템플릿

## 🔨 핵심 프로세스
1. gotchas.md 읽기
2. Rate limit 체크: `bash scripts/rate-limit-check.sh pm`
3. .project-config.json 읽기 → current_project
4. .project-meta.json 읽기 → project_type
5. workflows/{project_type}.md에서 프로젝트별 단계 로드
6. templates/{project_type}.md로 명세서 생성

## 📤 산출물
- API 명세, UI 명세, 테스트 케이스: `projects/{project}/planning/specs/`
- 로그: `projects/{project}/logs/pm/`

상세 지침은 workflows/ 참조.
```

**create할 file**:
- `team/.agents/pm/workflows/web-fullstack.md` (currently CLAUDE.md에서 추출)
- `team/.agents/pm/workflows/cli-tool.md`
- `team/.agents/coding/workflows/web-fullstack.md`
- `team/.agents/qa/workflows/web-fullstack.md`

**기대 효과**:
- 초기 컨text load: **-30%**
- required한 워크플로우만 온디맨드 읽기
- 새 project type add 용이 (워크플로우 file만 add)

---

#### 1.3 Auto-Response rule을 data화
**난이도**: 🟢 Low
**영향**: 🟡 Medium - 튜닝 용이, code change 불required

**create할 file**: `team/.config/auto-responses.json`

```json
{
  "pm": {
    "patterns": [
      {
        "trigger": "추가.*기능.*할까요",
        "response": "no, 티켓 범위 내에서만 Progress해주세요",
        "reason": "scope_creep_prevention"
      },
      {
        "trigger": "변경.*할까요",
        "response": "no, 현재 명세대로 Progress해주세요",
        "reason": "spec_compliance"
      },
      {
        "trigger": "이 부분.*애매",
        "response": "티켓의 Acceptance Criteria를 기반으로 합리적으로 판단하고 로그에 기록해주세요",
        "reason": "ambiguity_handling"
      }
    ]
  },
  "coding": {
    "patterns": [
      {
        "trigger": "더 나은 패턴",
        "response": "코딩 룰에 명시된 패턴을 우선 사용하세요. 대Plan이 명백히 우수하면 로그에 근거를 작성하세요",
        "reason": "architecture_consistency"
      }
    ]
  }
}
```

**fix할 file**:
- `team/scripts/auto_pipeline.py` (24-29줄, 140-145줄)

**기대 효과**:
- code deployment 없이 response 튜닝
- 로그에서 pattern learning 가능 (Phase 2)
- response 전략 version 관리

---

### **Phase 2: 핵심 improvement (1주)**
> Self-learning 메커니즘 and validation 후크

#### 2.1 Structure화된 의사결정 로그
**난이도**: 🟡 Medium
**영향**: 🔴 High - 실수에서 learning 가능

**currently problem**: 로그는 작성되지만 analytics Plan 됨

**새 로그 Structure**:
```markdown
# PM Log: User Authentication

## 메타데이터
- Agent: PM
- Ticket: PLAN-001
- Timestamp: 2026-03-19T10:30:00Z
- Decision Count: 3

## 의사결정

### Decision 1: OAuth 제외
- **컨텍스트**: 티켓에 "login" 명시, 방법 미지정
- **옵션**: [Email/Password만, OAuth, 둘 다]
- **선택**: Email/Password만
- **이유**: Acceptance Criteria에 email/password만 명시
- **위험도**: Low (티켓에 명확함)
- **신뢰도**: 95%

### Decision 2: 비밀번호 재설정 엔드포인트 포함 여부
- **컨텍스트**: 티켓에 없지만 일반적인 패턴
- **옵션**: [포함, 제외, 사용자에게 질문]
- **선택**: 제외
- **이유**: Gotcha #1 적용 (범위 확대 방지)
- **위험도**: Medium (사용자가 기대할 수 있음)
- **신뢰도**: 70%

## 적용한 Gotchas
- ✅ Gotcha #1: 범위 확대 - 티켓 확인, 비밀번호 재설정 제외
- ✅ Gotcha #5: 잘못된 디렉토리 - .project-config.json 먼저 읽기

## 관찰된 패턴
- 사용자가 "auth"라고 하면 → 로그인/로그아웃만 의미할 가능성 높음
- "forgot password" 언급 없음 → 비밀번호 재설정 제외
```

**create할 file**:
```
team/.config/log-schema.json (필수 의사결정 필드 정의)
team/scripts/analyze-logs.py (로그에서 패턴 추출)
```

**통합**:
- 모든 agent CLAUDE.md를 Structure화된 로그 형식으로 update
- 주간으로 `analyze-logs.py` execute:
  - 가장 흔한 의사결정 pattern 식별
  - failure한 고up험 결정 발견
  - 새 Gotcha 후보 발견

**기대 효과**:
- 회고적 learning: **+80%**
- 새 Gotcha 발견률: 초기에 주당 **2-3개**
- 의사결정 quality 추적 (신뢰도 vs 실제 result)

---

#### 2.2 validation 후크 (Skill 기반)
**난이도**: 🟡 Medium
**영향**: 🔴 High - 비용 높은 코딩 stage 전에 error 포착

**create할 Skills**:
```
team/.skills/
├── validate-spec/
│   ├── skill.md
│   ├── rules.json
│   └── examples/
└── validate-code/
    ├── skill.md
    └── rules.json
```

**`validate-spec/skill.md`**:
```markdown
# Spec Validation Skill

PM Agent 결과를 Coding Agent로 전달하기 전에 검증.

## 트리거
- Auto-pipeline: PM agent Complete 후
- 수동: `bash scripts/run-skill.sh validate-spec PLAN-001`

## 검사 항목

### 1. 완전성
- [ ] API 명세에 티켓의 모든 CRUD 엔드포인트 포함
- [ ] UI 명세에 Acceptance Criteria의 모든 유저 플로우 포함
- [ ] 모든 엣지 케이스에 대한 테스트 케이스 존재
- [ ] 와이어프레임 HTML 존재 (프로젝트 타입이 필요로 하는 경우)

### 2. 범위 준수
- [ ] 티켓 Acceptance Criteria 외 기능 없음
- [ ] Out-of-Scope 섹션에 제외 항목 나열
- [ ] .project-meta.json의 tech stack 변경 없음

### 3. 품질 게이트
- [ ] API 엔드포인트가 REST 규약 준수
- [ ] 예시에 하드코딩된 비밀번호 없음
- [ ] 에러 응답 문서화됨
- [ ] 입력 검증 규칙 명시됨

## 출력
- Pass/Fail 상태
- 발견된 이슈 목록
- 사소한 이슈에 대한 자동 수정 제Plan
```

**`validate-spec/rules.json`**:
```json
{
  "rules": [
    {
      "id": "no-scope-creep",
      "check": "명세 기능을 티켓 Acceptance Criteria와 비교",
      "severity": "error",
      "auto_fix": false
    },
    {
      "id": "rest-conventions",
      "check": "POST=생성, GET=읽기, PUT=수정, DELETE=삭제",
      "severity": "warning",
      "auto_fix": false
    },
    {
      "id": "no-hardcoded-secrets",
      "check": "명세에서 API_KEY, PASSWORD, SECRET 패턴 검색",
      "severity": "error",
      "auto_fix": true,
      "fix": "환경 변수 참조로 대체"
    }
  ]
}
```

**Auto-Pipeline 통합**:
```python
# auto_pipeline.py의 PM agent 후
result = self.run_agent("pm", ticket_content, ticket_num)

# 검증 skill 실행
validation = self.run_skill("validate-spec", ticket_num)
if not validation["passed"]:
    print(f"⚠️  명세 검증 실패: {validation['issues']}")
    # 이슈를 컨텍스트로 PM agent 재시도
    self.run_agent("pm", f"다음 이슈 수정: {validation['issues']}", ticket_num)
```

**기대 효과**:
- specification quality error 포착: **+90%**
- 낭비된 코딩 반복: **-60%**
- ticket당 절약된 API call: **~3-5회** (재task none)

---

#### 2.3 메모리 system (learning된 pattern)
**난이도**: 🟡 Medium
**영향**: 🔴 High - past 실수에서 learning

**file Structure**:
```
team/.memory/
├── patterns.json (학습된 의사결정 패턴)
├── failures.json (카탈로그화된 실패)
└── successes.json (검증된 모범 사례)
```

**`patterns.json`**:
```json
{
  "pm": {
    "pattern_001": {
      "trigger": "티켓에 'auth' 언급, OAuth 없음",
      "learned_decision": "OAuth 제외, Out-of-Scope에 기록",
      "confidence": 0.95,
      "learned_from": ["PLAN-001", "PLAN-023", "PLAN-047"],
      "success_rate": "47/50",
      "last_updated": "2026-03-15"
    },
    "pattern_002": {
      "trigger": "폼 제출 UI 명세",
      "learned_decision": "항상 로딩 상태와 에러 표시 포함",
      "confidence": 0.88,
      "learned_from": ["PLAN-005", "PLAN-012"],
      "success_rate": "28/32"
    }
  }
}
```

**`failures.json`**:
```json
{
  "failure_001": {
    "ticket": "PLAN-007",
    "agent": "coding",
    "symptom": "잘못된 디렉토리에 코드 생성",
    "root_cause": ".project-config.json 체크 생략",
    "detection": "수동 리뷰",
    "fix_applied": "gotchas.md #3에 추가",
    "prevented_count": 12
  }
}
```

**learning script**: `team/scripts/learn-from-logs.py`

**feature**:
1. recently 7일 로그 파싱
2. 의사결정 + result 추출 (git commit, test result에서)
3. >80% success률 pattern → `patterns.json`에 add
4. 반복 failure 식별 → `failures.json` → 새 Gotcha create
5. success pattern 기반으로 auto-responses.json update

**통합**:
```markdown
## 메모리 파일
- `.memory/patterns.json` - 학습된 모범 사례 적용
- `.memory/failures.json` - 알려진 실패 모드 회피
```

**기대 효과**:
- 반복 실수: **-70%**
- 의사결정 quality (정확도): **+25%**
- 새 project type 숙련 time: **-50%**

---

#### 2.4 Gotcha auto 발견
**난이도**: 🟡 Medium
**영향**: 🟡 Medium - Gotcha 지속 improvement

**script**: `team/scripts/discover-gotchas.py`

**알고리즘**:
1. 모든 failure 로그 파싱 (git revert, failure한 test, manual fix)
2. common pattern 추출:
   - error message
   - 관련 file path
   - failure 전 agent 의사결정
3. 유사 failure 클러스터링
4. Gotcha 초Plan create:
   ```markdown
   ## [초Plan] 잘못된 테스트 파일 위치
   **증상**: src/에 테스트 생성, tests/가 아닌
   **빈도**: 3회 (PLAN-012, PLAN-019, PLAN-024)
   **원인**: QA agent가 프로젝트 Structure 오독
   **해결**: 테스트 디렉토리 규약은 항상 .project-meta.json 확인
   ```
5. `gotchas.md`에 add 전 사람 검토

**trigger**:
- cron으로 주간 execute
- git revert 후 execute
- 온디맨드: `bash scripts/discover-gotchas.py --since 7d`

**기대 효과**:
- 새 Gotcha 발견: 주당 **1-2개**
- 엣지 케이스 coverage: 3개월 내 **+40%**
- Gotcha manual 작성 decrease

---

### **Phase 3: advanced feature (2주+)**
> 하이브리드 agent-skill 아키텍처, advanced learning

#### 3.1 Skill 기반 아키텍처 (점진적 마이그레이션)
**난이도**: 🔴 High
**영향**: 🔴 High - Anthropic의 최신 Skills pattern

**전략**: 하이브리드 - agent 유지, Skills 점진 add

**새 Structure**:
```
team/
├── .agents/ (기존 - 당분간 유지)
├── .skills/ (신규)
│   ├── commit/
│   │   ├── skill.md
│   │   ├── commit-message-generator.py
│   │   └── gotchas.md
│   ├── review-pr/
│   │   ├── skill.md
│   │   ├── review-checklist.json
│   │   └── auto-fix-rules.json
│   ├── validate-spec/ (Phase 2.2에서)
│   └── refactor-code/
│       ├── skill.md
│       └── patterns.json
```

**마이그레이션 path**:
1. **1주차**: 작고 독립적인 task을 Skills로 전환
   - `commit` skill (하드코딩 commit template 대체)
   - `validate-spec` skill (Phase 2.2에서)
2. **2주차**: 누락된 part을 up한 새 Skills add
   - `review-pr` skill (auto PR review)
   - `refactor-code` skill (code improvement 제Plan)
3. **3주차**: agent가 Skills 사용하도록 refactoring
   - PM agent가 create 후 `validate-spec` skill call
   - Coding agent가 commit 전 `refactor-code` skill call
4. **2-3개월**: agent feature을 Skills로 점진 마이그레이션

**yes시 Skill**: `commit/skill.md`
```markdown
# Commit Skill

프로젝트 규약에 따라 시맨틱 커밋 생성.

## 트리거
- 수동: 코드 생성 후 사용자가 "commit" 입력
- Auto-pipeline: coding/qa agents Complete 후

## 프로세스
1. git diff 읽기
2. 변경 파일 분석
3. 커밋 메시지 생성:
   - Prefix: feat/fix/test/docs/refactor
   - Scope: (ticket-number)
   - Subject: 명령형, <70자
   - Body: 변경 이유
   - Footer: Co-Authored-By, Closes #
4. 승인을 위해 메시지 표시
5. 커밋 실행

## 메모리
- `.memory/commit-history.json` - 일관성을 위한 과거 커밋 메시지
- 프로젝트별 어휘 학습

## 예시
```
feat(PLAN-001): implement JWT authentication

Added login/logout endpoints with token generation.
Password hashing uses bcrypt with salt rounds=12.

Closes #PLAN-001
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Gotchas
- Subject에 파일 경로 포함 금지 (Body 사용)
- 테스트 실패 시 커밋 금지 (검증 먼저 실행)
```

**기대 효과**:
- commit message quality: **+60%**
- project 간 재사용
- 새 워크플로우 add 용이 (Skill만 add)

---

#### 3.2 feedback 루프 통합
**난이도**: 🔴 High
**영향**: 🔴 High - learning 루프 완성

**system**:
```
team/.feedback/
├── outcomes.json (티켓 → 결과 매핑)
└── metrics.json (에이전트 Performance 메트릭)
```

**`outcomes.json`**:
```json
{
  "PLAN-001": {
    "agents": ["pm", "coding", "qa"],
    "completed": "2026-03-10T15:00:00Z",
    "pr_merged": "2026-03-11T10:00:00Z",
    "review_comments": 3,
    "revisions": 1,
    "test_pass_rate": 0.95,
    "outcome": "success",
    "learnings": [
      {
        "agent": "pm",
        "issue": "에러 응답 문서 누락",
        "pattern": "항상 4xx/5xx 응답 문서화",
        "added_to": "patterns.json#pm_pattern_003"
      }
    ]
  }
}
```

**feedback 수집**:
1. **PR 머지 후**: `bash scripts/record-outcome.sh PLAN-001 success`
2. **PR 코멘트 후**: GitHub API 파싱, issue 추출
3. **test failure 후**: 어떤 test case가 왜 failure했는지 기록

**feedback 적용**:
1. validation된 의사결정으로 `patterns.json` update
2. 반복 issue에 대한 새 Gotcha add
3. auto-response 신뢰도 score 조정
4. validation rule 튜닝

**dashboard** (optional):
```
team/scripts/dashboard.py
```

visible 항목:
- agent별 success률 (recently 30 ticket)
- 가장 흔한 failure 유형
- Gotcha 효과성 (방지된 failure 수)
- pattern 신뢰도 trend

**기대 효과**:
- agent 정확도: 월 **+15%**
- 자기 improvement system
- data 기반 Gotcha 우선ranking

---

#### 3.3 On-Demand Hooks (Plan전 가드)
**난이도**: 🟡 Medium
**영향**: 🟡 Medium - 치명적 실수 방지

**Thariq 영감**: "blocks rm -rf, DROP TABLE, force-push via PreToolUse matcher"

**implementation**:
```
team/.hooks/
├── pre-tool-use.json
└── validators/
    ├── dangerous-commands.py
    ├── scope-validator.py
    └── file-safety.py
```

**`pre-tool-use.json`**:
```json
{
  "hooks": [
    {
      "name": "block-dangerous-commands",
      "trigger": "Bash tool with rm -rf, DROP, git push --force",
      "action": "block",
      "message": "위험한 명령 차단. Plan전한 대Plan 사용."
    },
    {
      "name": "validate-file-paths",
      "trigger": "Write/Edit tool with path outside projects/{current_project}",
      "action": "warn",
      "message": "경고: 현재 프로젝트 디렉토리 외부에 파일 생성."
    },
    {
      "name": "prevent-spec-bloat",
      "trigger": "PM agent creates >5 spec files for single ticket",
      "action": "warn",
      "message": "범위 확대 가능성 - 티켓당 명세 2-3개 권장."
    }
  ]
}
```

**기대 효과**:
- 치명적 error: **-100%** (main으로 force push, data delete)
- project 외부 file create: **-90%**
- 정당한 task 제한 없이 Plan전성 확보

---

## 🔄 하up 호환성 전략

**원칙**: 모든 improvement은 add형, 파괴적 change none

### Phase 1
✅ agent는 all CLAUDE.md로 여전히 작동
✅ 새 `gotchas.md`와 `workflows/`는 optional적 improvement
✅ auto-responses.json 없으면 하드코딩으로 폴백

### Phase 2
✅ validation skills는 optional (auto-pipeline은 없이도 작동)
✅ 메모리 file은 read-only add (agent는 없이도 작동)
✅ 로그는 하up 호환

### Phase 3
✅ Skills는 agent 보완 (초기에는 대체 Plan 함)
✅ Hooks는 project별 optional
✅ feedback system은 manual (워크플로우 block Plan 함)

**project별 마이그레이션**:
```bash
# 기존 프로젝트는 계속 작동
cd projects/old-project
bash ../../scripts/run-agent.sh pm --ticket PLAN-001

# 새 프로젝트는 개선 사항 적용
cd projects/new-project
# 자동으로 gotchas, memory, validation 로드
bash ../../scripts/run-agent.sh pm --ticket PLAN-001
```

---

## 📈 success 메트릭

### Phase 1 (1-2주차)
- [ ] 각 agent CLAUDE.md를 <150줄로 zoom out
- [ ] agent당 10+ Gotchas documentation
- [ ] call당 컨text 사용량: **-30%**
- [ ] range 이탈 사고: **-40%**

### Phase 2 (3-5주차)
- [ ] ticket 100%에 Structure화된 로그
- [ ] `patterns.json`에 20+ pattern learning
- [ ] validation이 코딩 전 specification error 80%+ 포착
- [ ] 5+ 새 Gotcha auto 발견

### Phase 3 (6주차+)
- [ ] 3+ Skills 운영
- [ ] feedback 루프가 50+ ticket result 추적
- [ ] agent 정확도 월별 10% improvement
- [ ] 치명적 error 제로 (force push, 잘못된 directory)

---

## 🎯 implementation 우선ranking

### Must-Have (먼저 execute)
1. **Gotchas file** (Phase 1.1) - 최고 ROI, 가장 쉬움
2. **Progressive Disclosure** (Phase 1.2) - 큰 컨text 절약
3. **validation 후크** (Phase 2.2) - 비용 높은 실수 방지

### Should-Have (next execute)
4. **의사결정 로그** (Phase 2.1) - learning 가능화
5. **메모리 system** (Phase 2.3) - 자기 improvement
6. **Auto-responses data화** (Phase 1.3) - 유연성

### Nice-to-Have (나중 execute)
7. **Skills 마이그레이션** (Phase 3.1) - 장기 아키텍처
8. **feedback 루프** (Phase 3.2) - ticket 볼륨 required
9. **Plan전 Hooks** (Phase 3.3) - 완성도

---

## 🔑 핵심 implementation file

### immediately create/fix required
- **team/.agents/pm/gotchas.md** - currently CLAUDE.md 769-781줄에서 추출, 금지사항을 근본 원인과 탐지법이 있는 failure pattern으로 전환

- **team/.agents/pm/CLAUDE.md** - ~150줄로 zoom out, gotchas.md와 workflows/{project_type}.md를 가리키는 progressive disclosure Structure add

- **team/.config/auto-responses.json** - team/scripts/auto_pipeline.py 24-29줄의 하드코딩 pattern을 regex support JSON으로 move

- **team/scripts/auto_pipeline.py** - _check_auto_response() method (140-145줄) fix하여 JSON에서 load, PM agent completed 후 validation skill 통합 add

- **team/.skills/validate-spec/skill.md** - 완전성, range 준수, quality 게이트에 대한 specification validation 체크 and auto fix 제Plan create

---

## 💡 next stage

1. **Phase 1.1부터 start** (1-2일)
   - PM Agent의 gotchas.md create
   - 즉각적인 효과 confirmation

2. **result 측정**
   - range 이탈 사고 추적
   - token 사용량 compare

3. **점진적 확장**
   - 작동하면 다른 agent로 zoom in
   - Phase 1.2, 1.3 Progress

4. **feedback 수집**
   - 어떤 Gotchas가 가장 유용한지
   - 어떤 pattern이 가장 often 나타나는지

**start하시겠습니까?** Phase 1.1 (Gotchas file)부터 implementation해드릴까요?
