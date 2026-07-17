#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S15 カラー変換の回帰テスト。既知色のHSL・往復・不正入力を担保。"""

import sys
from color import describe, parse_color, rgb_to_hsl, hsl_to_rgb


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # 既知色(LLMが誤りやすいHSL)
    r = describe("#FF0000")
    check("red hex", r["hex"] == "#FF0000")
    check("red rgb", r["rgb"] == "rgb(255,0,0)")
    check("red hsl", r["hsl"] == "hsl(0,100%,50%)")
    check("green hsl", describe("#00FF00")["hsl"] == "hsl(120,100%,50%)")
    check("blue hsl", describe("#0000FF")["hsl"] == "hsl(240,100%,50%)")
    check("gray hsl", describe("#808080")["hsl"] == "hsl(0,0%,50%)")
    check("white hsl", describe("#FFFFFF")["hsl"] == "hsl(0,0%,100%)")
    check("black hsl", describe("#000000")["hsl"] == "hsl(0,0%,0%)")

    # 入力形式の自動判定
    check("parse rgb()", parse_color("rgb(255,106,61)") == (255, 106, 61))
    check("parse hsl()", parse_color("hsl(0,100%,50%)") == (255, 0, 0))
    check("parse 3-digit", parse_color("#F00") == (255, 0, 0))
    check("parse no-hash", parse_color("FF0000") == (255, 0, 0))

    # 往復: RGB → HSL → RGB
    for rgb in [(255, 106, 61), (18, 52, 86), (0, 128, 255), (7, 7, 7)]:
        h, s, l = rgb_to_hsl(*rgb)
        check(f"roundtrip {rgb}", hsl_to_rgb(h, s, l) == rgb)

    # 不正入力
    for bad in ["#GGGGGG", "rgb(300,0,0)", "notacolor", ""]:
        try:
            parse_color(bad)
            check(f"reject {bad!r}", False)
        except ValueError:
            pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 既知色HSL/形式判定/往復/不正入力 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
