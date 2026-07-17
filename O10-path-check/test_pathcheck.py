#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O10 パス/cwdドリフト防止の回帰テスト。正規化・実在・基準脱出検知を担保。"""

import os
import sys
import tempfile
from pathcheck import inspect


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    with tempfile.TemporaryDirectory() as d:
        base = os.path.realpath(d)
        inside = os.path.join(base, "a.txt")
        with open(inside, "w", encoding="utf-8") as f:
            f.write("x")
        subdir = os.path.join(base, "sub")
        os.mkdir(subdir)

        # 実在・種別
        r = inspect(inside)
        check("exists", r["exists"] is True)
        check("is_file", r["is_file"] is True)
        check("is_dir false", r["is_dir"] is False)
        check("absolute", os.path.isabs(r["absolute"]))
        check("posix has no backslash", "\\" not in r["posix"])

        # ディレクトリ
        check("dir", inspect(subdir)["is_dir"] is True)

        # 不在
        check("missing", inspect(os.path.join(base, "nope.txt"))["exists"] is False)

        # 基準内
        i = inspect(inside, base=base)
        check("inside_base", i["inside_base"] is True)
        check("no warning", "warning" not in i)

        # 基準の外へ脱出(../ )は検知する
        escape = os.path.join(base, "..", "escaped.txt")
        o = inspect(escape, base=base)
        check("outside_base", o["inside_base"] is False)
        check("warning", "warning" in o)

        # サブディレクトリは基準内
        check("subdir inside", inspect(subdir, base=base)["inside_base"] is True)

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 実在/種別/正規化/基準内/脱出検知 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
