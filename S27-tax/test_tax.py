#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S27 消費税計算の回帰テスト。税抜⇔税込・軽減税率・端数処理を担保。"""

import sys
from tax import from_excluded, from_included


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # 税抜 → 税込(既定10%)
    r = from_excluded(1000, 10)
    check("excl tax", r["tax"] == 100)
    check("excl incl", r["included"] == 1100)
    # 軽減8%
    check("excl 8%", from_excluded(150, 8)["tax"] == 12)
    # 端数: 105*10%=10.5 → floor 10 / round 11 / ceil 11
    check("floor", from_excluded(105, 10, "floor")["tax"] == 10)
    check("round", from_excluded(105, 10, "round")["tax"] == 11)
    check("ceil", from_excluded(105, 10, "ceil")["tax"] == 11)

    # 税込 → 税抜(浮動小数の誤差に強いこと)
    i = from_included(1100, 10)
    check("incl excl", i["excluded"] == 1000)
    check("incl tax", i["tax"] == 100)
    check("incl 8%", from_included(162, 8)["excluded"] == 150)

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 税抜⇔税込 / 軽減税率 / 端数(floor/round/ceil) 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
