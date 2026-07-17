#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S29 割り勘計算 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: 端数を含む割り勘の「誰がいくら」を公平に、合計がちょうど合う形で返す。
LLM は端数配分で合計が合わなくなりがち。

使い方:
  python splitbill.py 10000 3      # 合計10000を3人で
  python splitbill.py 10000 3 --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import sys


def split(total, people):
    if people <= 0:
        raise ValueError("人数は1以上で指定してください。")
    total = int(total)
    base = total // people
    rem = total % people  # base+1 を払う人数
    breakdown = (f"{rem}人が{base + 1}円、{people - rem}人が{base}円"
                 if rem else f"{people}人が{base}円")
    return {
        "total": total,
        "people": people,
        "base": base,
        "extra_payers": rem,          # base+1 円を払う人数
        "extra_amount": base + 1 if rem else base,
        "breakdown": breakdown,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="端数込みの割り勘を決定論的に計算する手足。")
    p.add_argument("total", type=float, help="合計金額(円)")
    p.add_argument("people", type=int, help="人数")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    try:
        r = split(a.total, a.people)
    except ValueError as e:
        if a.json:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
        else:
            print(f"エラー: {e}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        print(r["breakdown"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
