#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S29 割り勘の回帰テスト。端数配分と合計一致を担保。"""

import sys
from splitbill import split


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    r = split(10000, 3)
    check("base", r["base"] == 3333)
    check("extra_payers", r["extra_payers"] == 1)
    check("extra_amount", r["extra_amount"] == 3334)
    # 合計がちょうど合う
    check("sum", r["extra_payers"] * (r["base"] + 1)
          + (r["people"] - r["extra_payers"]) * r["base"] == 10000)

    e = split(1000, 4)
    check("even base", e["base"] == 250)
    check("even no extra", e["extra_payers"] == 0)

    # いろいろな組合せで合計一致を確認
    for total, people in [(100, 3), (7, 2), (99999, 7), (5, 5)]:
        s = split(total, people)
        got = s["extra_payers"] * (s["base"] + 1) + (people - s["extra_payers"]) * s["base"]
        check(f"sum {total}/{people}", got == total)

    try:
        split(1000, 0)
        check("reject 0 people", False)
    except ValueError:
        pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 端数配分/合計一致/均等/不正人数 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
