#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S26 複利積立の回帰テスト。手計算可能な参照値と無利子を担保。"""

import sys
from compound import future_value


def run():
    failed = 0

    def close(a, b, tol=0.01):
        return abs(a - b) <= tol

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # 手計算参照: 元本0・毎月100・年利12%(月1%)・2ヶ月
    #   FV = 100*((1.01^2 - 1)/0.01) = 100*2.01 = 201
    r = future_value(0, 100, 12, 2)
    check("FV ref", close(r["future_value"], 201.0))
    check("contributed", r["total_contributed"] == 200)
    check("interest", close(r["total_interest"], 1.0))

    # 無利子は 元本+積立総額
    z = future_value(1000, 100, 0, 10)
    check("zero-rate FV", z["future_value"] == 2000)
    check("zero-rate interest", z["total_interest"] == 0)

    # 元本のみ(積立なし)複利: 1000*(1.01^2)=1020.1
    p = future_value(1000, 0, 12, 2)
    check("principal only", close(p["future_value"], 1020.1))

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 参照値/無利子/元本のみ複利 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
