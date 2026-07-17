#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S5 Base64変換 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM は非自明な文字列（日本語・記号・長い列）の Base64 を
しばしば取り違える。このスクリプトなら必ず正確に相互変換する。

使い方:
  python base64tool.py encode "こんにちは"
  python base64tool.py decode "SGVsbG8="
  python base64tool.py encode "a+b/c" --url    # URLセーフ
  python base64tool.py encode "hi" --json      # 機械可読

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import base64
import binascii
import json
import sys


def encode(text, url=False, encoding="utf-8"):
    raw = text.encode(encoding)
    b = base64.urlsafe_b64encode(raw) if url else base64.b64encode(raw)
    return b.decode("ascii")


def decode(s, url=False, encoding="utf-8"):
    s = s.strip()
    pad = "=" * (-len(s) % 4)  # パディング欠落を許容
    data = (s + pad).encode("ascii")
    raw = base64.urlsafe_b64decode(data) if url else base64.b64decode(data)
    return raw.decode(encoding)


def main(argv=None):
    p = argparse.ArgumentParser(description="Base64を決定論的にエンコード/デコードする手足。")
    p.add_argument("mode", choices=["encode", "decode"], help="encode / decode")
    p.add_argument("input", nargs="+", help="対象の文字列")
    p.add_argument("--url", action="store_true", help="URLセーフ Base64")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    text = " ".join(a.input)
    try:
        result = encode(text, a.url) if a.mode == "encode" else decode(text, a.url)
    except (binascii.Error, ValueError, UnicodeDecodeError) as e:
        msg = f"{a.mode} に失敗しました: {e}"
        if a.json:
            print(json.dumps({"error": msg, "input": text}, ensure_ascii=False))
        else:
            print(f"エラー: {msg}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps({"mode": a.mode, "url_safe": a.url, "input": text, "result": result},
                         ensure_ascii=False))
    else:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
