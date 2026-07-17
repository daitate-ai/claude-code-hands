#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
O10 パス / cwd ドリフト防止 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: Windowsの円記号パス・空白入りパス・相対パスと cwd のズレで
「あるはずのファイルが無い」「意図しない場所に書く」事故が起きる。
このスクリプトはパスを正規化し、実在性と「基準ディレクトリの外に出ていないか」
(../ による脱出)を機械的に確認する。

使い方:
  python pathcheck.py "..\\data\\a.txt"
  python pathcheck.py "../x" --base /home/me/proj    # 基準の外に出ていないか
  python pathcheck.py "notes.md" --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import os
import sys


def inspect(path, base=None):
    absolute = os.path.abspath(path)
    r = {
        "input": path,
        "absolute": absolute,
        "posix": absolute.replace("\\", "/"),
        "exists": os.path.exists(absolute),
        "is_dir": os.path.isdir(absolute),
        "is_file": os.path.isfile(absolute),
        "cwd": os.getcwd(),
        "has_space": " " in absolute,
    }
    if base is not None:
        base_abs = os.path.abspath(base)
        try:
            common = os.path.commonpath([base_abs, absolute])
            inside = common == base_abs
        except ValueError:  # 別ドライブ等で比較不能
            inside = False
        r["base"] = base_abs
        r["inside_base"] = inside
        if not inside:
            r["warning"] = "基準ディレクトリの外を指しています（../ による脱出の可能性）"
    return r


def main(argv=None):
    p = argparse.ArgumentParser(description="パスを正規化し実在性と基準内包含を確認する手足。")
    p.add_argument("path")
    p.add_argument("--base", help="この基準ディレクトリの外に出ていないか確認")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    r = inspect(a.path, a.base)
    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        print(f"絶対パス {r['absolute']}")
        print(f"実在     {'あり' if r['exists'] else 'なし'}")
        if "inside_base" in r:
            print(f"基準内   {'はい' if r['inside_base'] else 'いいえ ← 危険'}")
    # 基準の外を指していたら異常終了(=止める合図)
    return 1 if r.get("inside_base") is False else 0


if __name__ == "__main__":
    raise SystemExit(main())
