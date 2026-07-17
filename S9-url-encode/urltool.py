#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S9 URLエンコード — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM はパーセントエンコード（%20 など）を取りこぼす/取り違える。
このスクリプトは必ず正確にエンコード/デコードする。

使い方:
  python urltool.py encode "a b&c=d"      # a%20b%26c%3Dd
  python urltool.py decode "a%20b"        # a b
  python urltool.py encode "a b" --plus   # a+b (フォーム形式)
  python urltool.py encode "x" --json

依存: なし(Python 3.8+ 標準ライブラリ urllib のみ)
"""

import argparse
import json
import sys
import urllib.parse


def encode(text, plus=False):
    return urllib.parse.quote_plus(text) if plus else urllib.parse.quote(text, safe="")


def decode(text, plus=False):
    return urllib.parse.unquote_plus(text) if plus else urllib.parse.unquote(text)


def main(argv=None):
    p = argparse.ArgumentParser(description="URLパーセントエンコードを決定論的に行う手足。")
    p.add_argument("mode", choices=["encode", "decode"])
    p.add_argument("input", nargs="+", help="対象の文字列")
    p.add_argument("--plus", action="store_true", help="空白を + にする(フォーム形式)")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    text = " ".join(a.input)
    try:
        result = encode(text, a.plus) if a.mode == "encode" else decode(text, a.plus)
    except (ValueError, UnicodeDecodeError) as e:
        msg = f"{a.mode} に失敗しました: {e}"
        if a.json:
            print(json.dumps({"error": msg, "input": text}, ensure_ascii=False))
        else:
            print(f"エラー: {msg}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps({"mode": a.mode, "plus": a.plus, "input": text, "result": result},
                         ensure_ascii=False))
    else:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
