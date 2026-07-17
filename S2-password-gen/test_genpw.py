#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S2 パスワード生成の回帰テスト。長さ・文字種保証・除外・一意性を担保。"""

import re
import sys
from genpw import generate, AMBIGUOUS


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # 長さ
    check("length", all(len(generate(16)) == 16 for _ in range(50)))
    check("length 32", len(generate(32)) == 32)

    # 全文字種を必ず含む
    ok = True
    for _ in range(100):
        pw = generate(12)
        if not (re.search(r"[a-z]", pw) and re.search(r"[A-Z]", pw)
                and re.search(r"[0-9]", pw) and re.search(r"[^a-zA-Z0-9]", pw)):
            ok = False
            break
    check("all classes present", ok)

    # 記号を除く
    check("no symbols", all(re.fullmatch(r"[a-zA-Z0-9]+", generate(16, symbols=False))
                            for _ in range(30)))
    # 紛らわしい文字を除く
    check("no ambiguous", all(not any(c in AMBIGUOUS for c in generate(20, no_ambiguous=True))
                              for _ in range(50)))

    # 一意性(乱数が偏っていない最低限の確認)
    check("unique", len({generate(16) for _ in range(500)}) == 500)

    # 長さが文字種数未満はエラー
    try:
        generate(2)  # 4種類必要
        check("reject short", False)
    except ValueError:
        pass
    # 文字種ゼロはエラー
    try:
        generate(10, upper=False, lower=False, digits=False, symbols=False)
        check("reject no pool", False)
    except ValueError:
        pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 長さ/文字種保証/記号除外/紛らわしい文字除外/一意性/不正入力 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
