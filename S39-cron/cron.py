#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S39 Cron式ビルダー/読み解き — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM は cron 式(分 時 日 月 曜日)の読み解きを誤り、
「毎日9時」のつもりが違う時刻になる事故を起こす。このスクリプトは
実際にフィールドを展開して検証し、日本語で正確に説明する。

使い方:
  python cron.py "0 9 * * 1-5"      # 平日9:00
  python cron.py "*/15 * * * *"     # 15分ごと
  python cron.py "0 9 * * 1-5" --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import sys

WEEK = {0: "日", 1: "月", 2: "火", 3: "水", 4: "木", 5: "金", 6: "土"}
ALL_MIN = set(range(60))
ALL_HOUR = set(range(24))
ALL_DOM = set(range(1, 32))
ALL_MON = set(range(1, 13))
ALL_DOW = set(range(7))


def parse_field(expr, lo, hi):
    """cron の1フィールドを展開して値の集合にする。"""
    values = set()
    for part in expr.split(","):
        step = 1
        if "/" in part:
            part, st = part.split("/", 1)
            if not st.isdigit() or int(st) < 1:
                raise ValueError(f"不正なステップ: /{st}")
            step = int(st)
        if part == "*":
            start, end = lo, hi
        elif "-" in part.lstrip("-"):
            a, b = part.split("-", 1)
            start, end = int(a), int(b)
        else:
            start = end = int(part)
            if step != 1:
                end = hi  # 例: 5/10 は 5 から step10 で hi まで
        if start < lo or end > hi or start > end:
            raise ValueError(f"範囲外の値: {expr}（許容 {lo}-{hi}）")
        values.update(range(start, end + 1, step))
    if not values:
        raise ValueError(f"値が空です: {expr}")
    return values


def describe(expression):
    fields = expression.split()
    if len(fields) != 5:
        raise ValueError("cron式は5フィールド（分 時 日 月 曜日）で指定してください。")
    try:
        mins = parse_field(fields[0], 0, 59)
        hours = parse_field(fields[1], 0, 23)
        dom = parse_field(fields[2], 1, 31)
        mon = parse_field(fields[3], 1, 12)
        dow = {d % 7 for d in parse_field(fields[4], 0, 7)}
    except (ValueError, TypeError) as e:
        raise ValueError(f"不正なcron式: {e}")

    seg = []
    if mon != ALL_MON:
        seg.append("・".join(f"{m}月" for m in sorted(mon)))
    if dow != ALL_DOW:
        seg.append("毎週" + "・".join(WEEK[d] for d in sorted(dow)))
    elif dom != ALL_DOM:
        seg.append("毎月" + "・".join(f"{d}日" for d in sorted(dom)))
    else:
        seg.append("毎日")

    if fields[0].startswith("*/") and hours == ALL_HOUR:
        seg.append(f"{fields[0][2:]}分ごと")
    elif len(hours) == 1 and len(mins) == 1:
        seg.append(f"{sorted(hours)[0]}:{sorted(mins)[0]:02d}")
    elif len(hours) == 1:
        seg.append(f"{sorted(hours)[0]}時の{','.join(str(m) for m in sorted(mins))}分")
    elif len(mins) == 1 and hours == ALL_HOUR:
        seg.append(f"毎時{sorted(mins)[0]}分")
    else:
        seg.append("時" + ",".join(map(str, sorted(hours)))
                  + " 分" + ",".join(map(str, sorted(mins))))

    return {
        "expression": expression,
        "valid": True,
        "description": " ".join(seg),
        "fields": {
            "minute": sorted(mins), "hour": sorted(hours),
            "day_of_month": sorted(dom), "month": sorted(mon),
            "day_of_week": sorted(dow),
        },
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="cron式を検証し日本語で説明する手足。")
    p.add_argument("expression", help='cron式（例: "0 9 * * 1-5"）')
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    try:
        r = describe(a.expression)
    except ValueError as e:
        if a.json:
            print(json.dumps({"expression": a.expression, "valid": False,
                              "error": str(e)}, ensure_ascii=False))
        else:
            print(f"エラー: {e}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        print(r["description"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
