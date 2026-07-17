#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S39 Cron式の回帰テスト。展開・説明・不正検出を担保。"""

import sys
from cron import describe, parse_field


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # フィールド展開
    check("star", parse_field("*", 0, 59) == set(range(60)))
    check("step", parse_field("*/15", 0, 59) == {0, 15, 30, 45})
    check("range", parse_field("1-5", 0, 7) == {1, 2, 3, 4, 5})
    check("list", parse_field("1,3,5", 0, 59) == {1, 3, 5})

    # 平日9:00
    r = describe("0 9 * * 1-5")
    check("weekday valid", r["valid"] is True)
    check("weekday minute", r["fields"]["minute"] == [0])
    check("weekday hour", r["fields"]["hour"] == [9])
    check("weekday dow", r["fields"]["day_of_week"] == [1, 2, 3, 4, 5])
    check("weekday desc time", "9:00" in r["description"])
    check("weekday desc days", "月" in r["description"] and "金" in r["description"])

    # 15分ごと
    q = describe("*/15 * * * *")
    check("every15 minutes", q["fields"]["minute"] == [0, 15, 30, 45])
    check("every15 desc", "15分ごと" in q["description"])

    # 毎月1日 0:00
    m = describe("0 0 1 * *")
    check("monthly desc", "毎月1日" in m["description"] and "0:00" in m["description"])

    # 毎時0分
    h = describe("0 * * * *")
    check("hourly desc", "毎時0分" in h["description"])

    # 日曜は 0 と 7 の両方で表現できる
    check("sunday 0", describe("0 9 * * 0")["fields"]["day_of_week"] == [0])
    check("sunday 7", describe("0 9 * * 7")["fields"]["day_of_week"] == [0])

    # 不正
    for bad in ["99 * * * *", "* * * *", "0 9 * * 9", "0 25 * * *", "abc * * * *"]:
        try:
            describe(bad)
            check(f"reject {bad!r}", False)
        except ValueError:
            pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 展開/平日/ステップ/毎月/毎時/日曜表現/不正検出 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
