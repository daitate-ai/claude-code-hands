#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
O3 本物の乱数 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM に「1〜100で適当に」と頼むと乱数にならない。人間同様に
特定の数(37, 42, 73…)へ強く偏る。このスクリプトは OS の暗号学的乱数
(secrets)を使い、偏りのない選択・シャッフルを行う。

使い方:
  python rand.py int 1 100            # 範囲の整数
  python rand.py int 1 6 --count 5
  python rand.py choice りんご みかん ぶどう
  python rand.py shuffle a b c d
  python rand.py dice 2d6             # サイコロ
  python rand.py int 1 100 --json

依存: なし(Python 3.8+ 標準ライブラリ secrets のみ)
"""

import argparse
import json
import re
import secrets
import sys


def rand_int(low, high):
    """low..high(両端含む)の一様乱数。"""
    if low > high:
        raise ValueError("low は high 以下にしてください。")
    return low + secrets.randbelow(high - low + 1)


def choice(seq):
    if not seq:
        raise ValueError("選択肢が空です。")
    return secrets.choice(seq)


def shuffle(seq):
    """Fisher-Yates を secrets で。元のリストは変更しない。"""
    items = list(seq)
    for i in range(len(items) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        items[i], items[j] = items[j], items[i]
    return items


def roll(spec):
    """'2d6' 形式を振る。戻り値は (各出目, 合計)。"""
    m = re.fullmatch(r"(\d*)d(\d+)", spec.strip(), re.I)
    if not m:
        raise ValueError("サイコロは NdM 形式で指定してください(例: 2d6)。")
    n = int(m.group(1) or 1)
    sides = int(m.group(2))
    if n < 1 or sides < 2:
        raise ValueError("個数は1以上、面数は2以上にしてください。")
    if n > 1000:
        raise ValueError("個数が多すぎます(上限1000)。")
    rolls = [rand_int(1, sides) for _ in range(n)]
    return rolls, sum(rolls)


def main(argv=None):
    p = argparse.ArgumentParser(description="暗号学的乱数で偏りなく選ぶ手足。")
    sub = p.add_subparsers(dest="mode", required=True)

    pi = sub.add_parser("int", help="範囲の整数")
    pi.add_argument("low", type=int)
    pi.add_argument("high", type=int)
    pi.add_argument("--count", type=int, default=1)

    pc = sub.add_parser("choice", help="候補から1つ選ぶ")
    pc.add_argument("items", nargs="+")

    ps = sub.add_parser("shuffle", help="並べ替える")
    ps.add_argument("items", nargs="+")

    pd = sub.add_parser("dice", help="サイコロ(NdM)")
    pd.add_argument("spec")

    for sp in (pi, pc, ps, pd):
        sp.add_argument("--json", action="store_true")

    a = p.parse_args(argv)

    try:
        if a.mode == "int":
            if a.count < 1:
                raise ValueError("--count は1以上です。")
            vals = [rand_int(a.low, a.high) for _ in range(a.count)]
            out = {"mode": "int", "low": a.low, "high": a.high, "values": vals}
            text = "\n".join(str(v) for v in vals)
        elif a.mode == "choice":
            v = choice(a.items)
            out = {"mode": "choice", "items": a.items, "value": v}
            text = v
        elif a.mode == "shuffle":
            v = shuffle(a.items)
            out = {"mode": "shuffle", "items": a.items, "value": v}
            text = " ".join(v)
        else:
            rolls, total = roll(a.spec)
            out = {"mode": "dice", "spec": a.spec, "rolls": rolls, "total": total}
            text = f"{rolls} 合計 {total}"
    except ValueError as e:
        if getattr(a, "json", False):
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
        else:
            print(f"エラー: {e}", file=sys.stderr)
        return 2

    print(json.dumps(out, ensure_ascii=False) if a.json else text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
