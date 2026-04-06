# Phase 1.1 implementation 로그

> **일시**: 2026-03-19
> **task**: Gotchas file create + Progressive Disclosure 적용
> **소요 time**: ~30분
> **status**: ✅ completed

---

## 📋 implementation content

### 1. PM Agent Gotchas file create

**file**: `team/.agents/pm/gotchas.md` (483줄)

**포함된 10가지 Gotchas**:
1. ✅ range zoom in (Scope Creep)
2. ✅ 잘못된 project directory
3. ✅ project type 무시
4. ✅ HTML 와이어프레임에 외부 library
5. ✅ 실제 API call 시뮬레이션 누락
6. ✅ user approval 없이 file create
7. ✅ 로그 작성 생략
8. ✅ API specification에서 error response 누락
9. ✅ test case 접근성 누락
10. ✅ Coding Agent role 침범

**각 Gotcha Structure**:
- ❌ 증상
- 🔍 근본 원인
- 📝 실제 failure 사례
- 🚨 탐지 방법
- ✅ 올바른 접근

---

### 2. CLAUDE.md zoom out (Progressive Disclosure)

**change 전**: `CLAUDE.md` (833줄)
**change 후**: `CLAUDE.md` (231줄)
**zoom out율**: **-72% (602줄 decrease)**

**backup**: `CLAUDE-backup-20260319.md`

**새 Structure**:
```markdown
# PM Agent (231줄)
├── 역할 정의
├── 📂 파일 Structure Plan내 (gotchas, workflows, templates)
├── 🤖 자동화 모드 규칙
├── 🔨 핵심 프로세스 (Step 0-4)
├── ⚠️ 금지 사항 (요약만, 상세는 gotchas.md)
└── 📋 체크리스트
```

**Progressive Disclosure 적용**:
- agent가 required한 file만 읽도록 Plan내
- `gotchas.md` → `workflows/{project_type}.md` → task start
- 컨text load 시 all가 아닌 required part만

---

### 3. Auto-Responses data화

**file**: `team/.config/auto-responses.json`

**하드코딩 remove**:
```python
# 기존 (auto_pipeline.py 24-29줄)
self.auto_responses = {
    "추가할까요": "no, 티켓 범위 내에서만...",
    "변경할까요": "no, 현재 명세대로...",
    "괜찮을까요": "yes, 계속..."
}
```

**new운 방식** (JSON 기반):
```json
{
  "pm": {
    "patterns": [
      {
        "id": "prevent-scope-creep",
        "trigger": "(추가|더|또한).*(기능|구현).*할까요",
        "response": "no, 티켓 범위 내에서만...",
        "reason": "scope_creep_prevention",
        "gotcha_ref": "gotchas.md#1",
        "confidence": 0.95
      }
    ]
  }
}
```

**장점**:
- ✅ Regex support (더 정교한 매칭)
- ✅ Gotcha reference 연결
- ✅ 신뢰도 score (learning 기반 조정 가능)
- ✅ code deployment 없이 rule change

---

## 📊 기대 효과

### 컨text 효율
```
기존: 833줄 전체 로드
개선: 231줄 (핵심) + 필요 시 gotchas.md/workflows 로드
절약: -30% 예상
```

### failure 방지
```
Gotcha #1 (범위 확대): 40% 감소 예상
Gotcha #2 (잘못된 디렉토리): 90% 감소 예상
Gotcha #4 (HTML 라이브러리): 100% 감소 예상
```

### 유지보수
```
새 실패 패턴 발견 시:
- 기존: CLAUDE.md 전체 수정 (833줄)
- 개선: gotchas.md만 업데이트 (1개 섹션 추가)
```

---

## 🧪 test Plan

### 1. 기존 feature 호환성 test

```bash
# PM Agent 실행 (기존 방식)
bash team/scripts/run-agent.sh pm --ticket-file projects/test-project/planning/tickets/PLAN-001-test.md

# 체크 포인트:
# - gotchas.md를 읽는가?
# - 올바른 경로에 파일 생성하는가?
# - 로그가 정상 작성되는가?
```

### 2. Gotcha 효과 측정

next 3개 ticket으로 test:
- ticket A: range zoom in 유도 ("auth feature" → OAuth add하는지 confirmation)
- ticket B: path 혼동 유도 (project confirmation 생략하는지)
- ticket C: HTML library (Tailwind 사용하는지)

**success 기준**:
- [ ] range zoom in Plan 함 (Out-of-Scope에 기록만)
- [ ] 올바른 path에 file create
- [ ] 바닐라 JS만 사용

### 3. 컨text 사용량 측정

```bash
# API 호출 로그 비교
# 기존: 833줄 CLAUDE.md → N tokens
# 개선: 231줄 CLAUDE.md → M tokens
# 절감: (N-M)/N * 100%
```

---

## 🚀 next stage (Phase 1.2, 1.3)

### Phase 1.2: Workflows file 분리

**create할 file**:
```
team/.agents/pm/workflows/
├── web-fullstack.md (현재 CLAUDE-backup에서 추출)
├── cli-tool.md
├── desktop-app.md
├── web-mvc.md
├── library.md
└── data-pipeline.md
```

**yes상 효과**:
- CLAUDE.md를 100줄 이하로 더 zoom out
- project type별 required한 워크플로우만 load
- 새 project type add 시 워크플로우 file만 add

**소요 time**: 1-2time

---

### Phase 1.3: auto_pipeline.py fix

**fix file**: `team/scripts/auto_pipeline.py`

**change content**:
```python
# 기존 (24-29줄)
self.auto_responses = {
    "추가할까요": "no, ...",
    # ...
}

# 개선
def load_auto_responses(self):
    with open('.config/auto-responses.json') as f:
        return json.load(f)

def _check_auto_response(self, message: str) -> str:
    rules = self.auto_responses.get(self.agent_name, {}).get("patterns", [])
    for rule in rules:
        if re.search(rule["trigger"], message):
            return rule["response"]
    return self.auto_responses["fallback"]["default_response"]
```

**소요 time**: 30분

---

## 📈 success 메트릭

### immediately 측정 가능
- [x] CLAUDE.md 줄 수: 833 → 231 (-72%)
- [ ] Gotchas documentation: 0 → 10개
- [ ] Auto-response pattern: 3 → 15+

### 1주일 후 측정
- [ ] range 이탈 사고: previous 대비 -40%
- [ ] 잘못된 path error: previous 대비 -90%
- [ ] HTML library 사용: 0건

### 1개월 후 측정
- [ ] 새 Gotcha 발견: 5+ 개 (auto 발견 script Phase 2.4)
- [ ] 컨text token 절약: 누적 20%+

---

## 🔄 롤백 Plan

problem 발생 시:
```bash
cd team/.agents/pm
mv CLAUDE.md CLAUDE-new-broken.md
mv CLAUDE-backup-20260319.md CLAUDE.md
```

---

## 💡 인사이트

### Thariq의 교훈 적용

1. **"The highest-signal content is the Gotchas section"**
   ✅ implementation: gotchas.md 483줄 (가장 많은 info)

2. **"Progressive Disclosure"**
   ✅ implementation: CLAUDE.md → gotchas.md → workflows/{type}.md

3. **"Don't state the obvious"**
   ✅ implementation: 금지사항을 "왜 failure하는지" pattern으로 전환

### yes상 못한 이점

- **search 가능성**: Gotcha별 ID로 reference (gotchas.md#1)
- **learning 가능성**: 신뢰도 score로 pattern 효과 추적
- **협업 improvement**: 팀원이 gotchas.md만 보고 agent action 이해

---

## 📝 improvement ID어 (later)

- [ ] Gotcha 효과 auto 측정 script
- [ ] 주간 Gotcha report (가장 많이 발동된 pattern)
- [ ] Auto-response 신뢰도 auto 조정 (success률 기반)

---

**next implementation**: Phase 1.2 - Workflows file 분리
**yes상 일정**: 2026-03-20
