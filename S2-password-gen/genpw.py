#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2 パスワード生成 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM が"考えて"作るパスワードは乱数が偏り、予測されうる。
このスクリプトは OS の暗号学的乱数(secrets)で、指定した文字種を必ず含む
パスワードを生成する。

使い方:
  python genpw.py                       # 既定16文字
  python genpw.py --length 24 --count 3
  python genpw.py --no-symbols          # 記号を除く
  python genpw.py --no-ambiguous        # 紛らわしい文字(0O1lI)を除く
  python genpw.py --json

依存: なし(Python 3.8+ 標準ライブラリ secrets のみ)
"""

import argparse
import json
import secrets
import string
import sys

AMBIGUOUS = "0O1lI"
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?"


def generate(length=16, upper=True, lower=True, digits=True, symbols=True,
             no_ambiguous=False):
    pools = []
    if lower:
        pools.append(string.ascii_lowercase)
    if upper:
        pools.append(string.ascii_uppercase)
    if digits:
        pools.append(string.digits)
    if symbols:
        pools.append(SYMBOLS)
    if not pools:
        raise ValueError("文字種を最低1つ有効にしてください。")
    if no_ambiguous:
        pools = ["".join(c for c in p if c not in AMBIGUOUS) for p in pools]
        pools = [p for p in pools if p]
    if length < len(pools):
        raise ValueError(f"長さは文字種の数({len(pools)})以上にしてください。")

    # 各文字種から最低1文字を保証し、残りを全体プールから引く
    chars = [secrets.choice(p) for p in pools]
    allc = "".join(pools)
    chars += [secrets.choice(allc) for _ in range(length - len(pools))]
    # 偏りのないシャッフル(Fisher-Yates を secrets で)
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]
    return "".join(chars)


def main(argv=None):
    p = argparse.ArgumentParser(description="暗号学的乱数でパスワードを生成する手足。")
    p.add_argument("--length", type=int, default=16)
    p.add_argument("--count", type=int, default=1)
    p.add_argument("--no-upper", action="store_true")
    p.add_argument("--no-lower", action="store_true")
    p.add_argument("--no-digits", action="store_true")
    p.add_argument("--no-symbols", action="store_true")
    p.add_argument("--no-ambiguous", action="store_true", help="0O1lI を除く")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    try:
        if a.count < 1:
            raise ValueError("--count は1以上です。")
        pws = [generate(a.length, not a.no_upper, not a.no_lower,
                        not a.no_digits, not a.no_symbols, a.no_ambiguous)
               for _ in range(a.count)]
    except ValueError as e:
        if a.json:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
        else:
            print(f"エラー: {e}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps({"length": a.length, "count": len(pws), "passwords": pws},
                         ensure_ascii=False))
    else:
        for pw in pws:
            print(pw)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
