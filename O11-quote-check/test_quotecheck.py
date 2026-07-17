#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O11 出典接地の回帰テスト。一致/不一致(ねつ造検知)/行番号/空白正規化を担保。"""

import sys
from quotecheck import check_quote

SOURCE = (
    "第一段落です。\n"
    "決定論こそが手足の価値である。\n"
    "最後の行。\n"
)


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # そのまま存在する引用 → 一致・行番号
    r = check_quote("決定論こそが手足の価値である。", SOURCE)
    check("found", r["found"] is True)
    check("similarity", r["similarity"] == 1.0)
    check("line", r["line"] == 2)

    # 言い回しが違う = ねつ造 → 見つからない + 近い箇所を示す
    f = check_quote("決定論こそが手足の本質である。", SOURCE)
    check("not found", f["found"] is False)
    check("closest line", f["closest_line"] == 2)
    check("high similarity", 0.7 < f["similarity"] < 1.0)
    check("reason", "ねつ造" in f["reason"])

    # 全く無い引用 → 見つからない・一致度は低い
    n = check_quote("宇宙人が来た。", SOURCE)
    check("absent", n["found"] is False)
    check("low similarity", n["similarity"] < 0.5)

    # 空白の違いは --normalize-space で吸収できる
    spaced = "Hello    world.\n"
    check("ws strict", check_quote("Hello world.", spaced)["found"] is False)
    check("ws normalized", check_quote("Hello world.", spaced, normalize=True)["found"] is True)

    # 1行目・最終行の行番号
    check("first line", check_quote("第一段落です。", SOURCE)["line"] == 1)
    check("last line", check_quote("最後の行。", SOURCE)["line"] == 3)

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 一致/行番号/ねつ造検知/近似箇所/空白正規化 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
