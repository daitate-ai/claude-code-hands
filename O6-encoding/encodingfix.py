#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
O6 文字コード / BOM固定 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: 文字化け・改行崩れ・BOM有無は目視では分からず、LLM は
"たぶんUTF-8"と推測して壊す。このスクリプトは実際のバイト列を見て
エンコーディング・BOM・改行コードを判定し、指定形式へ変換する。

(当社の実例: PowerShell 5.1 はUTF-8 BOM必須 / Windowsで CRLF 混入)

使い方:
  python encodingfix.py inspect file.txt
  python encodingfix.py convert file.txt --to-encoding utf-8 --bom --newline crlf
  python encodingfix.py inspect file.txt --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import sys

BOMS = [
    ("utf-8-sig", b"\xef\xbb\xbf"),
    ("utf-32-le", b"\xff\xfe\x00\x00"),
    ("utf-32-be", b"\x00\x00\xfe\xff"),
    ("utf-16-le", b"\xff\xfe"),
    ("utf-16-be", b"\xfe\xff"),
]
NEWLINES = {"lf": "\n", "crlf": "\r\n", "cr": "\r"}


def detect(raw):
    """バイト列から BOM・エンコーディング・改行を判定する。"""
    bom = None
    for name, sig in BOMS:
        if raw.startswith(sig):
            bom = name
            break

    if bom:
        encoding = bom
    else:
        encoding = None
        for cand in ("utf-8", "cp932"):  # 日本語環境の現実的な候補順
            try:
                raw.decode(cand)
                encoding = cand
                break
            except UnicodeDecodeError:
                continue
        if encoding is None:
            encoding = "unknown"

    crlf = raw.count(b"\r\n")
    lf = raw.count(b"\n") - crlf
    cr = raw.count(b"\r") - crlf
    kinds = [k for k, v in (("CRLF", crlf), ("LF", lf), ("CR", cr)) if v]
    newline = kinds[0] if len(kinds) == 1 else ("mixed" if kinds else "none")

    return {
        "bom": bom,
        "has_bom": bom is not None,
        "encoding": encoding,
        "newline": newline,
        "counts": {"crlf": crlf, "lf": lf, "cr": cr},
        "bytes": len(raw),
    }


def convert(raw, to_encoding="utf-8", bom=False, newline="lf"):
    """判定した上で、指定のエンコーディング・BOM・改行に変換したバイト列を返す。"""
    info = detect(raw)
    if info["encoding"] == "unknown":
        raise ValueError("エンコーディングを判定できません。")
    text = raw.decode(info["encoding"])
    # 一旦すべて LF に正規化してから目的の改行へ
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if newline not in NEWLINES:
        raise ValueError(f"未知の改行指定: {newline}")
    text = text.replace("\n", NEWLINES[newline])
    enc = "utf-8-sig" if (bom and to_encoding == "utf-8") else to_encoding
    return text.encode(enc)


def main(argv=None):
    p = argparse.ArgumentParser(description="文字コード・BOM・改行を判定/変換する手足。")
    p.add_argument("mode", choices=["inspect", "convert"])
    p.add_argument("path")
    p.add_argument("--to-encoding", default="utf-8")
    p.add_argument("--bom", action="store_true", help="UTF-8にBOMを付ける(PowerShell 5.1向け)")
    p.add_argument("--newline", choices=list(NEWLINES), default="lf")
    p.add_argument("--out", help="変換の出力先(省略時は上書き)")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    try:
        with open(a.path, "rb") as f:
            raw = f.read()
        if a.mode == "inspect":
            r = detect(raw)
            r["path"] = a.path
        else:
            out = convert(raw, a.to_encoding, a.bom, a.newline)
            dest = a.out or a.path
            with open(dest, "wb") as f:
                f.write(out)
            r = {"path": dest, "written_bytes": len(out),
                 "encoding": a.to_encoding, "bom": a.bom, "newline": a.newline}
    except (OSError, ValueError, LookupError) as e:
        if a.json:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
        else:
            print(f"エラー: {e}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    elif a.mode == "inspect":
        print(f"エンコーディング {r['encoding']}  BOM {'あり' if r['has_bom'] else 'なし'}  改行 {r['newline']}")
    else:
        print(f"書き出し {r['path']} ({r['written_bytes']} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
