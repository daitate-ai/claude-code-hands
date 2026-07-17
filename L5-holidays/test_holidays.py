#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L5 祝日カレンダーの回帰テスト。固定データで解析・絞り込み・並びを検証。"""

import sys
from holidays import parse_holidays

# 実際の Nager.Date レスポンスと同じ形
FIXTURE = [
    {"date": "2026-01-01", "localName": "元日", "name": "New Year's Day",
     "countryCode": "JP", "types": ["Public"]},
    {"date": "2026-07-20", "localName": "海の日", "name": "Marine Day",
     "countryCode": "JP", "types": ["Public"]},
    {"date": "2026-05-05", "localName": "こどもの日", "name": "Children's Day",
     "countryCode": "JP", "types": ["Public"]},
]


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    r = parse_holidays(FIXTURE)
    check("count", r["count"] == 3)
    # 日付順に並ぶ(入力順は バラバラ)
    check("sorted", [h["date"] for h in r["holidays"]]
          == ["2026-01-01", "2026-05-05", "2026-07-20"])
    h = r["holidays"][0]
    check("local name", h["name_local"] == "元日")
    check("en name", h["name_en"] == "New Year's Day")
    check("country", h["country"] == "JP")

    # 指定日より後だけ
    after = parse_holidays(FIXTURE, after="2026-07-17")
    check("after count", after["count"] == 1)
    check("after date", after["holidays"][0]["date"] == "2026-07-20")
    check("after name", after["holidays"][0]["name_local"] == "海の日")
    # 境界: 同日は含まない(「より後」)
    check("after exclusive", parse_holidays(FIXTURE, after="2026-07-20")["count"] == 0)

    # 件数制限
    check("limit", parse_holidays(FIXTURE, limit=2)["count"] == 2)
    check("after+limit", parse_holidays(FIXTURE, after="2026-01-01", limit=1)
          ["holidays"][0]["date"] == "2026-05-05")

    # 出典と注意書き
    check("source", "Nager.Date" in r["source"])
    check("note", "内閣府" in r["note"])

    # 不正形式は明示エラー
    for bad in [{}, "x", None]:
        try:
            parse_holidays(bad)
            check(f"reject {bad}", False)
        except ValueError:
            pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 解析/日付順/日付絞り込み/境界/件数制限/不正形式 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
