#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O2 算術手足の回帰テスト。正確さ・多倍長・安全性(コード実行拒否)を担保。"""

import sys
from calc import calc


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # 基本(LLMが誤りやすい桁)
    check("mul", calc("1234*5678") == 7006652)
    check("pow", calc("2**10") == 1024)
    check("truediv", calc("7/2") == 3.5)
    check("floordiv", calc("7//2") == 3)
    check("mod", calc("10%3") == 1)
    check("paren", calc("(1+2)*3") == 9)
    check("unary", calc("-5+3") == -2)
    check("float", calc("0.1+0.2") == 0.1 + 0.2)

    # 整数は多倍長で厳密(LLMには絶対に無理な桁)
    check("bigint", calc("2**100") == 1267650600228229401496703205376)

    # 安全性: コード実行・変数・文字列は全て拒否
    for bad in ["__import__('os')", "open('x')", "a+1", "'a'+'b'", "[1,2][0]",
                "(1).__class__", "lambda: 1"]:
        try:
            calc(bad)
            check(f"reject {bad!r}", False)
        except ValueError:
            pass

    # 巨大累乗は上限で拒否(固まらせない)
    try:
        calc("2**999999")
        check("reject huge pow", False)
    except ValueError:
        pass

    # ゼロ除算
    try:
        calc("1/0")
        check("zero div", False)
    except ZeroDivisionError:
        pass

    # 構文エラー
    try:
        calc("1+")
        check("syntax", False)
    except ValueError:
        pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 算術/多倍長/安全性(コード実行拒否)/上限/例外 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
