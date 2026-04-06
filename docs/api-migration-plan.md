# Multi-Agent Coding Tool - API Migration Plan

**Date**: 2026-03-16
**Goal**: Transition from Claude Code CLI to Anthropic API-based system for fully automated agentic coding tool

---

## 📋 Table of Contents

1. [Current Status Analysis](#1-current-status-analysis)
2. [Goal and Requirements](#2-goal-and-requirements)
3. [Technical Stack Comparison](#3-technical-stack-comparison)
4. [Architecture Design](#4-architecture-design)
5. [Implementation Plan](#5-implementation-plan)
6. [Cost Analysis](#6-cost-analysis)
7. [Risk Management](#7-risk-management)
8. [Milestones](#8-milestones)

---

## 1. Current Status Analysis

### 1.1 Current System (v0.0.2)

**Structure:**
```
Shell Script (auto-pipeline.sh)
  ↓
Claude Code CLI (대화형)
  ↓
수동 Ctrl+C 종료
```

**장점:**
- ✅ 빠른 프로토type
- ✅ Claude Code Max subscribe 활용
- ✅ ticket별 execute 잘 작동

**단점:**
- ❌ automation 불완전 (manual 개입 required)
- ❌ Follow-up question 시 waiting
- ❌ 프로그래밍 방식 제어 불가
- ❌ error 핸들링 제한적
- ❌ logging/모니터링 어려움

### 1.2 사용 pattern analytics

**ticket별 execute (Manual Mode):**
- frequency: 80%
- 사용 케이스: 복잡한 feature, 실험적 development
- Requirements: 대화형, 사람 개입 가능

**all auto execute (Auto-Pipeline):**
- frequency: 20%
- 사용 케이스: 명확한 Requirements, 반복 task
- Requirements: 완전 automation, 무인 execute

---

## 2. Goal and Requirements

### 2.1 핵심 Goal

1. **완전 automation**: Follow-up question auto response, 무인 execute
2. **비용 효율**: 장기적으로 Claude Code Max보다 저렴
3. **유지보수성**: 확장 가능하고 관리 쉬운 code베이스
4. **양립 가능**: Manual/Auto mode all support

### 2.2 feature Requirements

**Must Have:**
- [ ] ticket별 execute (Manual Mode)
- [ ] all ticket auto execute (Auto-Pipeline)
- [ ] auto response system
- [ ] session save and resume
- [ ] Rate limit auto 관리
- [ ] Git auto commit/push
- [ ] Progress상황 save/restore

**Should Have:**
- [ ] error auto 복구 (재시도)
- [ ] 상세 logging/모니터링
- [ ] 비용 추적
- [ ] 대화 히스토리 analytics

**Nice to Have:**
- [ ] Multi-agent parallel execute
- [ ] learning 기반 auto response improvement
- [ ] Web UI
- [ ] Slack/Discord notification

---

## 3. Technical Stack Comparison

### 3.1 Claude Code CLI vs Anthropic API

| 항목 | Claude Code CLI | Anthropic API |
|------|----------------|---------------|
| **비용 model** | 월 subscribe ($110) | 사용량 기반 (~$50/월 yes상) |
| **제어 수준** | 제한적 (CLI interface) | 완전 제어 (Python API) |
| **automation** | part적 (--print mode) | 완벽 (프로그래밍) |
| **대화 관리** | auto (내장) | manual (code 작성) |
| **error 핸들링** | 제한적 | 완전 제어 |
| **logging** | 제한적 | 완전 제어 |
| **확장성** | 낮음 | 높음 |
| **러닝 커브** | 낮음 | 중간 |

### 3.2 optional 근거

**Anthropic API optional 이유:**

1. **비용**: 월 $50 yes상 vs $110 (45% 절감)
2. **automation**: 100% 무인 execute 가능
3. **확장성**: future feature add 용이
4. **제어**: 모든 stage 세밀 제어

**리스크:**
- 초기 development time (2-4주)
- code 복잡도 increase
- API change 대응 required

---

## 4. Architecture Design

### 4.1 system Structure

```
┌─────────────────────────────────────────┐
│         CLI Interface                    │
│  python auto_pipeline.py [options]       │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      Pipeline Controller                 │
│  - Mode selection (manual/auto)         │
│  - Ticket orchestration                 │
│  - Progress management                  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         Agent System                     │
│  ┌─────────┬─────────┬─────────┐       │
│  │   PM    │ Coding  │   QA    │       │
│  └─────────┴─────────┴─────────┘       │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      Anthropic API Client                │
│  - Message management                   │
│  - Auto-response engine                 │
│  - Session persistence                  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│    Infrastructure Services               │
│  - Git operations                       │
│  - File I/O                             │
│  - Logging                              │
│  - Cost tracking                        │
└─────────────────────────────────────────┘
```

### 4.2 핵심 컴포넌트

#### 4.2.1 Pipeline Controller

```python
class PipelineController:
    """
    파이프라인 전체 오케스트레이션

    책임:
    - Ticket 로딩 and 순서 관리
    - Agent 실행 조율
    - Progress상황 관리
    - 에러 처리 and 복구
    """

    def run_manual_mode(self, ticket_num: str)
    def run_auto_mode(self, resume: bool = False)
    def save_progress(self, ticket_num: str, step: str)
    def load_progress(self) -> dict
```

#### 4.2.2 Agent System

```python
class BaseAgent:
    """
    모든 에이전트의 베이스 클래스

    책임:
    - System prompt 로딩
    - 대화 관리
    - 자동 응답 규칙 적용
    - Complete 감지
    """

    def run(self, prompt: str, auto_respond: bool) -> ConversationResult
    def is_complete(self, message: str) -> bool
    def auto_reply(self, message: str) -> Optional[str]

class PMAgent(BaseAgent):
    """PM 특화 로직"""

class CodingAgent(BaseAgent):
    """Coding 특화 로직"""

class QAAgent(BaseAgent):
    """QA 특화 로직"""
```

#### 4.2.3 Auto-Response Engine

```python
class AutoResponseEngine:
    """
    자동 응답 규칙 관리

    책임:
    - 패턴 매칭
    - 컨텍스트 기반 응답 선택
    - 학습 데이터 수집 (미래)
    """

    rules: Dict[str, ResponseRule]

    def match_pattern(self, message: str) -> Optional[str]
    def add_rule(self, pattern: str, response: str)
    def learn_from_history(self, conversations: List[Conversation])
```

#### 4.2.4 Session Manager

```python
class SessionManager:
    """
    세션 저장 and 재개

    책임:
    - 대화 히스토리 저장
    - 세션 복원
    - 메타데이터 관리
    """

    def save_session(self, ticket_num: str, agent: str, messages: List)
    def load_session(self, ticket_num: str, agent: str) -> List
    def list_sessions(self) -> List[SessionInfo]
```

### 4.3 data model

```python
@dataclass
class Ticket:
    number: str          # "PLAN-001"
    title: str
    content: str
    status: TicketStatus  # pending, pm_done, coding_done, qa_done, completed

@dataclass
class ConversationResult:
    messages: List[Message]
    completed: bool
    session_id: str
    cost: float

@dataclass
class Message:
    role: str  # "user" | "assistant"
    content: str
    timestamp: datetime

@dataclass
class PipelineProgress:
    last_ticket: str
    last_step: str  # "pm" | "coding" | "qa"
    timestamp: datetime
    total_cost: float
```

---

## 5. Implementation Plan

### 5.1 Phase 1: default 인프라 (Week 1-2)

**Goal**: API 기반 single ticket execute

**task:**
- [ ] `anthropic` library installation and configuration
- [ ] `BaseAgent` class implementation
- [ ] `PMAgent`, `CodingAgent`, `QAAgent` implementation
- [ ] single ticket manual mode 작동
- [ ] default logging system

**산출물:**
```python
# 실행 예시
python auto_pipeline.py --ticket PLAN-001 --mode manual
```

**test:**
- PLAN-001 ticket으로 PM → Coding → QA all 플로우 success

---

### 5.2 Phase 2: auto response system (Week 3)

**Goal**: Follow-up question auto process

**task:**
- [ ] `AutoResponseEngine` implementation
- [ ] default response rule 정의
- [ ] pattern 매칭 로직
- [ ] Auto mode implementation

**response rule yes시:**
```python
AUTO_RESPONSE_RULES = {
    r".*추가.*할까요.*\?": "no, 티켓 범위 내에서만 Progress",
    r".*변경.*할까요.*\?": "no, 현재 명세대로",
    r".*확인.*필요.*\?": "yes, 계속 Progress",
    r".*리팩토링.*\?": "no, 현재 티켓만 집중",
}
```

**산출물:**
```python
# 실행 예시
python auto_pipeline.py --ticket PLAN-001 --mode auto
```

**test:**
- Follow-up question 5개 시나리오에서 auto response success

---

### 5.3 Phase 3: all pipeline (Week 4)

**Goal**: all ticket auto execute

**task:**
- [ ] `PipelineController` implementation
- [ ] ticket 순회 로직
- [ ] Progress상황 save/restore
- [ ] Git auto commit/push
- [ ] Rate limit 체크 통합

**산출물:**
```python
# 실행 예시
python auto_pipeline.py --mode auto --all-tickets
python auto_pipeline.py --mode auto --resume
```

**test:**
- 5개 ticket project 무인 execute success
- stop 후 resume success

---

### 5.4 Phase 4: advanced feature (Week 5-6)

**Goal**: Production-ready feature

**task:**
- [ ] error auto 복구 (재시도 로직)
- [ ] 상세 logging (file별, 타임스탬프)
- [ ] 비용 추적 and report
- [ ] session 관리 improvement
- [ ] performance optimization

**산출물:**
```python
# 비용 리포트
python auto_pipeline.py --cost-report

# 세션 목록
python auto_pipeline.py --list-sessions

# 재시도
python auto_pipeline.py --retry-failed
```

---

### 5.5 Phase 5: 병행 운영 and 전환 (Week 7-8)

**Goal**: Shell script → Python 완전 전환

**task:**
- [ ] 기존 shell script와 병행 운영
- [ ] 비용/performance compare 측정
- [ ] user guide 작성
- [ ] Migration script 작성
- [ ] 기존 system deprecated 마킹

**의사결정 기준:**
```
비용 비교:
- Shell script (Claude Code Max): $110/month
- Python (Anthropic API): $XX/month

Performance 비교:
- 자동화율: Shell XX% vs Python XX%
- 에러율: Shell XX% vs Python XX%
- 평균 실행 시간: Shell XXm vs Python XXm

→ Python이 더 저렴하고 자동화율 높으면 전환
```

---

## 6. Cost Analysis

### 6.1 yes상 사용량

**가정:**
- 월 5개 project development
- project당 average 20개 ticket
- ticket당 3stage (PM, Coding, QA)

**총 request:**
- 5 project × 20 ticket × 3 agent = **300 request/월**

### 6.2 token 사용량 추정

**PM Agent (ticket당):**
```
Input:
  - 티켓 내용: 1,000 tokens
  - System prompt: 2,000 tokens
  - 총: 3,000 tokens

Output:
  - 명세서: 5,000 tokens

비용: 3K × $3/1M + 5K × $15/1M = $0.084
```

**Coding Agent (ticket당):**
```
Input:
  - 명세서: 5,000 tokens
  - System prompt: 2,000 tokens
  - 코드 참조: 3,000 tokens
  - 총: 10,000 tokens

Output:
  - 코드: 10,000 tokens

비용: 10K × $3/1M + 10K × $15/1M = $0.18
```

**QA Agent (ticket당):**
```
Input:
  - 테스트케이스: 3,000 tokens
  - System prompt: 2,000 tokens
  - 총: 5,000 tokens

Output:
  - 테스트 코드: 8,000 tokens

비용: 5K × $3/1M + 8K × $15/1M = $0.135
```

**ticket당 총 비용:**
```
$0.084 + $0.18 + $0.135 = $0.40/티켓
```

### 6.3 월간 비용 추정

**default 시나리오:**
```
100 티켓/월 × $0.40 = $40/월
```

**여유분 (재시도, 실험, fix):**
```
+30% = $12/월
```

**총 yes상 비용:**
```
$52/월
```

**Claude Code Max 대비:**
```
절감액: $110 - $52 = $58/월 (53% 절감)
연간: $696 절감
```

### 6.4 비용 optimization 전략

**단기:**
- Prompt optimization (불required한 token remove)
- Caching 활용 (system prompt 캐싱)

**중기:**
- Batch API 활용 (50% discount)
- model optional optimization (Haiku for simple tasks)

**장기:**
- Fine-tuning으로 prompt zoom out
- Self-hosting 고려

---

## 7. Risk Management

### 7.1 기술 리스크

| 리스크 | 영향도 | 가능성 | 완화 방Plan |
|--------|--------|--------|-----------|
| API change | 높음 | 낮음 | version 핀닝, 정기 update 체크 |
| Rate limit 초과 | 중간 | 중간 | auto 재시도, 백오프 전략 |
| 비용 초과 | 중간 | 낮음 | 비용 모니터링, yes산 notification |
| auto response failure | 중간 | 중간 | Fallback 전략, manual 개입 |

### 7.2 운영 리스크

| 리스크 | 영향도 | 가능성 | 완화 방Plan |
|--------|--------|--------|-----------|
| 마이그레이션 failure | 높음 | 낮음 | 병행 운영, 롤백 Plan |
| learning 곡선 | 낮음 | 중간 | 상세 documentation, example 제공 |
| 유지보수 부담 | 중간 | 중간 | module화, test code |

### 7.3 비용 리스크

**시나리오 analytics:**

**Best Case (월 $30):**
- 효율적인 prompt
- 재시도 minimize
- Batch API 활용

**Base Case (월 $52):**
- currently 추정치

**Worst Case (월 $80):**
- 비효율적 사용
- 많은 재시도
- 실험 많음

**대응:**
- 월 $100 초과 시 notification
- Cost Analysis report 주간 create
- required 시 Claude Code로 롤백

---

## 8. Milestones

### 8.1 development 일정

```
Week 1-2: Phase 1 - 기본 인프라
  ├─ Day 1-3: API 연동 and BaseAgent
  ├─ Day 4-7: PM/Coding/QA Agent 구현
  └─ Day 8-10: 통합 테스트

Week 3: Phase 2 - 자동 응답
  ├─ Day 11-13: AutoResponseEngine
  └─ Day 14-15: Auto 모드 테스트

Week 4: Phase 3 - 전체 파이프라인
  ├─ Day 16-18: PipelineController
  ├─ Day 19-20: Git 통합
  └─ Day 21-22: 전체 테스트

Week 5-6: Phase 4 - 고급 기능
  ├─ Week 5: 에러 처리, 로깅
  └─ Week 6: 비용 추적, 최적화

Week 7-8: Phase 5 - 병행 운영
  ├─ Week 7: 병행 운영, 비용 측정
  └─ Week 8: 의사결정, 전환 or 롤백
```

### 8.2 success 기준

**MVP (Week 4 completed 시):**
- [ ] single ticket manual mode 100% success
- [ ] single ticket auto mode 80% success (auto response)
- [ ] all ticket auto mode 70% success (5개 ticket)

**Production (Week 8 completed 시):**
- [ ] all ticket auto mode 90% success
- [ ] 월 비용 $60 이하
- [ ] error 복구율 95% 이상
- [ ] documentation completed

---

## 9. next stage

### 9.1 immediately execute (this 주)

1. **의사결정**: API 마이그레이션 Progress 여부 최종 confirmation
2. **환경 configuration**: Anthropic API 키 발급, development 환경 구축
3. **킥오프**: Phase 1 start

### 9.2 체크points

**Week 2 exit 시:**
- Phase 1 completed confirmation
- single ticket manual mode 작동 validation
- Go/No-go 결정

**Week 4 exit 시:**
- MVP 완성 confirmation
- 초기 비용 측정
- 전환 여부 yes비 결정

**Week 8 exit 시:**
- 최종 비용/performance compare
- 전환 or 롤백 최종 결정

---

## 10. 부록

### 10.1 reference 자료

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Claude Sonnet 4.5 Pricing](https://www.anthropic.com/pricing)
- [Best Practices for Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)

### 10.2 FAQ

**Q: 기존 shell script는 어떻게 되나요?**
A: Week 8까지 병행 운영 후, Python이 더 나으면 deprecated process.

**Q: 비용이 yes상보다 높으면?**
A: 월 $100 초과 시 Claude Code Max로 롤백 가능.

**Q: development duration 중 project는 어떻게 Progress하나요?**
A: 기존 shell script continue 사용하면서 병행 development.

**Q: API 키 관리는?**
A: 환경variable `.env` file로 관리, git에 commit Plan 함.

---

## 11. approval

이 기획Plan에 대한 approval and feedback:

- [ ] **approval**: API 마이그레이션 Progress
- [ ] **pending**: add 검토 required
- [ ] **rejection**: Current System 유지

**feedback:**
```
(여기에 의견 작성)
```

---

**documentation version**: v1.0
**최종 fix**: 2026-03-16
**작성자**: Claude Sonnet 4.5
