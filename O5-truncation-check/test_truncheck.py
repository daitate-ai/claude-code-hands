#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O5 truncation検知の回帰テスト。完結/切れの判定を担保。"""

import sys
from truncheck import check as tcheck


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # 完結しているもの
    check("complete json", tcheck('{"a":1}')["likely_truncated"] is False)
    check("complete ja", tcheck("これは完結した文です。")["likely_truncated"] is False)
    check("complete en", tcheck("This is complete.")["likely_truncated"] is False)
    check("complete fence", tcheck("```py\nx=1\n```")["likely_truncated"] is False)

    # 切れているもの
    t = tcheck('{"a":1')
    check("truncated json", t["likely_truncated"] is True)
    check("truncated reason", any("括弧" in r for r in t["reasons"]))

    f = tcheck("```py\nx=1")
    check("unclosed fence", f["likely_truncated"] is True)
    check("fence reason", any("コードフェンス" in r for r in f["reasons"]))

    check("no terminal", tcheck("途中で切れた文")["likely_truncated"] is True)
    check("odd quote", tcheck('say "hello')["likely_truncated"] is True)
    check("stray closer", tcheck("a)")["likely_truncated"] is True)

    # 空文字は"切れ"扱いしない
    check("empty", tcheck("")["likely_truncated"] is False)

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 完結(JSON/日本語/英語/フェンス) / 切れ(括弧/フェンス/終端/引用符) / 空 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
