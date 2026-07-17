#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S19 進数変換 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM は桁の多い基数変換で計算を誤る。このスクリプトは
2/8/10/16進を必ず正確に相互変換する（負数・接頭辞も対応）。

使い方:
  python radix.py 255          # 10進として解釈し全基数表示
  python radix.py 0xFF         # 16進入力
  python radix.py 0b1010       # 2進入力
  python radix.py -16 --json   # 機械可読

入力の基数は接頭辞(0x/0o/0b)で自動判定。無ければ10進。

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import sys


def parse_int(s):
    """0x/0o/0b 接頭辞つき、または10進の整数文字列を int に。負号対応。"""
    s = s.strip().replace("_", "")
    neg = s.startswith("-")
    if neg or s.startswith("+"):
        s = s[1:]
    low = s.lower()
    if low.startswith("0x"):
        v = int(s, 16)
    elif low.startswith("0o"):
        v = int(s, 8)
    elif low.startswith("0b"):
        v = int(s, 2)
    else:
        v = int(s, 10)
    return -v if neg else v


def convert(n):
    sign = "-" if n < 0 else ""
    m = abs(n)
    return {
        "dec": str(n),
        "hex": f"{sign}0x{m:x}",
        "oct": f"{sign}0o{m:o}",
        "bin": f"{sign}0b{m:b}",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="2/8/10/16進を決定論的に相互変換する手足。")
    p.add_argument("input", help="変換する数（0x/0o/0b 接頭辞で入力基数を指定可）")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    try:
        n = parse_int(a.input)
    except ValueError:
        msg = f"数として解釈できません: {a.input!r}"
        if a.json:
            print(json.dumps({"error": msg, "input": a.input}, ensure_ascii=False))
        else:
            print(f"エラー: {msg}", file=sys.stderr)
        return 2

    res = convert(n)
    if a.json:
        print(json.dumps({"input": a.input, **res}, ensure_ascii=False))
    else:
        print(f"10進 {res['dec']}")
        print(f"16進 {res['hex']}")
        print(f"8進  {res['oct']}")
        print(f"2進  {res['bin']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
