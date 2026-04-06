# Git branch 전략

멀티 agent system의 Git branch 전략 상세 guide

---

## 📌 핵심 원칙

### branch 흐름

```
main/dev (베이스 브랜치)
  │
  ├─ docs/PLAN-001-xxx        (PM Agent)
  │
  └─ feature/PLAN-001-xxx     (Coding Agent)
       │
       └─ test/PLAN-001-xxx   (QA Agent)
```

**important:**
- **PM, Coding Agent**: `base_branch` (main/dev)에서 분기
- **QA Agent**: 동일한 ticket의 **feature branch**에서 분기

---

## 🌿 agent별 branch 전략

### 1. PM Agent

**branch pattern**: `docs/{티켓번호}-{slug}`

**베이스**: base_branch (main/dev)

**yes시**:
```bash
bash scripts/run-agent.sh pm --ticket-file projects/my-app/planning/tickets/PLAN-001-user-auth.md
# → main에서 docs/PLAN-001-user-auth 브랜치 생성
```

**용도**: specification and test case 작성

---

### 2. Coding Agent

**branch pattern**: `feature/{티켓번호}-{slug}`

**베이스**: base_branch (main/dev)

**yes시**:
```bash
bash scripts/run-agent.sh coding --ticket PLAN-001
# → main에서 feature/PLAN-001-user-auth 브랜치 생성
```

**용도**: 실제 code implementation

---

### 3. QA Agent

**branch pattern**: `test/{티켓번호}-{slug}`

**베이스**: **feature branch** (동일 ticket)

**yes시**:
```bash
bash scripts/run-agent.sh qa --ticket PLAN-001
# → feature/PLAN-001-user-auth에서 test/PLAN-001-user-auth 브랜치 생성
```

**용도**: test code 작성

**important 사항**:
- QA Agent를 execute하기 전에 반드시 Coding Agent를 먼저 must execute 합니다
- feature branch가 없으면 warning message를 visible하고 base_branch를 사용

---

## 🔄 all 워크플로우 yes시

### 시나리오: PLAN-001 유저 authentication feature development

```bash
cd team

# 1. PM Agent: 명세서 작성
bash scripts/run-agent.sh pm --ticket-file projects/my-app/planning/tickets/PLAN-001-user-auth.md
# → docs/PLAN-001-user-auth 브랜치 생성 (from main)

cd projects/my-app
git add .
git commit -m "docs(PLAN-001): 유저 인증 명세서 작성"
git push origin docs/PLAN-001-user-auth
cd ../..

# 2. Coding Agent: 코드 구현
bash scripts/run-agent.sh coding --ticket PLAN-001
# → feature/PLAN-001-user-auth 브랜치 생성 (from main)

cd projects/my-app
git add .
git commit -m "feat(PLAN-001): 유저 인증 구현"
git push origin feature/PLAN-001-user-auth
cd ../..

# 3. QA Agent: 테스트 작성
bash scripts/run-agent.sh qa --ticket PLAN-001
# → test/PLAN-001-user-auth 브랜치 생성 (from feature/PLAN-001-user-auth)

cd projects/my-app
git add .
git commit -m "test(PLAN-001): 유저 인증 테스트 작성"
git push origin test/PLAN-001-user-auth
cd ../..
```

### branch Structure (최종)

```
my-app/.git/
├── main
├── docs/PLAN-001-user-auth           (from main)
├── feature/PLAN-001-user-auth        (from main)
└── test/PLAN-001-user-auth           (from feature/PLAN-001-user-auth)
```

---

## ⚙️ configuration file

### `.config/git-workflow.json`

```json
{
  "branch_strategy": {
    "enabled": true,
    "base_branch": "main",
    "auto_create": true,
    "auto_checkout": true
  },
  "branch_naming": {
    "base_branch_by_agent": {
      "pm": "base_branch",
      "coding": "base_branch",
      "qa": "feature_branch"
    }
  }
}
```

**주요 configuration**:
- `base_branch`: PM/Coding이 사용할 베이스 branch (main, dev 등)
- `qa`: feature_branch 사용 (동일 ticket)

---

## 🔧 manual branch 관리

### branch 준비 (agent가 auto execute)

```bash
# Coding Agent용
bash scripts/git-branch-helper.sh prepare coding PLAN-001 user-auth
# → main에서 feature/PLAN-001-user-auth 생성

# QA Agent용
bash scripts/git-branch-helper.sh prepare qa PLAN-001 user-auth
# → feature/PLAN-001-user-auth에서 test/PLAN-001-user-auth 생성
```

### currently status confirmation

```bash
bash scripts/git-branch-helper.sh status
```

### configuration confirmation

```bash
bash scripts/git-branch-helper.sh config
```

---

## 🚨 note사항

### 1. QA Agent execute 순서

❌ **잘못된 순서**:
```bash
bash scripts/run-agent.sh qa --ticket PLAN-001
# feature 브랜치가 없음 → 경고
```

✅ **올바른 순서**:
```bash
bash scripts/run-agent.sh coding --ticket PLAN-001
# feature 브랜치 생성

bash scripts/run-agent.sh qa --ticket PLAN-001
# feature 브랜치에서 test 브랜치 생성
```

### 2. 베이스 branch change

dev branch를 사용하려면:

```json
{
  "branch_strategy": {
    "base_branch": "dev"
  }
}
```

### 3. project별 Git

각 project는 독립적인 Git is 리포지토리:

```
team/projects/
├── my-app/.git/           # 프로젝트 A Git
└── my-blog/.git/          # 프로젝트 B Git
```

branch task은 **project 리포지토리 내**에서 becomes perform.

---

## 📋 branch 네이밍 rule

### pattern

```
{prefix}/{ticket-number}-{slug}
```

### yes시

| ticket | PM | Coding | QA |
|-----|-------|--------|-----|
| PLAN-001-user-auth | `docs/PLAN-001-user-auth` | `feature/PLAN-001-user-auth` | `test/PLAN-001-user-auth` |
| PLAN-002-todo-crud | `docs/PLAN-002-todo-crud` | `feature/PLAN-002-todo-crud` | `test/PLAN-002-todo-crud` |

### Slug 추출

ticket file명에서 auto 추출:
- `PLAN-001-user-auth.md` → slug: `user-auth`
- `PLAN-002-todo-crud.md` → slug: `todo-crud`

---

## 🔀 PR (Pull Request) 전략

### 1. Feature → Main

```bash
cd projects/my-app
git checkout feature/PLAN-001-user-auth
git push origin feature/PLAN-001-user-auth
# GitHub에서 PR: feature/PLAN-001-user-auth → main
```

### 2. Test → Feature (option)

test를 별도 PR로 관리:

```bash
cd projects/my-app
git checkout test/PLAN-001-user-auth
git push origin test/PLAN-001-user-auth
# GitHub에서 PR: test/PLAN-001-user-auth → feature/PLAN-001-user-auth
```

### 3. Feature + Test → Main (권장)

feature branch에 test branch를 머지 후 PR:

```bash
cd projects/my-app
git checkout feature/PLAN-001-user-auth
git merge test/PLAN-001-user-auth
git push origin feature/PLAN-001-user-auth
# GitHub에서 PR: feature/PLAN-001-user-auth → main
```

---

## 🛠️ 트러블슈팅

### Q1. feature branch가 없는데 QA를 execute했어요

**현상**:
```
⚠️  feature 브랜치가 없습니다: feature/PLAN-001-user-auth
   먼저 coding 에이전트를 실행하세요.
   또는 기본 베이스 브랜치를 사용합니다: main
```

**solution**:
1. Coding Agent를 먼저 execute
2. 또는 main에서 test branch create (권장하지 않음)

### Q2. branch가 auto으로 create되지 않아요

**confirmation사항**:
```bash
# 설정 확인
cat .config/git-workflow.json

# auto_create가 true인지 확인
```

### Q3. 다른 베이스 branch를 사용하고 싶어요

**solution**:
```json
{
  "branch_strategy": {
    "base_branch": "develop"
  }
}
```

---

**version**: v0.0.2
**최종 update**: 2026-03-12
