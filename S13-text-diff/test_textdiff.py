#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S13 テキスト差分の回帰テスト。追加/削除/変更なし/内容を担保。"""

import sys
from textdiff import diff_texts


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    r = diff_texts("a\nb\nc", "a\nB\nc")
    check("added", r["added"] == 1)
    check("removed", r["removed"] == 1)
    check("changed", r["changed"] is True)
    check("diff has -b", "-b" in r["diff"])
    check("diff has +B", "+B" in r["diff"])

    same = diff_texts("hello\nworld", "hello\nworld")
    check("no change added", same["added"] == 0)
    check("no change removed", same["removed"] == 0)
    check("no change flag", same["changed"] is False)
    check("no change diff empty", same["diff"] == "")

    grow = diff_texts("a\nb", "a\nb\nc")
    check("grow added", grow["added"] == 1)
    check("grow removed", grow["removed"] == 0)

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 追加/削除/変更なし/行追加 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
