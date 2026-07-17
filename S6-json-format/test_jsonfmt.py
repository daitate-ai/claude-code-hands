#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S6 JSON整形の回帰テスト。整形/圧縮/ソート/不正検出を担保。"""

import json
import sys
from jsonfmt import format_json


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # 圧縮(順序保持)
    check("minify", format_json('{"b":1, "a":2}', minify=True) == '{"b":1,"a":2}')
    # 圧縮+キーソート
    check("sort", format_json('{"b":1,"a":2}', minify=True, sort_keys=True) == '{"a":2,"b":1}')
    # 整形(インデント2)
    pretty = format_json('{"a":1}')
    check("pretty", pretty == '{\n  "a": 1\n}')
    # 日本語を保持(エスケープしない)
    check("utf8", format_json('{"x":"あ"}', minify=True) == '{"x":"あ"}')
    # 配列
    check("array", format_json("[1,2,3]", minify=True) == "[1,2,3]")
    # 不正JSONは例外
    try:
        format_json('{"a":}')
        check("invalid detected", False)
    except json.JSONDecodeError:
        pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 圧縮/ソート/整形/日本語/不正検出 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
