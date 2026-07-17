#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S12 ケース変換の回帰テスト。分解と各形式を担保。"""

import sys
from casetool import split_words, cases


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # 分解
    check("camel split", split_words("helloWorldFoo") == ["hello", "world", "foo"])
    check("snake split", split_words("my_var_name") == ["my", "var", "name"])
    check("kebab split", split_words("my-var-name") == ["my", "var", "name"])
    check("acronym split", split_words("HTTPServer") == ["http", "server"])

    c = cases("helloWorldFoo")
    check("snake", c["snake"] == "hello_world_foo")
    check("kebab", c["kebab"] == "hello-world-foo")
    check("constant", c["constant"] == "HELLO_WORLD_FOO")
    check("camel", c["camel"] == "helloWorldFoo")
    check("pascal", c["pascal"] == "HelloWorldFoo")
    check("title", c["title"] == "Hello World Foo")

    # snake → camel
    check("snake->camel", cases("my_var_name")["camel"] == "myVarName")
    # 単一語
    check("single camel", cases("hello")["camel"] == "hello")
    check("single pascal", cases("hello")["pascal"] == "Hello")

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 分解(camel/snake/kebab/頭字語) / 各形式 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
