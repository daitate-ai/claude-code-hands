#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S12 ケース変換 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: 識別子の命名規則変換（camelCase ⇔ snake_case ⇔ kebab-case…）を
一貫したルールで確実に行う。境界（頭字語・数字）でブレない。

使い方:
  python casetool.py "helloWorldFoo"       # 全ケース表示
  python casetool.py "my_var_name" --to camel
  python casetool.py "HTTPServer" --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import re
import sys


def split_words(s):
    """任意の識別子を単語リスト(小文字)に分解する。"""
    s = re.sub(r"[_\-\s]+", " ", s.strip())
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", s)      # camel境界
    s = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", s)    # 頭字語→語 の境界
    return [w.lower() for w in s.split() if w]


def cases(s):
    w = split_words(s)
    return {
        "words": w,
        "snake": "_".join(w),
        "kebab": "-".join(w),
        "constant": "_".join(x.upper() for x in w),
        "camel": (w[0] + "".join(x.capitalize() for x in w[1:])) if w else "",
        "pascal": "".join(x.capitalize() for x in w),
        "title": " ".join(x.capitalize() for x in w),
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="命名規則(ケース)を決定論的に変換する手足。")
    p.add_argument("input", nargs="+", help="変換する識別子")
    p.add_argument("--to", choices=["snake", "kebab", "constant", "camel", "pascal", "title"],
                   help="1つの形式だけ出力")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    c = cases(" ".join(a.input))
    if a.to:
        print(c[a.to])
        return 0
    if a.json:
        print(json.dumps(c, ensure_ascii=False))
    else:
        for k in ("camel", "pascal", "snake", "kebab", "constant", "title"):
            print(f"{k:9} {c[k]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
