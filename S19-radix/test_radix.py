#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S19 進数変換の回帰テスト。既知値・負数・往復を担保。"""

import sys
from radix import parse_int, convert

PARSE = [
    ("255", 255), ("0xFF", 255), ("0xff", 255), ("0b1010", 10),
    ("0o377", 255), ("-16", -16), ("+8", 8), ("1_000", 1000),
]


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    for s, v in PARSE:
        check(f"parse {s!r}", parse_int(s) == v)

    c = convert(255)
    check("255 hex", c["hex"] == "0xff")
    check("255 oct", c["oct"] == "0o377")
    check("255 bin", c["bin"] == "0b11111111")
    check("255 dec", c["dec"] == "255")

    n = convert(-16)
    check("-16 hex", n["hex"] == "-0x10")
    check("-16 bin", n["bin"] == "-0b10000")
    check("-16 oct", n["oct"] == "-0o20")

    # 往復: どの基数表現も parse で元に戻る
    for v in (0, 1, 255, 4096, -255, 123456789):
        c = convert(v)
        for key in ("hex", "oct", "bin", "dec"):
            check(f"roundtrip {v} {key}", parse_int(c[key]) == v)

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 解釈 / 既知値 / 負数 / 往復 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
