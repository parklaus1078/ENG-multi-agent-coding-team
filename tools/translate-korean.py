#!/usr/bin/env python3
"""
Detect and help translate Korean text in files.
Usage: python tools/translate-korean.py <file_path>
       python tools/translate-korean.py --batch <directory>
"""

import re
import sys
import os
from pathlib import Path

def find_korean_lines(file_path):
    """Find all lines containing Korean characters."""
    korean_pattern = re.compile(r'[가-힣ㄱ-ㅎㅏ-ㅣ]+')

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return []

    korean_lines = []
    for i, line in enumerate(lines, 1):
        if korean_pattern.search(line):
            korean_lines.append((i, line.rstrip()))

    return korean_lines

def scan_directory(directory, extensions=None):
    """Scan directory for files with Korean text."""
    if extensions is None:
        extensions = ['.md', '.py', '.js', '.html', '.sh', '.json']

    korean_pattern = re.compile(r'[가-힣ㄱ-ㅎㅏ-ㅣ]+')
    files_with_korean = []

    for ext in extensions:
        for file_path in Path(directory).rglob(f'*{ext}'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if korean_pattern.search(content):
                        korean_lines = len([line for line in content.split('\n')
                                           if korean_pattern.search(line)])
                        files_with_korean.append((str(file_path), korean_lines))
            except Exception as e:
                pass  # Skip files that can't be read

    return sorted(files_with_korean, key=lambda x: x[1], reverse=True)

def main():
    if len(sys.argv) < 2:
        print("Usage: python translate-korean.py <file_path>")
        print("       python translate-korean.py --batch <directory>")
        sys.exit(1)

    if sys.argv[1] == '--batch':
        if len(sys.argv) < 3:
            print("Error: --batch requires a directory path")
            sys.exit(1)

        directory = sys.argv[2]
        print(f"🔍 Scanning {directory} for Korean text...\n")

        files_with_korean = scan_directory(directory)

        if not files_with_korean:
            print("✅ No Korean text found in any files!")
            return

        print(f"📊 Found {len(files_with_korean)} files with Korean text:\n")
        print("File Path | Lines with Korean")
        print("-" * 80)

        total_lines = 0
        for file_path, line_count in files_with_korean:
            # Make path relative for readability
            rel_path = os.path.relpath(file_path, directory)
            print(f"{rel_path:60s} | {line_count:4d} lines")
            total_lines += line_count

        print("-" * 80)
        print(f"Total: {len(files_with_korean)} files, {total_lines} lines with Korean text")

    else:
        file_path = sys.argv[1]

        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            sys.exit(1)

        korean_lines = find_korean_lines(file_path)

        if not korean_lines:
            print(f"✅ No Korean text found in {file_path}")
            return

        print(f"📝 Found {len(korean_lines)} lines with Korean text in {file_path}:\n")
        for line_num, line in korean_lines:
            # Highlight Korean text
            korean_pattern = re.compile(r'([가-힣ㄱ-ㅎㅏ-ㅣ]+)')
            highlighted = korean_pattern.sub(r'[\033[93m\1\033[0m]', line)
            print(f"Line {line_num:4d}: {highlighted}")

        print(f"\n📊 Total lines needing translation: {len(korean_lines)}")

if __name__ == '__main__':
    main()
