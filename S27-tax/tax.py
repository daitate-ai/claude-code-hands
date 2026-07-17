#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S27 消費税計算 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM は税込/税抜の往復や端数処理を誤る。このスクリプトは
指定税率(既定10%、軽減8%)で税抜⇔税込を正確に計算する。

使い方:
  python tax.py 1000               # 税抜1000 → 税込
  python tax.py 1100 --included    # 税込1100 → 税抜
  python tax.py 1000 --rate 8      # 軽減税率
  python tax.py 1000 --round round # 端数: floor(既定)/round/ceil
  python tax.py 1000 --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import math
import sys

ROUNDERS = {
    "floor": math.floor,
    "ceil": math.ceil,
    "round": lambda x: int(x + 0.5),  # 四捨五入(正の金額前提)
}


def from_excluded(amount, rate, rounding="floor"):
    r = ROUNDERS[rounding]
    tax = r(round(amount * rate / 100, 6))  # round(...,6)で浮動小数の誤差を消してから端数処理
    return {"excluded": amount, "tax": tax, "included": amount + tax, "rate": rate}


def from_included(amount, rate, rounding="floor"):
    r = ROUNDERS[rounding]
    excluded = r(round(amount / (1 + rate / 100), 6))
    return {"excluded": excluded, "tax": amount - excluded, "included": amount, "rate": rate}


def main(argv=None):
    p = argparse.ArgumentParser(description="消費税(税込/税抜)を決定論的に計算する手足。")
    p.add_argument("amount", type=float)
    p.add_argument("--included", action="store_true", help="入力を税込として扱う")
    p.add_argument("--rate", type=float, default=10, help="税率%%(既定10、軽減8)")
    p.add_argument("--round", choices=list(ROUNDERS), default="floor", help="端数処理")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    calc = from_included if a.included else from_excluded
    res = calc(a.amount, a.rate, a.round)

    if a.json:
        print(json.dumps(res, ensure_ascii=False))
    else:
        print(f"税抜 {res['excluded']}")
        print(f"税({res['rate']}%) {res['tax']}")
        print(f"税込 {res['included']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
