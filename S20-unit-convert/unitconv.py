#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S20 単位変換 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM は単位換算(特に温度・ヤードポンド)で係数を誤る。
このスクリプトは長さ・重さ・温度を必ず正確に換算する。

使い方:
  python unitconv.py 100 cm m       # 1.0
  python unitconv.py 32 F C         # 0.0
  python unitconv.py 1 mile km      # 1.609344
  python unitconv.py 100 cm m --json

対応: 長さ(mm/cm/m/km/inch/ft/yard/mile) 重さ(mg/g/kg/t/oz/lb) 温度(C/F/K)

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import sys

LENGTH = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0,
          "inch": 0.0254, "in": 0.0254, "ft": 0.3048, "yard": 0.9144,
          "yd": 0.9144, "mile": 1609.344, "mi": 1609.344}
WEIGHT = {"mg": 0.001, "g": 1.0, "kg": 1000.0, "t": 1_000_000.0,
          "oz": 28.349523125, "lb": 453.59237}
TEMP = {"c", "f", "k"}


def _to_celsius(v, u):
    return {"c": v, "f": (v - 32) * 5 / 9, "k": v - 273.15}[u]


def _from_celsius(c, u):
    return {"c": c, "f": c * 9 / 5 + 32, "k": c + 273.15}[u]


def convert(value, from_unit, to_unit):
    f, t = from_unit.lower(), to_unit.lower()
    if f in TEMP and t in TEMP:
        return _from_celsius(_to_celsius(value, f), t)
    if f in LENGTH and t in LENGTH:
        return value * LENGTH[f] / LENGTH[t]
    if f in WEIGHT and t in WEIGHT:
        return value * WEIGHT[f] / WEIGHT[t]
    raise ValueError(f"変換できない単位の組み合わせ: {from_unit} → {to_unit}")


def main(argv=None):
    p = argparse.ArgumentParser(description="長さ・重さ・温度を決定論的に換算する手足。")
    p.add_argument("value", type=float)
    p.add_argument("from_unit")
    p.add_argument("to_unit")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    try:
        result = convert(a.value, a.from_unit, a.to_unit)
    except ValueError as e:
        if a.json:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
        else:
            print(f"エラー: {e}", file=sys.stderr)
        return 2

    # 表示は不要な小数を落とす
    shown = round(result, 10)
    if a.json:
        print(json.dumps({"value": a.value, "from": a.from_unit, "to": a.to_unit,
                          "result": shown}, ensure_ascii=False))
    else:
        print(f"{a.value} {a.from_unit} = {shown} {a.to_unit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
