#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O7 冪等化の回帰テスト。キーの安定性と「一度きり」を担保。"""

import os
import sys
import tempfile
from idem import payload_key, claim, _load


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # キーは内容が同じなら同じ(JSONのキー順は吸収する)
    k1 = payload_key('{"to":"x","msg":"hi"}')
    k2 = payload_key('{"msg":"hi","to":"x"}')
    check("stable across key order", k1 == k2)
    check("hex length", len(k1) == 64)
    # 内容が違えば違うキー
    check("different payload", payload_key('{"to":"y"}') != k1)
    # JSONでない素のテキストも扱える
    check("plain text", payload_key("hello") == payload_key("hello"))
    check("plain differs", payload_key("hello") != payload_key("hello!"))

    with tempfile.TemporaryDirectory() as d:
        ledger = os.path.join(d, "sent.json")

        # 初回は claim できる
        r1 = claim(ledger, k1, note="test")
        check("first claim", r1["claimed"] is True)
        # 2回目は拒否(二重実行を防ぐ)
        r2 = claim(ledger, k1)
        check("second claim blocked", r2["claimed"] is False)
        check("blocked reason", "既に" in r2["reason"])
        # 別キーは通る
        check("other key ok", claim(ledger, payload_key('{"to":"z"}'))["claimed"] is True)

        # 台帳に永続化されている(別プロセス相当=再読込)
        data = _load(ledger)
        check("persisted", k1 in data)
        check("count", len(data) == 2)

        # 壊れた台帳はエラーにする(黙って通さない)
        with open(ledger, "w", encoding="utf-8") as f:
            f.write("{ broken")
        try:
            claim(ledger, "x")
            check("reject broken ledger", False)
        except ValueError:
            pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: キー安定性/JSON順吸収/初回のみ/永続化/壊れ台帳検知 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
