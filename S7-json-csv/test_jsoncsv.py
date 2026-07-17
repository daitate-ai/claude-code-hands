#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S7 JSON⇔CSV の回帰テスト。列順・引用・欠損・往復を担保。"""

import json
import sys
from jsoncsv import json_to_csv, csv_to_json


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    check("to-csv basic",
          json_to_csv('[{"a":1,"b":2},{"a":3,"b":4}]') == "a,b\n1,2\n3,4\n")
    # カンマ入りセルは引用される(LLMが壊しやすい所)
    check("to-csv quoting", json_to_csv('[{"a":"x,y"}]') == 'a\n"x,y"\n')
    # キーの和集合・欠損は空欄
    check("to-csv union", json_to_csv('[{"a":1},{"b":2}]') == "a,b\n1,\n,2\n")
    # 単一オブジェクトも1行として扱う
    check("to-csv single", json_to_csv('{"a":1}') == "a\n1\n")
    # 空配列
    check("to-csv empty", json_to_csv("[]") == "")

    # CSV → JSON (値は文字列になる)
    check("to-json basic",
          csv_to_json("a,b\n1,2\n", minify=True) == '[{"a":"1","b":"2"}]')
    check("to-json quoted",
          json.loads(csv_to_json('a\n"x,y"\n'))[0]["a"] == "x,y")
    # 日本語
    check("to-json utf8", json.loads(csv_to_json("a\nあ\n"))[0]["a"] == "あ")

    # 往復(文字列化される点を踏まえた比較)
    csv_text = json_to_csv('[{"name":"x,y","n":"5"}]')
    back = json.loads(csv_to_json(csv_text))
    check("roundtrip", back == [{"name": "x,y", "n": "5"}])

    # 不正
    for bad in ['{"a":}', '[1,2,3]', "not json"]:
        try:
            json_to_csv(bad)
            check(f"reject {bad!r}", False)
        except (ValueError, json.JSONDecodeError):
            pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 列順/引用/和集合/単一/空/CSV→JSON/日本語/往復/不正検出 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
