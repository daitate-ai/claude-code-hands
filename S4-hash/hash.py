#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S4 ハッシュ計算 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM はハッシュを"計算"できない（それらしい16進を捏造してしまう）。
このスクリプトなら文字列・ファイルの MD5/SHA を必ず正確に返す。

使い方:
  python hash.py "hello"            # 文字列のハッシュ一式
  python hash.py "hello" --algo sha256
  python hash.py --file path.pdf    # ファイルのハッシュ
  python hash.py "hello" --json     # 機械可読(Claude Codeはこれを使う)

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import hashlib
import json
import sys

ALGOS = ["md5", "sha1", "sha256", "sha512"]


def hash_text(text, encoding="utf-8"):
    data = text.encode(encoding)
    return {a: hashlib.new(a, data).hexdigest() for a in ALGOS}


def hash_file(path):
    hs = {a: hashlib.new(a) for a in ALGOS}
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            for h in hs.values():
                h.update(chunk)
    return {a: hs[a].hexdigest() for a in ALGOS}


def main(argv=None):
    p = argparse.ArgumentParser(description="文字列/ファイルのハッシュを決定論的に算出する手足。")
    p.add_argument("input", nargs="*", help="ハッシュ対象の文字列")
    p.add_argument("--file", help="このファイルをハッシュする")
    p.add_argument("--algo", choices=ALGOS, help="1つのアルゴリズムだけ出力")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    if a.file:
        try:
            res = hash_file(a.file)
        except OSError as e:
            _err(f"ファイルを開けません: {e}", a.json)
            return 2
        src = {"file": a.file}
    else:
        text = " ".join(a.input)
        if not text:
            _err("文字列か --file を指定してください。", a.json)
            return 2
        res = hash_text(text)
        src = {"text": text}

    if a.algo:
        res = {a.algo: res[a.algo]}

    if a.json:
        print(json.dumps({**src, "hashes": res}, ensure_ascii=False))
    else:
        for k, v in res.items():
            print(f"{k:7} {v}")
    return 0


def _err(msg, as_json):
    if as_json:
        print(json.dumps({"error": msg}, ensure_ascii=False))
    else:
        print(f"エラー: {msg}", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
