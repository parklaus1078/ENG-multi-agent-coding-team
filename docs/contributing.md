# system improvement guide

> 멀티 agent system developer를 up한 기여 guide

**version**: v0.0.2
**최종 update**: 2026-03-12
**대상**: system developer

---

## 🎯 이 documentation의 목적

이 documentation는 멀티 agent **system 자체**를 improvement하는 developer를 up한 is guide.

system user가 agent를 이용하여 project를 implementation하는 방법은 [루트 README.md](../README.md)를 please reference.

---

## 📂 system Structure 이해

### 핵심 directory

```
team/
├── .agents/              # 에이전트 지시 파일 (CLAUDE.md)
├── .rules/               # 코딩 룰
│   ├── _verified/        # 검증된 룰
│   └── _cache/           # 자동 생성 룰
├── .config/              # 시스템 설정
├── scripts/              # 시스템 스크립트
├── projects/             # 사용자 프로젝트 (독립 Git)
└── docs/                 # 시스템 문서 (이 디렉토리)
```

### documentation and 로그 구분

| directory | 목적 | 대상 | yes시 |
|---------|------|------|-----|
| `docs/` | system reference documentation | system developer | architecture.md, git-branch-strategy.md |
| `logs-agent_dev/` | system development 로그 | system developer | 20260312-v0.0.2-cleanup.md |
| `team/projects/{name}/logs/` | project implementation 로그 | system user | coding/20260312-PLAN-001.md |
| 루트 `README.md` | user guide | system user | 워크플로우, usage |

---

## 🛠️ system improvement task 유형

### 1. agent add/fix

**location**: `team/.agents/{agent-name}/CLAUDE.md`

**절차**:
1. 새 agent directory create
2. CLAUDE.md 작성 (프롬프트)
3. required 시 templates/ directory add
4. `scripts/run-agent.sh`에 case add
5. test execute
6. documentation update (README.md, architecture.md)

**yes시**:
```bash
# 새 에이전트 추가
mkdir -p team/.agents/devops
vim team/.agents/devops/CLAUDE.md

# run-agent.sh 수정
vim team/scripts/run-agent.sh
# case에 devops 추가

# 테스트
cd team
bash scripts/run-agent.sh devops --help
```

### 2. project type add

**영향 range**:
- `.agents/pm/templates/{new-type}.md`
- `.agents/coding/templates/{new-type}.md`
- `.agents/qa/templates/{new-type}.md`
- `docs/supported-tech-stacks.md`
- `scripts/init-project.sh`

**절차**:
1. project type 정의 (yes: `iot-firmware`)
2. 각 agent template 작성
3. init-project.sh에 type add
4. test project create/validation
5. documentation update

### 3. script improvement

**location**: `team/scripts/`

**주요 script**:
- `init-project.sh`: project initialize
- `run-agent.sh`: agent execute 래퍼
- `git-branch-helper.sh`: Git branch 관리
- `rate-limit-check.sh`: Rate Limit 관리
- `show-logs.sh`: 로그 조회

**절차**:
1. script fix
2. test (다양한 케이스)
3. error process add
4. documentation (comment, README)
5. version commit

### 4. 코딩 룰 add/improvement

**location**: `team/.rules/`

**Structure**:
```
.rules/
├── general-coding-rules.md    # 범용 원칙
├── _verified/                  # 검증된 룰
│   └── {project-type}/
│       └── {framework}-{language}.md
└── _cache/                     # 자동 생성 (24시간)
```

**절차**:
1. Stack Initializer가 create한 룰 검토 (`_cache/`)
2. 실제 사용 후 quality confirmation
3. validation completed 시 `_verified/`로 move
4. file명 rule: `{framework}-{language}.md`

**yes시**:
```bash
# 자동 생성된 룰 확인
cat team/.rules/_cache/cli-tool/cobra-go.md

# 검증 후 이동
mkdir -p team/.rules/_verified/cli-tool
mv team/.rules/_cache/cli-tool/cobra-go.md \
   team/.rules/_verified/cli-tool/

# 커밋
git add team/.rules/_verified/cli-tool/cobra-go.md
git commit -m "rules: verify cobra-go coding rules"
```

---

## 📝 development 로그 작성

### system development 로그 location

`logs-agent_dev/`

### file명 rule

```
YYYYMMDD-{topic}.md
```

**yes시**:
- `20260312-v0.0.2-cleanup.md`
- `20260313-git-branch-improvement.md`
- `20260314-new-agent-design.md`

### 로그 content Structure

```markdown
# {작업 제목}

**날짜**: YYYY-MM-DD
**목적**: 왜 이 작업을 했는가

## 변경 사항

### 추가
- 무엇을 추가했는가

### 수정
- 무엇을 수정했는가

### 삭제
- 무엇을 삭제했는가

## 의사결정

### 선택한 방Plan
설명

### 대Plan
- 대Plan A: 왜 선택하지 않았는가
- 대Plan B: 왜 선택하지 않았는가

## 테스트

수행한 테스트 and 결과

## 다음 작업

향후 개선 사항
```

---

## 🔄 Git 워크플로우

### branch 전략 (system development)

**베이스**: `dev` (system development branch)

**branch pattern**:
```
dev
├── feature/system-{feature-name}
├── fix/system-{bug-name}
└── docs/system-{doc-name}
```

**yes시**:
```bash
git checkout dev
git pull origin dev

# 새 기능 개발
git checkout -b feature/system-iot-firmware-support
# 작업...
git add .
git commit -m "feat: add IoT firmware project type support"
git push origin feature/system-iot-firmware-support
# PR: feature/system-iot-firmware-support → dev
```

### commit message rule

**포맷**:
```
{type}({scope}): {description}

{body}
```

**type**:
- `feat`: 새 feature
- `fix`: bug fix
- `docs`: documentation만 change
- `refactor`: refactoring
- `test`: test add/fix
- `chore`: 빌드, configuration change

**스코프** (optional):
- `agent`: agent 관련
- `script`: script 관련
- `rules`: 코딩 룰 관련
- `docs`: documentation 관련

**yes시**:
```bash
git commit -m "feat(agent): add DevOps agent for CI/CD automation"
git commit -m "fix(script): resolve branch detection in git-branch-helper.sh"
git commit -m "docs: update architecture for v0.0.3"
git commit -m "refactor(rules): restructure _verified directory by project type"
```

---

## 🧪 test

### manual test 체크리스트

새 feature add 시 confirmation 사항:

- [ ] project initialize가 정상 action하는가
- [ ] agent가 올바른 template을 load하는가
- [ ] Git branch가 올바르게 create되는가
- [ ] 로그가 올바른 location에 create되는가
- [ ] Rate Limit 체크가 action하는가
- [ ] multiple project 전환이 action하는가
- [ ] 모든 project type에서 action하는가

### test project create

```bash
cd team

# 각 타입별 테스트 프로젝트 생성
bash scripts/init-project.sh \
  --type web-fullstack \
  --name test-web-app \
  --language python,typescript \
  --framework fastapi,nextjs

bash scripts/init-project.sh \
  --type cli-tool \
  --name test-cli \
  --language go \
  --framework cobra

# 에이전트 실행 테스트
bash scripts/run-agent.sh project-planner \
  --project "Test TODO app"

bash scripts/run-agent.sh pm \
  --ticket-file projects/test-web-app/planning/tickets/PLAN-001*.md

bash scripts/run-agent.sh coding --ticket PLAN-001

bash scripts/run-agent.sh qa --ticket PLAN-001
```

---

## 📚 documentation update

### documentation file location

| file | 목적 | update 시기 |
|------|------|-------------|
| `README.md` (루트) | user guide | user 워크플로우 change 시 |
| `docs/architecture.md` | system 아키텍처 | Structure change 시 |
| `docs/git-branch-strategy.md` | Git branch 전략 | branch 전략 change 시 |
| `docs/supported-tech-stacks.md` | support 스택 list | 새 스택 add 시 |
| `docs/CHANGELOG.md` | change 이력 | 모든 release |
| `docs/contributing.md` | 이 documentation | development 프로세스 change 시 |

### version update

새 version release 시:

1. **CHANGELOG.md update**
   ```markdown
   ## [0.0.3] - 2026-03-15

   ### Added
   - ...

   ### Changed
   - ...
   ```

2. **documentation frontmatter update**
   ```markdown
   **버전**: v0.0.3
   **최종 업데이트**: 2026-03-15
   ```

3. **README.md version tag update**

---

## 🚀 release 프로세스

### version 관리

**version 체계**: Semantic Versioning (Major.Minor.Patch)

- **Major (1.0.0)**: 호환성 깨지는 change
- **Minor (0.1.0)**: 새 feature add (호환 유지)
- **Patch (0.0.1)**: bug fix

**currently version**: `v0.0.2` (beta)

### release 절차

```bash
# 1. dev 브랜치에서 릴리스 준비
git checkout dev
git pull origin dev

# 2. 버전 확인 and 문서 업데이트
vim docs/CHANGELOG.md
# [Unreleased] → [0.0.3]

vim README.md
# 버전 태그 업데이트

# 3. 커밋
git add .
git commit -m "chore: prepare release v0.0.3"

# 4. main에 머지
git checkout main
git merge dev
git tag -a v0.0.3 -m "Release v0.0.3"
git push origin main --tags

# 5. dev 브랜치 동기화
git checkout dev
git merge main
git push origin dev
```

---

## 🔧 트러블슈팅

### often 발생하는 problem

#### Q1. Rate Limit 초과

```bash
# rate-limit-check.sh 확인
bash scripts/rate-limit-check.sh

# 사용량 파싱
python3 scripts/parse_usage.py
```

#### Q2. Git branch create failure

```bash
# 설정 확인
bash scripts/git-branch-helper.sh config

# 수동 브랜치 준비
bash scripts/git-branch-helper.sh prepare coding PLAN-001 user-auth
```

#### Q3. project 컨text 인식 failure

```bash
# .project-config.json 확인
cat team/.project-config.json

# current_project 설정 확인
jq '.current_project' team/.project-config.json
```

---

## 📞 커뮤니케이션

### issue 제기

GitHub Issues 사용

**template**:
```markdown
## 문제 설명
무슨 문제인가?

## 재현 방법
1. ...
2. ...

## 예상 동작
무엇이 일어나야 하는가?

## 실제 동작
무엇이 일어났는가?

## 환경
- OS: macOS/Linux/Windows
- Shell: bash/zsh
- Claude Code 버전: ...
```

### Pull Request

**template**:
```markdown
## 변경 내용
무엇을 변경했는가?

## 목적
왜 변경했는가?

## 테스트
어떻게 테스트했는가?

## 체크리스트
- [ ] 문서 업데이트
- [ ] CHANGELOG.md 업데이트
- [ ] 테스트 Complete
```

---

## 📖 reference 자료

- [Architecture](./architecture.md): system Structure
- [Git Branch Strategy](./git-branch-strategy.md): branch 전략
- [Supported Tech Stacks](./supported-tech-stacks.md): support 스택
- [CHANGELOG](./CHANGELOG.md): change 이력

---

**version**: v0.0.2
**최종 update**: 2026-03-12
