#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O9 ロケール正規化の回帰テスト。米国式/欧州式/全角/通貨/曖昧申告を担保。"""

import sys
from localenorm import normalize_number as n


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # 両方の区切りがある → 後ろが小数点(1000倍間違いの元)
    check("us both", n("1,234.56")["value"] == 1234.56)
    check("us style", n("1,234.56")["detected_style"] == "us")
    check("eu both", n("1.234,56")["value"] == 1234.56)
    check("eu style", n("1.234,56")["detected_style"] == "eu")

    # 空白区切り(フランス式)
    check("space thousands", n("1 234,56")["value"] == 1234.56)

    # 複数区切りは桁区切り
    check("us multi", n("1,234,567")["value"] == 1234567)
    check("eu multi", n("1.234.567")["value"] == 1234567)

    # 小数部が3桁でない → 迷いなく小数点
    check("comma decimal", n("1,5")["value"] == 1.5)
    check("comma decimal style", n("1,5")["detected_style"] == "eu")

    # 3桁ちょうどは両義的 → 既定は米国式・ambiguousを申告
    a1 = n("1,234")
    check("ambiguous comma value", a1["value"] == 1234)
    check("ambiguous comma flag", a1["ambiguous"] is True)
    a2 = n("1.234")
    check("ambiguous dot value", a2["value"] == 1.234)
    check("ambiguous dot flag", a2["ambiguous"] is True)
    # 流儀を明示すれば曖昧さは消える
    check("forced eu", n("1.234", style="eu")["value"] == 1234)
    check("forced us", n("1,234", style="us")["value"] == 1234)
    check("forced eu comma", n("1,234", style="eu")["value"] == 1.234)

    # 全角
    check("fullwidth", n("１２３４")["value"] == 1234)
    check("fullwidth mixed", n("１，２３４．５６")["value"] == 1234.56)

    # 通貨・パーセント
    check("yen", n("¥1,234")["value"] == 1234)
    check("yen currency", n("¥1,234")["currency"] == "¥")
    check("kanji yen", n("1234円")["currency"] == "円")
    check("percent", n("12.5%")["value"] == 12.5)
    check("percent flag", n("12.5%")["is_percent"] is True)

    # 符号
    check("negative", n("-1,234.5")["value"] == -1234.5)
    check("accounting negative", n("(1234)")["value"] == -1234)
    check("plus", n("+42")["value"] == 42)

    # 整数はintで返る
    check("int type", isinstance(n("1234")["value"], int))
    check("float type", isinstance(n("12.5")["value"], float))

    # 不正
    for bad in ["abc", "", "1.2.3,4,5", "--1"]:
        try:
            n(bad)
            check(f"reject {bad!r}", False)
        except ValueError:
            pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 米国式/欧州式/空白区切り/全角/通貨/%/符号/曖昧申告/流儀指定/不正 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
