#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S22 BMI計算 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: 身長・体重からのBMIと判定を、毎回同じ基準(日本肥満学会)で正確に返す。

使い方:
  python bmi.py 170 65        # 身長cm 体重kg
  python bmi.py 170 65 --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import sys

# 日本肥満学会(JASSO)基準: 閾値未満なら左のラベル
CATS = [(18.5, "低体重"), (25, "普通体重"), (30, "肥満(1度)"),
        (35, "肥満(2度)"), (40, "肥満(3度)"), (float("inf"), "肥満(4度)")]


def bmi(height_cm, weight_kg):
    m = height_cm / 100
    if m <= 0 or weight_kg <= 0:
        raise ValueError("身長・体重は正の値で指定してください。")
    b = weight_kg / (m * m)
    category = next(name for thr, name in CATS if b < thr)
    return {
        "bmi": round(b, 2),
        "category": category,
        "standard_weight_kg": round(22 * m * m, 2),  # BMI22の標準体重
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="BMIと判定を決定論的に返す手足。")
    p.add_argument("height_cm", type=float, help="身長(cm)")
    p.add_argument("weight_kg", type=float, help="体重(kg)")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    try:
        r = bmi(a.height_cm, a.weight_kg)
    except ValueError as e:
        if a.json:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
        else:
            print(f"エラー: {e}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        print(f"BMI {r['bmi']}（{r['category']}）")
        print(f"標準体重 {r['standard_weight_kg']} kg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
