# Phase 3.1 part completed: Skill 기반 아키텍처 (commit skill) ✅

> **일시**: 2026-03-19
> **Phase**: 3.1 - Skill 기반 아키텍처 (점진적 마이그레이션)
> **소요 time**: ~20분
> **status**: ⚠️ part completed (commit skill만)

---

## 🎯 Goal

**하이브리드 Agent-Skill 아키텍처 구축**
- agent 유지 (기존 system 보존)
- Skills 점진 add (독립적인 task부터)
- 재available한 워크플로우

---

## 📦 Phase 3.1 - commit skill create

### create된 file (3개)

| file | 줄 수 | description |
|------|-------|------|
| `team/.skills/commit/skill.md` | 387줄 | Commit Skill documentation |
| `team/.skills/commit/commit-message-generator.py` | 389줄 | commit message auto create script |
| `team/.memory/commit-history.json` | 43줄 | commit 히스토리 learning data |

**총**: 819줄

**fix된 file**:
- `team/scripts/run-skill.sh`: commit 스킬 add (+3줄)

---

## 🔧 commit skill feature

### 1. Git Diff auto analytics

```bash
# 변경된 파일 확인
git diff --cached --name-status
```

**추출 info**:
- change된 file list
- file status (A=add, M=fix, D=delete)
- file type

### 2. commit type auto 결정

**rule 기반 판단**:
- `feat`: 새 file add 많음 (A > M)
- `fix`: 기존 file fix 많음 (M > A)
- `test`: test/ 또는 spec/ file
- `docs`: .md file만
- `chore`: package.json, .gitignore 등 configuration file
- `refactor`: feature change 없이 fix

**auto 판단 로직**:
```python
def determine_type(changed_files):
    if any("test" in f or "spec" in f for f in files):
        return "test"
    elif all(f.endswith(".md") for f in files):
        return "docs"
    elif added_count > modified_count:
        return "feat"
    else:
        return "fix"  # 기본값
```

### 3. Subject auto create

**input**:
- commit type
- change file path
- ticket description (optional)

**output**:
- 명령형 동사 (implement, fix, add)
- 70자 이하
- 소문자 start

**yes시**:
```
feat(PLAN-001): implement user authentication
fix(PLAN-002): resolve login validation error
test(PLAN-003): add integration tests for API
```

### 4. Body auto create (조건부)

**create 조건**:
- file 3개 이상 change
- 또는 type이 refactor/feat

**content**:
- change 이유 (optional)
- file list (maximum 5개)

### 5. Footer auto add

**required 포함**:
```
Closes #PLAN-001
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## 📤 output yes시

### yes시 1: Feature

```
feat(PLAN-001): implement JWT authentication

Added new functionality:
- src/auth/login.js
- src/auth/token.js
- src/auth/middleware.js

Closes #PLAN-001
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### yes시 2: Bug Fix

```
fix(PLAN-003): resolve null pointer in user profile

Closes #PLAN-003
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### yes시 3: Test

```
test(PLAN-005): add unit tests for payment module

Closes #PLAN-005
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## 🚀 usage

### manual execute

```bash
# 기본 - 메시지 생성 and 커밋
bash scripts/run-skill.sh commit --ticket PLAN-001

# Dry-run - 메시지만 확인
bash scripts/run-skill.sh commit --ticket PLAN-001 --dry-run

# 메시지만 생성 (승인 후 커밋)
bash scripts/run-skill.sh commit --ticket PLAN-001 --generate-only
```

### Auto-pipeline 통합 (향후)

```python
# auto_pipeline.py

# QA Agent Complete 후
result_qa = self.run_agent("qa", qa_prompt, ticket_num)

if result_qa["all_tests_passed"]:
    # Commit Skill 실행
    commit_result = self.run_skill("commit", ticket_num)

    if commit_result["success"]:
        print(f"✅ 커밋 Complete: {commit_result['commit_hash']}")
```

### Git Hook 통합 (optional)

```bash
# .git/hooks/prepare-commit-msg
#!/bin/bash

TICKET_NUM=$(git branch --show-current | grep -oP 'PLAN-\d+')

if [ -n "$TICKET_NUM" ]; then
    python3 .skills/commit/commit-message-generator.py --ticket $TICKET_NUM --generate-only > $1
fi
```

---

## 🧠 메모리 system 연계

### commit-history.json Structure

```json
{
  "project": "my-project",
  "vocabulary": {
    "auth": ["authentication", "login", "logout", "token"],
    "user": ["profile", "settings", "account"]
  },
  "frequent_verbs": {
    "feat": ["implement", "add", "create"],
    "fix": ["fix", "resolve", "correct"]
  },
  "recent_commits": [
    {
      "hash": "abc123",
      "message": "feat(PLAN-001): implement user authentication",
      "files": ["src/auth/login.js"],
      "timestamp": "2026-03-19T10:00:00Z"
    }
  ]
}
```

**learning 방법** (향후 implementation):
```python
def learn_from_git_history():
    # Git log에서 최근 50개 커밋 분석
    commits = git_log(limit=50)

    # 자주 사용되는 어휘 추출
    vocabulary = extract_vocabulary(commits)

    # 일관성 점수 계산
    consistency = check_consistency(commits)

    # commit-history.json 업데이트
```

---

## ⚠️ Gotchas (skill 내장)

### 1. Subject에 file path 포함 금지

❌ 잘못:
```
feat(PLAN-001): implement src/auth/login.js
```

✅ correct:
```
feat(PLAN-001): implement user authentication
```

### 2. test failure 시 commit 금지

**validation**:
```bash
# QA Agent Complete 확인
if qa_result["all_tests_passed"]:
    run_skill("commit")
```

### 3. 여러 ticket 혼합 금지

**검출**:
```python
# 변경 파일에서 티켓 번호 추출
if len(set(tickets)) > 1:
    print("⚠️  여러 티켓의 변경 감지. 티켓별로 커밋하세요.")
```

### 4. 빈 commit 방지

**validation**:
```bash
git diff --cached --quiet
if [ $? -eq 0 ]; then
    echo "변경 사항 없음"
    exit 0
fi
```

---

## 📊 기대 효과

### Before (manual commit)

```
개발자 작성:
- "fix bug"
- "update code"
- "wip"
- "test"
```

**problem점**:
- ❌ 일관성 none
- ❌ info 부족
- ❌ Git history 가독성 낮음

### After (commit skill)

```
자동 생성:
- "feat(PLAN-001): implement user authentication"
- "fix(PLAN-002): resolve login validation error"
- "test(PLAN-003): add integration tests for API"
```

**improvement점**:
- ✅ 100% 일관된 형식
- ✅ 명확한 info (type, 스코프, content)
- ✅ Git history 가독성 향상

### 수치 Goal

| 항목 | Goal |
|------|------|
| **commit message quality** | **+60%** |
| **작성 time** | **-90%** |
| **Git history 가독성** | **+80%** |
| **project 간 재사용** | **100%** |

---

## 🔗 다른 Skills와의 연계

### validate-spec → commit

```
명세서 검증 → Coding Agent → QA Agent → commit skill
```

### 향후 Skills (Phase 3.1 완성 시)

**review-pr skill**:
```
커밋 → PR 생성 → review-pr skill (자동 리뷰)
```

**refactor-code skill**:
```
리팩토링 제Plan → 적용 → commit skill (type=refactor)
```

---

## 🎯 Phase 3.1 all Plan

### completed된 Skills (1/4)

- ✅ **commit skill** - commit message auto create
- ⬜ **review-pr skill** - PR auto review
- ⬜ **refactor-code skill** - code improvement 제Plan
- ⬜ agent Skills 사용 refactoring

### 마이그레이션 path

**Week 1** (currently):
- ✅ commit skill create
- ⬜ validate-spec skill (Phase 2.2에서 이미 completed)

**Week 2**:
- review-pr skill add
- refactor-code skill add

**Week 3**:
- PM Agent가 validate-spec skill call하도록 fix
- Coding Agent가 commit skill call하도록 fix
- QA Agent가 review-pr skill call하도록 fix

**2-3개월**:
- agent feature을 점진적으로 Skills로 마이그레이션
- 하이브리드 Structure 유지

---

## 💡 핵심 인사이트

### Skill 아키텍처의 장점

1. **재사용성**: project 간 100% 재사용
2. **독립성**: Skill add/remove가 agent에 영향 none
3. **test 용이**: Skill 단up로 test 가능
4. **확장 용이**: 새 워크플로우는 Skill만 add

### 하이브리드 접근의 이점

1. **기존 system 보존**: agent continue 작동
2. **점진적 마이그레이션**: 한 번에 하나씩
3. **up험 minimize**: failure 시 롤백 쉬움
4. **learning 곡선**: 천천히 적응 가능

---

## 🚀 next stage

### immediately test 가능

```bash
# 1. 테스트용 변경 만들기
cd projects/test-project
echo "# Test" > test.md
git add test.md

# 2. Commit Skill 실행 (dry-run)
bash ../../scripts/run-skill.sh commit --ticket PLAN-001 --dry-run

# 3. 실제 커밋
bash ../../scripts/run-skill.sh commit --ticket PLAN-001

# 4. Git log 확인
git log -1
```

### Phase 3.1 완성 (권장 순서)

1. **review-pr skill** add
   - PR auto review 체크리스트
   - code quality 검사
   - Auto-fix 제Plan

2. **refactor-code skill** add
   - code 스멜 감지
   - refactoring pattern 제Plan
   - 복잡도 analytics

3. **agent refactoring**
   - auto_pipeline.py에 Skills 통합
   - agent CLAUDE.md에 Skill 사용 지침 add

---

## 📈 Phase 3.1 (commit skill) 성과

### create된 자산

| 카테고리 | file 수 | 줄 수 |
|---------|--------|------|
| **Skill documentation** | 1개 | 387줄 |
| **Skill script** | 1개 | 389줄 |
| **메모리 file** | 1개 | 43줄 |
| **script fix** | 1개 | +3줄 |
| **total** | 4개 | 822줄 |

### improvement 메트릭

| 항목 | 달성 |
|------|------|
| **commit type auto 결정** | ✅ 7개 type (feat, fix, test, docs, refactor, chore, style) |
| **Subject auto create** | ✅ 70자 제한, 명령형 |
| **Body 조건부 create** | ✅ file 3개 이상 또는 refactor/feat |
| **Footer auto add** | ✅ Closes, Co-Authored-By |
| **Gotchas 내장** | ✅ 4개 (file path, test, 여러 ticket, 빈 commit) |
| **메모리 연계** | ✅ commit-history.json |

---

## 🎉 Phase 3.1 (commit skill) completed!

**달성**:
- ✅ commit skill create (documentation + script)
- ✅ commit type auto 결정
- ✅ Subject/Body/Footer auto create
- ✅ 4개 Gotchas 내장
- ✅ 메모리 system 연계

**기대 효과**:
- commit message quality: **+60%**
- 작성 time: **-90%**
- Git history 가독성: **+80%**

**next**: Phase 3.1 나머지 (review-pr, refactor-code)? 또는 Phase 3.2/3.3?

---

## 📝 change 이력

### 2026-03-19
- ✅ `team/.skills/commit/skill.md` create
- ✅ `team/.skills/commit/commit-message-generator.py` create
- ✅ `team/.memory/commit-history.json` create
- ✅ `team/scripts/run-skill.sh` update (commit add)
