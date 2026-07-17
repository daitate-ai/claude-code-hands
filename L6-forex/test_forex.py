#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L6 為替換算の回帰テスト。固定データで換算ロジックを検証(ネットワーク非依存)。"""

import sys
from forex import convert

# 実際の Frankfurter レスポンスと同じ形
FIXTURE = {"amount": 1.0, "base": "USD", "date": "2026-07-16", "rates": {"JPY": 162.2}}


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    r = convert(FIXTURE, 100, "JPY")
    check("result", r["result"] == 16220.0)
    check("rate", r["rate"] == 162.2)
    check("base", r["base"] == "USD")
    check("to", r["to"] == "JPY")
    check("date", r["date"] == "2026-07-16")
    check("source", "Frankfurter" in r["source"])
    check("note", "手数料" in r["note"])

    # 小数・ゼロ・小額
    check("fraction", convert(FIXTURE, 1.5, "JPY")["result"] == 243.3)
    check("zero", convert(FIXTURE, 0, "JPY")["result"] == 0)
    # 通貨コードは小文字でも通る
    check("lowercase", convert(FIXTURE, 1, "jpy")["result"] == 162.2)

    # 含まれない通貨・空レートは明示エラー
    for bad_args, bad_raw in [(("EUR",), FIXTURE), (("JPY",), {"rates": {}}),
                              (("JPY",), {}), (("JPY",), {"rates": "x"})]:
        try:
            convert(bad_raw, 1, *bad_args)
            check(f"reject {bad_args} {bad_raw}", False)
        except ValueError:
            pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 換算/小数/大小文字/未収録通貨/不正形式 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
