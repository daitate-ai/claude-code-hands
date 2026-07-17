#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S9 URLエンコードの回帰テスト。既知値・往復・plus形式を担保。"""

import sys
from urltool import encode, decode


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    check("space", encode("a b") == "a%20b")
    check("reserved", encode("a&b=c") == "a%26b%3Dc")
    check("slash", encode("a/b") == "a%2Fb")
    check("plus form", encode("a b", plus=True) == "a+b")
    check("decode", decode("a%20b") == "a b")
    check("decode plus", decode("a+b", plus=True) == "a b")
    # 日本語の往復
    check("ja roundtrip", decode(encode("あ")) == "あ")
    check("ja encode", encode("あ") == "%E3%81%82")

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 空白/予約文字/スラッシュ/plus/デコード/日本語 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
