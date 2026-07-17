#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S40 パスワード強度 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: パスワードの強さ(エントロピー)を、毎回同じ基準で決定論的に見積もる。
LLM の主観的な「強そう/弱そう」判定を、文字種プールと長さに基づく計算に置き換える。

注意: 文字構成からの推定エントロピー。辞書攻撃・使い回し・パターンは考慮しない。

使い方:
  python pwstrength.py 'Abc123!@'
  python pwstrength.py 'Abc123!@' --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import math
import re
import sys

RATINGS = [(28, "とても弱い"), (36, "弱い"), (60, "まずまず"),
           (128, "強い"), (float("inf"), "とても強い")]


def strength(pw):
    pool = 0
    has_lower = bool(re.search(r"[a-z]", pw))
    has_upper = bool(re.search(r"[A-Z]", pw))
    has_digit = bool(re.search(r"[0-9]", pw))
    has_symbol = bool(re.search(r"[^a-zA-Z0-9]", pw))
    if has_lower:
        pool += 26
    if has_upper:
        pool += 26
    if has_digit:
        pool += 10
    if has_symbol:
        pool += 32
    length = len(pw)
    entropy = length * math.log2(pool) if pool and length else 0.0
    rating = next(name for thr, name in RATINGS if entropy < thr)
    return {
        "length": length,
        "pool_size": pool,
        "entropy_bits": round(entropy, 1),
        "rating": rating,
        "has_lower": has_lower,
        "has_upper": has_upper,
        "has_digit": has_digit,
        "has_symbol": has_symbol,
        "note": "文字構成からの推定エントロピー。辞書攻撃・使い回し・パターンは考慮しない。",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="パスワード強度を決定論的に見積もる手足。")
    p.add_argument("password", help="評価するパスワード")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    r = strength(a.password)
    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        print(f"強度 {r['rating']}（{r['entropy_bits']} bit / {r['length']}文字 / プール{r['pool_size']}）")
        print(f"※ {r['note']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
