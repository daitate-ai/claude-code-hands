#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S11 文字数カウンタの回帰テスト。文字/単語/行/バイト/出現数を担保。"""

import sys
from countchars import count


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    r = count("hello world")
    check("chars", r["characters"] == 11)
    check("no-space", r["characters_no_spaces"] == 10)
    check("words", r["words"] == 2)
    check("lines", r["lines"] == 1)
    check("bytes", r["bytes_utf8"] == 11)

    # LLMが誤りやすい: strawberry の r
    check("strawberry r", count("strawberry", find="r")["find_count"] == 3)

    # 複数行
    m = count("a\nb\nc")
    check("multiline lines", m["lines"] == 3)

    # 空文字
    e = count("")
    check("empty chars", e["characters"] == 0)
    check("empty lines", e["lines"] == 0)
    check("empty words", e["words"] == 0)

    # 日本語(コードポイント数とUTF-8バイト数)
    j = count("あいう")
    check("ja chars", j["characters"] == 3)
    check("ja bytes", j["bytes_utf8"] == 9)

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 文字/単語/行/バイト/出現数/空/日本語 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
