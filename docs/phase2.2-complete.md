# Phase 2.2 completed: Validation Hooks (validate-spec Skill) ✅

> **일시**: 2026-03-19
> **Phase**: 2.2 - validation Hooks
> **소요 time**: ~30분
> **status**: ✅ completed

---

## 🎯 Goal

**PM Agent output물을 Coding Agent로 전달하기 전에 auto validation**
- 잘못된 specification로 인한 코딩 failure 사전 block
- API call 60%+ 절약

---

## 📦 create된 file (4개)

| file | 줄 수 | description |
|------|-------|------|
| `team/.skills/validate-spec/skill.md` | 473줄 | 스킬 documentation (validation 항목, usage) |
| `team/.skills/validate-spec/rules.json` | 234줄 | validation rule configuration (project type별) |
| `team/.skills/validate-spec/validate.py` | 573줄 | 실제 validation 로직 (Python) |
| `team/scripts/run-skill.sh` | 32줄 | Skill execute wrapper |

**총**: 1,312줄

---

## 🔍 validation 항목 (5개 카테고리)

### 1. 완전성 검사 (Completeness)

**project type별 required file 존재 여부**:
- Web-Fullstack: 5개 file (backend, frontend, html, 2 test-cases)
- CLI Tool: 2개 file (command-spec, test-cases)
- Desktop App: 6개 file (screens, state, 3 test-cases)
- Library: 4개 file (api, examples, 2 test-cases)

**required section 존재 여부**:
- Backend: "endpoint list", "Request Body", "Response 200"
- Frontend: "화면 list", "유저 플로우", "컴포넌트 configuration"
- CLI: "커맨드", "flag", "exit code"

### 2. range 준수 검사 (Scope Compliance)

**Gotcha #1 적용 - range zoom in 방지**:
- ticket의 Acceptance Criteria 추출
- specification의 feature list 추출
- range zoom in 의심 키워드 탐지:
  - OAuth, 소셜 login, email authentication
  - password 재configuration, 2FA
  - administrator, dashboard, analytics
- Out-of-Scope section confirmation

### 3. quality 게이트 (Quality Gates)

**API specification**:
- [x] REST 규약 준수 (POST=create, GET=조회, etc.)
- [x] error response 완비 (400, 401, 500 required) - **Gotcha #8**

**HTML 와이어프레임**:
- [x] 외부 library 금지 (tailwind, react, vue 등) - **Gotcha #4**
- [x] 실제 API call 금지 (fetch, axios 등) - **Gotcha #5**

**접근성**:
- [x] 접근성 test case 포함 - **Gotcha #9**

**CLI Tool**:
- [x] Exit Code 정의 required

### 4. implementation 세부사항 침범 검사

**Gotcha #10 적용 - Coding Agent role 침범 방지**:

금지된 키워드 탐지:
- library: bcrypt, jwt, axios, mongoose, prisma
- file Structure: src/, lib/, controllers/, services/
- DB 스키마: VARCHAR, INTEGER, PRIMARY KEY
- design pattern: Singleton, Factory, MVC

### 5. auto fix (Auto-fix)

경미한 issue auto fix:
- [x] Out-of-Scope section 누락 시 auto add
- [x] 하드코딩 password → 환경 variable reference
- [x] HTTP → HTTPS 변환

---

## 🚀 usage

### manual execute

```bash
# 특정 티켓 검증
bash team/scripts/run-skill.sh validate-spec PLAN-001

# 검증 + 자동 수정
bash team/scripts/run-skill.sh validate-spec PLAN-001 --auto-fix

# Python 직접 실행
cd projects/my-project
python3 ../../.skills/validate-spec/validate.py PLAN-001 --auto-fix
```

### Auto-pipeline 통합 (auto)

```python
# auto_pipeline.py에 통합됨

# PM Agent 실행 후
result = self.run_agent("pm", ticket_content, ticket_num)

# 자동으로 검증 실행
validation_result = self._run_validate_spec(ticket_num, auto_fix=True)

if not validation_result["passed"]:
    # PM Agent 재실행 (이슈 포함)
    retry_prompt = self._build_retry_prompt(ticket_content, validation_result)
    result = self.run_agent("pm", retry_prompt, ticket_num)

    # 재검증
    validation_retry = self._run_validate_spec(ticket_num, auto_fix=True)

    if not validation_retry["passed"]:
        raise Exception("수동 개입 필요")
```

---

## 📤 output yes시

### success 시

```
============================================================
Spec Validation: PLAN-001
프로젝트 타입: web-fullstack
============================================================

1️⃣  완전성 검사...
   ✅ 5/5 파일 생성 Complete

2️⃣  범위 준수 검사...
   ✅ 범위 확대 없음

3️⃣  품질 게이트...
   ✅ API 에러 응답 완비
   ✅ HTML 외부 라이브러리 없음
   ✅ HTML API 호출 없음 (목업만 사용)

4️⃣  구현 세부사항 침범 검사...
   ✅ 구현 세부사항 침범 없음

5️⃣  자동 수정 적용...
   (없음)

============================================================
✅ Spec Validation 통과: PLAN-001
============================================================

다음 조치:
Coding Agent 실행 가능

📝 로그 저장: projects/my-project/logs/validate-spec/20260319-153000-PLAN-001.md
```

### failure 시

```
============================================================
❌ Spec Validation 실패: PLAN-001
============================================================

에러 (2개):
1. [완전성] 필수 파일 누락: specs/test-cases/PLAN-001-backend.md
2. [품질] API 에러 응답 누락: 401 (in PLAN-001-backend.md)

경고 (3개):
1. [범위] 'OAuth' 발견 (티켓에 없음) - PLAN-001-backend.md
2. [품질] 접근성 테스트 케이스 누락
3. [구현] 구현 세부사항 포함 의심: 'bcrypt' in PLAN-001-backend.md

자동 수정 (1개):
✓ Out-of-Scope 섹션 추가: PLAN-001-backend.md

다음 조치:
1. PM Agent 재실행하여 누락된 파일/섹션 생성
2. 에러 수정 후 재검증 필요
```

---

## 🧪 validation 로직 implementation

### 핵심 class

```python
class SpecValidator:
    def __init__(self, project_root: Path, ticket_num: str):
        self.rules = self._load_rules()  # rules.json
        self.project_meta = self._load_project_meta()  # .project-meta.json
        self.project_type = self.project_meta.get("project_type")

    def validate(self, auto_fix: bool = False) -> ValidationResult:
        # 1. 완전성 검사
        self._check_completeness(result)

        # 2. 범위 준수 검사
        self._check_scope_compliance(result)

        # 3. 품질 게이트
        self._check_quality_gates(result)

        # 4. 구현 세부사항
        self._check_implementation_details(result)

        # 5. 자동 수정
        if auto_fix:
            self._apply_auto_fixes(result)

        return result
```

### 주요 method

**완전성 검사**:
```python
def _check_completeness(self, result):
    # 프로젝트 타입별 필수 파일 확인
    required_files = self.rules["project_type_Requirements"][self.project_type]["required_files"]

    for file_pattern in required_files:
        # {number}, {slug} 치환
        file_path = file_pattern.replace("{number}", ticket_num)
        if not file_path.exists():
            result.errors.append(f"필수 파일 누락: {file_path}")

        # 섹션 검사
        self._check_file_sections(file_path, result)
```

**range 준수 검사**:
```python
def _check_scope_compliance(self, result):
    # 티켓 Acceptance Criteria 추출
    ticket_features = self._extract_acceptance_criteria(ticket_content)

    # 범위 확대 키워드 탐지
    scope_keywords = self.rules["scope_creep_keywords"]
    for keyword in scope_keywords:
        if keyword in spec_content and keyword not in ticket_content:
            # Out-of-Scope 섹션 확인
            if not has_out_of_scope_section(spec_file):
                result.errors.append(f"범위 확대 + Out-of-Scope 누락: {keyword}")
            else:
                result.warnings.append(f"범위 확대 의심: {keyword}")
```

**quality 게이트**:
```python
def _check_error_responses(self, result):
    # API 에러 응답 (Gotcha #8)
    required_codes = ["400", "401", "500"]
    for code in required_codes:
        pattern = rf"(Response|응답|에러|Error)\s*{code}"
        if not re.search(pattern, content, re.IGNORECASE):
            result.errors.append(f"API 에러 응답 누락: {code}")

def _check_html_libraries(self, result):
    # HTML 외부 라이브러리 (Gotcha #4)
    forbidden = ["tailwind", "react", "vue", "bootstrap", "cdn"]
    for pattern in forbidden:
        if re.search(pattern, html_content, re.IGNORECASE):
            result.errors.append(f"HTML 외부 라이브러리 사용: {pattern}")
```

---

## 📊 기대 효과

### Before (validation none)

```
PM Agent → Coding Agent
         ↓ (잘못된 명세서)
       실패 → 재작업 → PM Agent 재실행 → Coding Agent 재실행

API 호출: 5-10회
```

### After (validation 적용)

```
PM Agent → Validate-Spec → 통과 → Coding Agent
           ↓ (실패)
         재실행 (이슈 포함)
           ↓
         통과 → Coding Agent

API 호출: 2-3회
절감: 60-70%
```

### 수치 Goal

| 항목 | Goal |
|------|------|
| **error 사전 포착률** | **80%+** |
| **API call 절감** | **60%+** |
| **range zoom in 방지** | **90%+** |
| **quality 게이트 통과율** | **95%+** |

---

## 🔗 Gotchas 연결

| Gotcha | validation 항목 | 탐지 방법 |
|--------|---------|---------|
| #1 range zoom in | range 준수 검사 | 키워드 매칭 + Out-of-Scope confirmation |
| #4 HTML library | quality 게이트 | Regex pattern 매칭 |
| #5 API call | quality 게이트 | fetch/axios 탐지 |
| #8 error response 누락 | quality 게이트 | required HTTP code confirmation |
| #9 접근성 누락 | quality 게이트 | 키워드 매칭 |
| #10 role 침범 | implementation 세부사항 | implementation 키워드 탐지 |

---

## 📝 로그 system

**로그 path**: `projects/{project}/logs/validate-spec/{timestamp}-{ticket_num}.md`

**로그 content**:
- validation result 요약 (통과/failure)
- 각 카테고리별 상세 result
- 발견된 error/warning list
- 적용된 auto fix list
- next 조치 권장사항

**활용**:
- failure pattern analytics
- 주간 report (가장 많이 발견된 issue)
- Phase 2.4 (Gotcha Auto-Discovery)의 data 소스

---

## 🔧 configuration 커스터마이징

`rules.json`에서 validation rule 조정 가능:

```json
{
  "rules": {
    "completeness": {
      "enabled": true,
      "severity": "error"
    },
    "scope_compliance": {
      "enabled": true,
      "severity": "error",
      "strict_mode": false,
      "scope_creep_keywords": [
        "OAuth", "소셜 로그인", "관리자"
      ]
    },
    "quality_gates": {
      "error_responses": {
        "enabled": true,
        "required_codes": ["400", "401", "500"]
      },
      "html_libraries": {
        "enabled": true,
        "forbidden_patterns": ["tailwind", "react"]
      }
    }
  },
  "auto_fix": {
    "enabled": true,
    "rules": [
      "add_out_of_scope_section",
      "replace_hardcoded_secrets",
      "http_to_https"
    ]
  }
}
```

---

## 💡 핵심 인사이트

### yes상 못한 이점

1. **조기 feedback**: Coding Agent execute 전 problem 발견 → 빠른 fix 사이클
2. **learning data**: validation 로그 → Phase 2.4 auto Gotcha 발견에 활용
3. **auto fix**: 간단한 issue는 auto solution → manual 개입 minimize
4. **일관성**: 모든 specification가 동일한 quality 기준 통과

### improvement points

1. **다른 agent로 확장**:
   - Coding Agent output물 validation (코딩 룰 준수 confirmation)
   - QA Agent output물 validation (test coverage confirmation)

2. **신뢰도 score**:
   - validation rule별 success률 추적
   - 낮은 success률 rule → 튜닝 required

3. **CI/CD 통합**:
   - PR create 전 auto validation
   - validation failure 시 PR block

---

## 🎯 Thariq 교훈 적용

| Thariq 교훈 | 적용 방법 |
|------------|----------|
| **"Validation skills catch 80%+ errors"** | validate-spec 스킬 implementation ✅ |
| **"Hooks before expensive operations"** | PM → Coding 사이에 validation ✅ |
| **"Scripts & Code over instructions"** | Python script로 automation ✅ |
| **"Memory & Data"** | rules.json으로 configuration 관리 ✅ |
| **"Gotchas are highest-signal"** | Gotchas 6개 연결 ✅ |

---

## 🚀 next stage

### immediately test 가능

```bash
# 테스트용 티켓 생성
cd team
bash scripts/run-agent.sh pm --ticket-file projects/test-project/planning/tickets/PLAN-001-test.md

# 검증 실행
bash scripts/run-skill.sh validate-spec PLAN-001 --auto-fix

# Auto-pipeline 통합 테스트
python3 scripts/auto_pipeline.py --project projects/test-project
```

### Phase 2 나머지 항목

**Phase 2.1 - Structure화된 의사결정 로그** (우선ranking: 높음)
- agent 로그에 의사결정 + 근거 + 신뢰도 기록
- 향후 learning의 기반

**Phase 2.3 - 메모리 system** (우선ranking: 중간)
- `patterns.json`: success pattern save
- `failures.json`: failure pattern save
- 반복 실수 learning

**Phase 2.4 - Gotcha Auto-Discovery** (우선ranking: 중간)
- validation 로그 analytics
- new운 Gotcha auto 발견
- 주간 report

---

## 📈 Phase 2.2 성과

### create된 자산

| 카테고리 | file 수 | 줄 수 |
|---------|--------|------|
| **documentation** | 1개 | 473줄 |
| **configuration** | 1개 | 234줄 |
| **script** | 2개 | 605줄 |
| **통합** | auto_pipeline.py fix | +70줄 |
| **total** | 4개 | 1,382줄 |

### improvement 메트릭

| 항목 | 달성 |
|------|------|
| **validation 카테고리** | **5개** (완전성, range, quality, implementation, autofix) |
| **Gotcha 연결** | **6개** (#1, #4, #5, #8, #9, #10) |
| **project type support** | **4개** (web-fullstack, cli-tool, desktop-app, library) |
| **Auto-fix rule** | **3개** (Out-of-Scope, password, HTTP) |
| **로그 system** | **✅** (validation result save) |
| **Auto-pipeline 통합** | **✅** (PM Agent 후 auto validation) |

---

## 🎉 Phase 2.2 completed!

**달성**:
- ✅ validation 스킬 **5개 카테고리** implementation
- ✅ Gotcha 연결 **6개**
- ✅ Auto-fix **3개 rule**
- ✅ Auto-pipeline 통합
- ✅ 로그 system
- ✅ project type별 rule **4개**

**기대 효과**:
- error 사전 포착 **80%+**
- API call 절감 **60%+**
- range zoom in 방지 **90%+**

**next**: Phase 2.1, 2.3, 또는 2.4?

---

## 📝 change 이력

### 2026-03-19
- ✅ `team/.skills/validate-spec/skill.md` create
- ✅ `team/.skills/validate-spec/rules.json` create
- ✅ `team/.skills/validate-spec/validate.py` create
- ✅ `team/scripts/run-skill.sh` create
- ✅ `team/scripts/auto_pipeline.py` fix (validation 통합)
