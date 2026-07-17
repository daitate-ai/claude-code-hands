#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S6 JSON整形・検証 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM は大きな/崩れた JSON の整形・検証で括弧やカンマを取りこぼす。
このスクリプトは必ず正しく整形し、壊れていれば場所を指して報告する。

使い方:
  python jsonfmt.py '{"b":1,"a":2}'          # 整形(インデント2)
  python jsonfmt.py '{"b":1}' --minify        # 圧縮
  python jsonfmt.py '{"b":1,"a":2}' --sort-keys
  python jsonfmt.py --file data.json
  echo '{"a":1}' | python jsonfmt.py          # 標準入力
  python jsonfmt.py '{"a":1}' --check          # 検証のみ
  python jsonfmt.py '{"a":1}' --json           # 機械可読(結果をラップ)

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import sys


def format_json(text, minify=False, sort_keys=False):
    """text をパースして整形済み文字列を返す。不正なら json.JSONDecodeError。"""
    obj = json.loads(text)
    if minify:
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=sort_keys)
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=sort_keys)


def main(argv=None):
    p = argparse.ArgumentParser(description="JSONを決定論的に整形・検証する手足。")
    p.add_argument("input", nargs="*", help="JSON文字列(省略時は標準入力)")
    p.add_argument("--file", help="このファイルを読む")
    p.add_argument("--minify", action="store_true", help="圧縮(1行)")
    p.add_argument("--sort-keys", action="store_true", help="キーをソート")
    p.add_argument("--check", action="store_true", help="検証のみ(整形しない)")
    p.add_argument("--json", action="store_true", help="機械可読JSONで結果をラップ")
    a = p.parse_args(argv)

    if a.file:
        try:
            with open(a.file, encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            return _fail(f"ファイルを開けません: {e}", a.json)
    elif a.input:
        text = " ".join(a.input)
    else:
        text = sys.stdin.read()

    try:
        formatted = format_json(text, a.minify, a.sort_keys)
    except json.JSONDecodeError as e:
        return _fail(f"不正なJSON: {e.msg} (行{e.lineno} 列{e.colno})", a.json)

    if a.check:
        print(json.dumps({"valid": True}, ensure_ascii=False) if a.json else "valid")
        return 0
    if a.json:
        print(json.dumps({"valid": True, "formatted": formatted}, ensure_ascii=False))
    else:
        print(formatted)
    return 0


def _fail(msg, as_json):
    if as_json:
        print(json.dumps({"valid": False, "error": msg}, ensure_ascii=False))
    else:
        print(f"エラー: {msg}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
