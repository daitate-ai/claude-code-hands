#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S5 Base64変換の回帰テスト。既知値・往復・URLセーフを担保。"""

import sys
from base64tool import encode, decode

KNOWN = [
    ("Hello", "SGVsbG8="),
    ("", ""),
    ("f", "Zg=="),
    ("foobar", "Zm9vYmFy"),
]


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    for text, b64 in KNOWN:
        check(f"encode {text!r}", encode(text) == b64)
        check(f"decode {b64!r}", decode(b64) == text)

    # 日本語の往復
    check("日本語 roundtrip", decode(encode("こんにちは")) == "こんにちは")
    # パディング欠落を許容
    check("no-pad decode", decode("SGVsbG8") == "Hello")
    # URLセーフ: 通常だと +/ が出るバイト列
    raw = "\xfb\xff\xbf"
    check("urlsafe no +/", all(c not in "+/" for c in encode(raw, url=True)))
    check("urlsafe roundtrip", decode(encode(raw, url=True), url=True) == raw)

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 既知値 / 往復 / 日本語 / パディング / URLセーフ 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
