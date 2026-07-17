#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S24 日数差分の回帰テスト。既知間隔・うるう年・往復・曜日を担保。"""

import sys
from datediff import parse_date, date_diff, add_days


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    d = lambda s: parse_date(s)

    # 既知間隔
    check("2026通年", date_diff(d("2026-01-01"), d("2026-12-31"))["days"] == 364)
    # うるう年(2024) vs 平年(2026) の2月末→3月
    check("うるう年 Feb", date_diff(d("2024-02-28"), d("2024-03-01"))["days"] == 2)
    check("平年 Feb", date_diff(d("2026-02-28"), d("2026-03-01"))["days"] == 1)
    # 符号(過去向き)
    check("負の差", date_diff(d("2026-12-31"), d("2026-01-01"))["days"] == -364)
    # 週・余り
    w = date_diff(d("2026-07-01"), d("2026-07-16"))
    check("weeks", w["weeks"] == 2 and w["remainder_days"] == 1)

    # 日付加算 + 曜日
    a0 = add_days(d("2026-07-17"), 0)
    check("add0 result", a0["result"] == "2026-07-17")
    check("add0 曜日", a0["weekday"] == "金")
    check("add1 曜日", add_days(d("2026-07-17"), 1)["weekday"] == "土")

    # 往復: N日後にした日付を元と比べると N になる
    for n in (100, -30, 365, 0):
        r = add_days(d("2026-07-17"), n)
        back = date_diff(d("2026-07-17"), d(r["result"]))["days"]
        check(f"roundtrip {n}", back == n)

    # / 区切りも受ける
    check("slash", date_diff(d("2026/07/17"), d("2026/07/18"))["days"] == 1)

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 既知間隔 / うるう年 / 符号 / 週余り / 加算+曜日 / 往復 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
