#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S26 複利積立計算 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM は複利＋毎月積立の将来価値を正しく計算できない。
このスクリプトは元本・毎月積立・年利・期間から将来価値を正確に返す(月複利)。

使い方:
  python compound.py --principal 1000000 --monthly 30000 --rate 5 --years 20
  python compound.py --principal 0 --monthly 100 --rate 12 --months 2 --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import sys


def future_value(principal, monthly, annual_rate_pct, months):
    """月複利で 元本＋毎月積立 の将来価値を返す。"""
    if months < 0:
        raise ValueError("期間(月数)は0以上で指定してください。")
    r = annual_rate_pct / 100 / 12
    if r == 0:
        fv = principal + monthly * months
    else:
        fv = principal * (1 + r) ** months + monthly * (((1 + r) ** months - 1) / r)
    contributed = principal + monthly * months
    return {
        "future_value": round(fv, 2),
        "total_contributed": round(contributed, 2),
        "total_interest": round(fv - contributed, 2),
        "months": months,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="複利積立の将来価値を決定論的に計算する手足。")
    p.add_argument("--principal", type=float, default=0, help="初期元本")
    p.add_argument("--monthly", type=float, default=0, help="毎月の積立額")
    p.add_argument("--rate", type=float, required=True, help="年利%%")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--years", type=float, help="期間(年)")
    g.add_argument("--months", type=int, help="期間(月)")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    months = a.months if a.months is not None else int(round(a.years * 12))
    try:
        r = future_value(a.principal, a.monthly, a.rate, months)
    except ValueError as e:
        if a.json:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
        else:
            print(f"エラー: {e}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        print(f"将来価値 {r['future_value']}")
        print(f"積立総額 {r['total_contributed']}")
        print(f"運用益   {r['total_interest']}（{r['months']}ヶ月）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
