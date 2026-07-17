#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S21 割合計算の回帰テスト。3類型とゼロ除算を担保。"""

import sys
from percent import pct_of, ratio, change


def run():
    failed = 0

    def close(a, b, tol=1e-9):
        return abs(a - b) <= tol

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    check("of", close(pct_of(25, 200), 50))
    check("of small", close(pct_of(8, 12500), 1000))
    check("ratio", close(ratio(50, 200), 25))
    check("ratio 1/3", close(ratio(1, 3), 33.33333333333333))
    check("change up", close(change(200, 250), 25))
    check("change down", close(change(200, 150), -25))

    for fn, args in [(ratio, (5, 0)), (change, (0, 5))]:
        try:
            fn(*args)
            check(f"zerodiv {fn.__name__}", False)
        except ZeroDivisionError:
            pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: of/ratio/change/ゼロ除算 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
