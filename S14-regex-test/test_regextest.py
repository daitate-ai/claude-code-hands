#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S14 正規表現テスターの回帰テスト。マッチ数・位置・グループ・不正検出を担保。"""

import re
import sys
from regextest import find_matches


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    m = find_matches(r"\d+", "a1b22c333")
    check("count", len(m) == 3)
    check("values", [x["match"] for x in m] == ["1", "22", "333"])
    check("first pos", m[0]["start"] == 1 and m[0]["end"] == 2)

    g = find_matches(r"(\w)(\d)", "a1 b2")
    check("group count", len(g) == 2)
    check("groups", g[0]["groups"] == ["a", "1"])

    ci = find_matches("foo", "FOO xfoo", re.IGNORECASE)
    check("ignorecase", len(ci) == 2)

    check("no match", find_matches("zzz", "abc") == [])

    # 不正な正規表現は re.error
    try:
        find_matches("(", "x")
        check("invalid detected", False)
    except re.error:
        pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: マッチ数/位置/グループ/大小無視/不一致/不正検出 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
