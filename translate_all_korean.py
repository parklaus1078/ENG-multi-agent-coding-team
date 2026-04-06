#!/usr/bin/env python3
"""
Comprehensive Korean to English translator for all code files
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Translation dictionary - comprehensive mapping
TRANSLATIONS = {
    # Common terms
    "기반": "based",
    "클라이언트": "client",
    "자동": "auto",
    "규칙": "rules",
    "load": "load",
    "에previous트": "agent",
    "execute": "execute",
    "프롬프트": "prompt",
    "대화": "conversation",
    "히스토리": "history",
    "additional": "add",
    "message": "message",
    "content": "content",
    "completed": "completed",
    "task": "task",
    "question": "question",
    "response": "response",
    "in progress": "in progress",
    "currently": "currently",
   "계획대로": "as planned",
    "please": "please",
    "confirmation": "check",
    "감지": "detect",
    "매칭된": "matched",
    "참조": "reference",
    "error": "error",
    "warning": "warning",
    "정보": "information",
    "save": "save",
    "session": "session",
    "맵": "map",
    "update": "update",
    "상태": "status",
    "타임스탬프": "timestamp",
    "번호": "number",
    "티켓": "ticket",
    "파일": "file",
    "디렉토리": "directory",
    "프로젝트": "project",
    "전체": "entire",
    "파이프라인": "pipeline",
    "티켓": "ticket",
    "총": "total",
    "개": "items",
    "이미": "already",
    "스킵": "skip",
    "재개": "resume",
    "다음": "next",
    "단계": "stage",
    "시작": "start",
    "읽기": "read",
    "내용": "content",
    "명세서": "specification",
    "검증": "validation",
    "중": "in progress",
    "통과": "passed",
    "실패": "failed",
    "재시행": "retry",
    "필수": "필수",
    "수동": "manual",
    "개입": "intervention",
    "구현": "implementation",
    "코드": "code",
    "리팩토링": "refactoring",
    "제안": "suggestion",
    "확인": "check",
    "발견": "found",
    "가능한": "possible",
    "fix": "fix",
    "테스트": "test",
    "작성": "write",
    "실행": "execute",
    "모든": "all",
    "커버리지": "coverage",
    "커밋": "commit",
    "생성": "generate",
    "스킬": "skill",
    "documentation": "documentation",
    "변경사항": "changes",
    "변경": "change",
    "여부": "whether",
    "관련": "related",
    "현재": "current",
    "다음": "next",
    "이전": "previous",
    "간단한": "simple",
    "복잡한": "complex",
    "기능": "feature",
    "추가": "add",
    "삭제": "delete",
    "수정": "modify",
    "조회": "query",
    "취소": "cancel",
    "제거": "remove",
    "목록": "list",
    "상세": "detail",
    "요약": "summary",
    "결과": "result",
    "성공": "success",
    "실패": "failure",
    "경로": "path",
    "라우트": "route",
    "옵션": "option",
    "선택": "select",
    "이동": "move",
    "대기": "wait",
    "pending": "pending",
    "지침": "instruction",
    "창": "window",
    "입력": "input",
    "흐름": "flow",
    "전용": "only",
    "지원": "support",
    "활성화": "enabled",
    "모드": "mode",
    "타입": "type",
    "텍스트": "text",
    "형식": "format",
    "타이틀": "title",
    "설정": "configuration",
    "백그라운드": "background",
    "알림": "notification",
    "실행중": "running",
    "리스트": "list",
    "카테고리": "category",
    "설명": "description",
    "엔드포인트": "endpoint",
    "제품": "product",
    "기획": "planning",
    "구조화된": "structured",
    "산출물": "deliverable",
    "변환": "convert",
    "맞춰": "according to",
    "초기": "initial",
    "스택": "stack",
    "공통": "common",
    "로직": "logic",
    "available한": "available",
    "이슈": "issue",
    "제안": "suggestion",
    "제시": "present",
    "제시된": "suggested",
    "사용": "use",
    "필요": "need",
    "가능": "possible",
    "없음": "없음",
    "찾을 수 없습니다": "not found",
    "찾기": "find",
    "찾아": "find",
    "new운": "new",
    "중요": "important",
    "전략": "strategy",
    "대화형": "interactive",
    "특성": "characteristic",
    "활용한": "utilizing",
    "각": "each",
    "마다": "per",
    "터미널": "terminal",
    "탭": "tab",
    "유지": "maintain",
    "유지하여": "maintaining",
    "나중에": "later",
    "복귀": "return",
    "기록": "record",
    "관리": "management",
    "간": "between",
    "순차": "sequential",
    "아키텍처": "architecture",
    "별도": "separate",
    "종료하지": "not exit",
    "않음": "not",
    "기반": "based",
    "맵": "map",
    "및": "and",
    "환경": "environment",
    "통해": "through",
    "최종": "final",
    "조합": "combination",
    "create": "create",
    "open": "open",
    "delay": "delay",
    "echo": "echo",
    "cat": "cat",
    "copy": "copy",
    "붙여넣으세요": "paste",
    "위": "above",
    "claude": "claude",
    "기존": "existing",
    "요약": "summary",
    "시도": "try",
    "인덱스": "index",
    "부분": "part",
    "부품": "component",
    "컨텍스트": "context",
    "대기중": "waiting",
    "진행중": "in progress",
    "이": "this",
    "그": "the",
    "으로": "to",
    "에서": "from",
    "와": "with",
    "를": "to",
    "가": "is",
    "은": "is",
    "의": "of",
    "에": "to",
    "을": "to",
    "고": "and",
    "후": "after",
    "누르세요": "press",
    "패턴": "pattern",
    "메인": "main",
    "함수": "function",
    "help": "help",
    "생략": "omit",
    "시": "when",
    "예": "example",
    "필드": "field",
    "값": "value",
    "색상": "color",
    "파란색": "blue",
    "빨간색": "red",
    "노란색": "yellow",
    "녹색": "green",
    "계속": "continue",
    "열려있습니다": "remain open",
    "수정": "modification",
    "다시": "again",
    "대화": "conversation",
    "이어가기": "continue",
    "팁": "tip"
}

def translate_korean_to_english(text: str) -> str:
    """Translate Korean text to English using dictionary"""
    # This is a simplified translator - in real use, would use proper translation API
    result = text

    # Translate known patterns
    for ko, en in TRANSLATIONS.items():
        result = result.replace(ko, en)

    return result

def has_korean(text: str) -> bool:
    """Check if text contains Korean characters"""
    return bool(re.search('[가-힣]', text))

def find_korean_in_file(file_path: Path) -> List[Tuple[int, str]]:
    """Find lines with Korean in a file"""
    korean_lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if has_korean(line):
                    korean_lines.append((line_num, line.rstrip()))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return korean_lines

def main():
    """Main function to scan and report Korean text"""
    base_dir = Path("/Users/geunwoopark/Desktop/multi_agent_coding_team/ENG-multi-agent-coding-team/team")

    # File extensions to check
    extensions = ['.py', '.js', '.json', '.sh']

    total_files = 0
    files_with_korean = 0
    total_korean_lines = 0

    print("="*80)
    print("KOREAN TEXT DETECTION REPORT")
    print("="*80)
    print()

    for ext in extensions:
        print(f"\n{'='*80}")
        print(f"Checking {ext} files...")
        print('='*80)

        for file_path in base_dir.rglob(f'*{ext}'):
            if '.git' in str(file_path):
                continue

            total_files += 1
            korean_lines = find_korean_in_file(file_path)

            if korean_lines:
                files_with_korean += 1
                total_korean_lines += len(korean_lines)

                rel_path = file_path.relative_to(base_dir.parent)
                print(f"\n📄 {rel_path}")
                print(f"   Found {len(korean_lines)} lines with Korean:")

                for line_num, line in korean_lines[:5]:  # Show first 5
                    print(f"   Line {line_num}: {line[:100]}")

                if len(korean_lines) > 5:
                    print(f"   ... and {len(korean_lines) - 5} more lines")

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total files scanned: {total_files}")
    print(f"Files with Korean: {files_with_korean}")
    print(f"Total lines with Korean: {total_korean_lines}")
    print("="*80)

if __name__ == "__main__":
    main()
