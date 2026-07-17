#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O4 ファイル状態ドリフト防止の回帰テスト。指紋・変更検知・削除検知を担保。"""

import hashlib
import os
import sys
import tempfile
from filestate import snapshot, verify


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "notes.txt")
        with open(path, "wb") as f:
            f.write(b"hello world")

        snap = snapshot(path)
        # 指紋が実際の sha256 と一致
        check("sha256", snap["sha256"] == hashlib.sha256(b"hello world").hexdigest())
        check("size", snap["size"] == 11)

        # 変更なし → 安全に書ける
        v = verify(path, snap["sha256"])
        check("unchanged", v["changed"] is False)

        # 変更あり → 検知して止める
        with open(path, "wb") as f:
            f.write(b"hello world!!")
        v2 = verify(path, snap["sha256"])
        check("changed", v2["changed"] is True)
        check("changed reason", "変更" in v2["reason"])
        check("actual differs", v2["actual_sha256"] != snap["sha256"])

        # 削除 → 検知
        os.remove(path)
        v3 = verify(path, snap["sha256"])
        check("deleted", v3["changed"] is True)
        check("deleted reason", "削除" in v3["reason"])

        # 存在しないファイルの snapshot は例外
        try:
            snapshot(os.path.join(d, "nope.txt"))
            check("missing snapshot", False)
        except OSError:
            pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 指紋/変更なし/変更検知/削除検知/不在 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
