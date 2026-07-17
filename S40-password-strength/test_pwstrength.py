#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S40 パスワード強度の回帰テスト。プール・エントロピー・判定を担保。"""

import math
import sys
from pwstrength import strength


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # 小文字のみ: プール26・3文字 → 3*log2(26)=14.1 → とても弱い
    a = strength("abc")
    check("pool 26", a["pool_size"] == 26)
    check("entropy abc", a["entropy_bits"] == round(3 * math.log2(26), 1))
    check("rating abc", a["rating"] == "とても弱い")

    # 4種混在: プール94・8文字 → まずまず
    b = strength("Abc123!@")
    check("pool 94", b["pool_size"] == 94)
    check("all classes", b["has_lower"] and b["has_upper"] and b["has_digit"] and b["has_symbol"])
    check("entropy mix", b["entropy_bits"] == round(8 * math.log2(94), 1))
    check("rating mix", b["rating"] == "まずまず")

    # 空文字は 0bit・とても弱い
    e = strength("")
    check("empty entropy", e["entropy_bits"] == 0.0)
    check("empty rating", e["rating"] == "とても弱い")

    # 長い4種混在は強い側
    check("long strong", strength("Abc123!@Xy9$Qw8#Zt7&")["rating"] in ("強い", "とても強い"))

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: プール/エントロピー/判定/空/長文 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
