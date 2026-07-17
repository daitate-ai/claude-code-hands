#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S20 単位変換の回帰テスト。長さ・重さ・温度・異種拒否を担保。"""

import sys
from unitconv import convert


def run():
    failed = 0

    def close(a, b, tol=1e-9):
        return abs(a - b) <= tol

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # 長さ
    check("cm->m", close(convert(100, "cm", "m"), 1.0))
    check("km->m", close(convert(1, "km", "m"), 1000.0))
    check("inch->cm", close(convert(1, "inch", "cm"), 2.54))
    check("mile->km", close(convert(1, "mile", "km"), 1.609344))
    # 重さ
    check("kg->g", close(convert(1, "kg", "g"), 1000.0))
    check("lb->g", close(convert(1, "lb", "g"), 453.59237))
    # 温度
    check("F->C", close(convert(32, "F", "C"), 0.0))
    check("C->F", close(convert(100, "C", "F"), 212.0))
    check("C->K", close(convert(0, "C", "K"), 273.15))
    check("K->C", close(convert(273.15, "K", "C"), 0.0))

    # 異種カテゴリは拒否
    for bad in [("m", "kg"), ("C", "m"), ("g", "F")]:
        try:
            convert(1, *bad)
            check(f"reject {bad}", False)
        except ValueError:
            pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 長さ/重さ/温度/異種拒否 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
