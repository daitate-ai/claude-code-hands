#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S22 BMIの回帰テスト。値・判定・標準体重・不正入力を担保。"""

import sys
from bmi import bmi


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    r = bmi(170, 65)
    check("bmi value", r["bmi"] == 22.49)
    check("category", r["category"] == "普通体重")
    check("standard", r["standard_weight_kg"] == 63.58)

    check("low", bmi(160, 45)["category"] == "低体重")
    check("obese1", bmi(170, 80)["category"] == "肥満(1度)")
    check("boundary 25", bmi(200, 100)["category"] == "肥満(1度)")  # 25.0 は肥満側

    for bad in [(0, 60), (170, 0)]:
        try:
            bmi(*bad)
            check(f"reject {bad}", False)
        except ValueError:
            pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 値/判定/標準体重/境界/不正入力 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
