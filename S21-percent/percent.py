#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S21 割合計算 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM は割合の3類型（〜の何%／何%は幾つ／増減率）を取り違える。
このスクリプトはどれも正確に返す。

使い方:
  python percent.py of 25 200        # 200 の 25% = 50
  python percent.py ratio 50 200     # 50 は 200 の 25%
  python percent.py change 200 250   # 200 → 250 は +25%
  python percent.py of 25 200 --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import sys


def pct_of(p, base):
    return base * p / 100


def ratio(part, whole):
    if whole == 0:
        raise ZeroDivisionError("全体が0のため割合を計算できません。")
    return part / whole * 100


def change(old, new):
    if old == 0:
        raise ZeroDivisionError("基準が0のため増減率を計算できません。")
    return (new - old) / old * 100


def main(argv=None):
    p = argparse.ArgumentParser(description="割合を決定論的に計算する手足。")
    p.add_argument("mode", choices=["of", "ratio", "change"],
                   help="of=Yの X%%  ratio=X は Y の何%%  change=旧→新の増減率")
    p.add_argument("x", type=float)
    p.add_argument("y", type=float)
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    try:
        if a.mode == "of":
            val = pct_of(a.x, a.y)
            text = f"{a.y} の {a.x}% = {round(val, 10)}"
        elif a.mode == "ratio":
            val = ratio(a.x, a.y)
            text = f"{a.x} は {a.y} の {round(val, 10)}%"
        else:
            val = change(a.x, a.y)
            text = f"{a.x} → {a.y} は {round(val, 10):+}%"
    except ZeroDivisionError as e:
        if a.json:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
        else:
            print(f"エラー: {e}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps({"mode": a.mode, "x": a.x, "y": a.y, "result": round(val, 10)},
                         ensure_ascii=False))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
