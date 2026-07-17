#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S11 文字数カウンタ — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM は文字を数えるのが苦手（"strawberry の r は何個?"を誤る）。
このスクリプトは文字・単語・行・バイト、特定文字列の出現数を必ず正確に数える。

使い方:
  python countchars.py "hello world"
  python countchars.py "strawberry" --find r      # 出現回数を数える
  python countchars.py --file note.txt
  python countchars.py "こんにちは" --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import re
import sys


def count(text, find=None):
    res = {
        "characters": len(text),
        "characters_no_spaces": len(re.sub(r"\s", "", text)),
        "words": len(text.split()),
        "lines": (text.count("\n") + 1) if text else 0,
        "bytes_utf8": len(text.encode("utf-8")),
    }
    if find:
        res["find"] = find
        res["find_count"] = text.count(find)
    return res


def main(argv=None):
    p = argparse.ArgumentParser(description="文字・単語・行・出現数を決定論的に数える手足。")
    p.add_argument("input", nargs="*", help="対象の文字列(省略時は標準入力)")
    p.add_argument("--file", help="このファイルを数える")
    p.add_argument("--find", help="この文字列の出現回数を数える")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    if a.file:
        try:
            with open(a.file, encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            print(f"エラー: ファイルを開けません: {e}", file=sys.stderr)
            return 2
    elif a.input:
        text = " ".join(a.input)
    else:
        text = sys.stdin.read()

    res = count(text, a.find)
    if a.json:
        print(json.dumps(res, ensure_ascii=False))
    else:
        print(f"文字数        {res['characters']}")
        print(f"文字数(空白除)  {res['characters_no_spaces']}")
        print(f"単語数        {res['words']}")
        print(f"行数          {res['lines']}")
        print(f"バイト(UTF-8) {res['bytes_utf8']}")
        if a.find:
            print(f"「{res['find']}」の出現 {res['find_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
