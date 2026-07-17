#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O3 本物の乱数の回帰テスト。乱数値は固定できないので、
   必ず成り立つ性質(範囲・要素保存・全値出現・解析)を担保する。"""

import sys
from collections import Counter
from rand import rand_int, choice, shuffle, roll


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # 範囲(両端含む)を必ず守る
    vals = [rand_int(1, 6) for _ in range(3000)]
    check("range", all(1 <= v <= 6 for v in vals))
    # 両端を含めて全ての値が出る(偏りがない最低限の確認)
    check("all values appear", set(vals) == {1, 2, 3, 4, 5, 6})
    # 極端な偏りがない(一様なら各約500回。200〜900に収まるはず)
    c = Counter(vals)
    check("roughly uniform", all(200 < c[v] < 900 for v in c))
    # 単一値の範囲
    check("single", rand_int(5, 5) == 5)
    # 逆転はエラー
    try:
        rand_int(10, 1)
        check("reject reversed", False)
    except ValueError:
        pass

    # choice は必ず候補の中から返る
    items = ["a", "b", "c"]
    check("choice member", all(choice(items) in items for _ in range(200)))
    check("choice covers", {choice(items) for _ in range(200)} == set(items))
    try:
        choice([])
        check("reject empty", False)
    except ValueError:
        pass

    # shuffle は要素を保存し、元を壊さない
    src = ["a", "b", "c", "d"]
    sh = shuffle(src)
    check("shuffle multiset", sorted(sh) == sorted(src))
    check("shuffle not in place", src == ["a", "b", "c", "d"])
    # 何度か回せば少なくとも一度は並びが変わる
    check("shuffle varies", any(shuffle(src) != src for _ in range(50)))

    # サイコロ
    rolls, total = roll("2d6")
    check("dice count", len(rolls) == 2)
    check("dice range", all(1 <= r <= 6 for r in rolls))
    check("dice total", total == sum(rolls))
    check("dice default n", len(roll("d20")[0]) == 1)
    for bad in ["abc", "2d1", "0d6", "2000d6"]:
        try:
            roll(bad)
            check(f"reject {bad!r}", False)
        except ValueError:
            pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 範囲/全値出現/一様性/choice/shuffle保存/サイコロ/不正入力 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
