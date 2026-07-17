#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S25 ローン返済計算 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM は元利均等返済(PMT)の計算をまず正しくできない。
このスクリプトは毎月返済額・総支払・総利息を正確に返す。

使い方:
  python loan.py --principal 3000000 --rate 1.5 --years 10
  python loan.py --principal 1000000 --rate 12 --months 12 --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import sys


def monthly_payment(principal, annual_rate_pct, months):
    """元利均等返済の毎月返済額と総額。"""
    if months <= 0:
        raise ValueError("期間(月数)は1以上で指定してください。")
    r = annual_rate_pct / 100 / 12
    if r == 0:
        pmt = principal / months
    else:
        pmt = principal * r / (1 - (1 + r) ** (-months))
    total = pmt * months
    return {
        "monthly_payment": round(pmt, 2),
        "total_paid": round(total, 2),
        "total_interest": round(total - principal, 2),
        "months": months,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="元利均等ローンの返済額を決定論的に計算する手足。")
    p.add_argument("--principal", type=float, required=True, help="借入元金")
    p.add_argument("--rate", type=float, required=True, help="年利%%")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--years", type=float, help="期間(年)")
    g.add_argument("--months", type=int, help="期間(月)")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    months = a.months if a.months is not None else int(round(a.years * 12))
    try:
        r = monthly_payment(a.principal, a.rate, months)
    except ValueError as e:
        if a.json:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
        else:
            print(f"エラー: {e}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        print(f"毎月返済 {r['monthly_payment']}")
        print(f"総支払   {r['total_paid']}")
        print(f"総利息   {r['total_interest']}（{r['months']}回）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
