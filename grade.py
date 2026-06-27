#!/usr/bin/env python3
"""
grade.py

Simple grade calculator CLI that mirrors the frontend logic:
- validate score (0-100)
- compute grade A/B/C/D/F
- description text
- append history to `grade_history.txt`

Usage:
  python grade.py 85
  python grade.py --interactive
"""
from __future__ import annotations
import sys
import argparse
from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path(__file__).with_name('grade_history.txt')

def compute_grade(score: float) -> str:
    if score >= 80:
        return 'A'
    if score >= 70:
        return 'B'
    if score >= 60:
        return 'C'
    if score >= 50:
        return 'D'
    return 'F'

def grade_description(g: str) -> str:
    return {
        'A': 'คะแนนดีเยี่ยม',
        'B': 'คะแนนดี',
        'C': 'คะแนนพอใช้',
        'D': 'คะแนนต้องปรับปรุง',
        'F': 'สอบตก',
    }.get(g, '')

def validate_score(n: float) -> bool:
    return 0 <= n <= 100

def append_history(score: float, grade: str) -> None:
    txt = f"{datetime.now().isoformat(sep=' ', timespec='seconds')} - คะแนน: {score} -> เกรด {grade}\n"
    try:
        HISTORY_FILE.open('a', encoding='utf-8').write(txt)
    except Exception as e:
        print(f"ไม่สามารถบันทึกประวัติ: {e}")

def run_score(score: float) -> int:
    if not validate_score(score):
        print('คะแนนไม่ถูกต้อง: ต้องเป็นตัวเลขระหว่าง 0 ถึง 100')
        return 2
    grade = compute_grade(score)
    desc = grade_description(grade)
    print(f"คะแนน: {score} -> เกรด {grade}")
    print(desc)
    append_history(score, grade)
    return 0

def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(description='Grade calculator CLI')
    parser.add_argument('score', nargs='?', type=float, help='score 0-100')
    parser.add_argument('--interactive', '-i', action='store_true', help='interactive prompt')
    args = parser.parse_args(argv)

    if args.interactive or args.score is None:
        try:
            raw = input('ใส่คะแนน (0-100): ').strip()
            score = float(raw)
        except Exception:
            print('ป้อนค่าผิดพลาด ต้องเป็นตัวเลข')
            return 2
        return run_score(score)

    return run_score(args.score)

if __name__ == '__main__':
    raise SystemExit(main())
