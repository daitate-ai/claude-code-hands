#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O6 文字コード/BOMの回帰テスト。判定(BOM/改行/cp932)と変換を担保。"""

import sys
from encodingfix import detect, convert


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # 素の UTF-8 / LF
    d = detect(b"hello\n")
    check("utf8", d["encoding"] == "utf-8")
    check("no bom", d["has_bom"] is False)
    check("lf", d["newline"] == "LF")

    # BOM付き / CRLF (PowerShell 5.1 が要求する形)
    b = detect(b"\xef\xbb\xbfhello\r\n")
    check("bom detected", b["has_bom"] is True)
    check("bom name", b["bom"] == "utf-8-sig")
    check("crlf", b["newline"] == "CRLF")

    # 混在改行
    check("mixed", detect(b"a\r\nb\n")["newline"] == "mixed")
    # 改行なし
    check("none", detect(b"abc")["newline"] == "none")

    # cp932(UTF-8として不正なバイト列)は cp932 と判定
    check("cp932", detect("あ".encode("cp932"))["encoding"] == "cp932")
    # UTF-8 の日本語は utf-8
    check("utf8 ja", detect("あ".encode("utf-8"))["encoding"] == "utf-8")

    # 変換: LF → BOM付きCRLF
    out = convert(b"a\nb\n", to_encoding="utf-8", bom=True, newline="crlf")
    check("convert bom", out.startswith(b"\xef\xbb\xbf"))
    check("convert crlf", b"a\r\nb\r\n" in out)
    r = detect(out)
    check("convert detect bom", r["has_bom"] is True)
    check("convert detect crlf", r["newline"] == "CRLF")

    # 変換: BOM付きCRLF → BOMなしLF(元に戻る)
    back = convert(out, to_encoding="utf-8", bom=False, newline="lf")
    check("convert back", back == b"a\nb\n")

    # cp932 → utf-8
    check("cp932->utf8", convert("あ".encode("cp932"), to_encoding="utf-8",
                                 newline="lf") == "あ".encode("utf-8"))

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: BOM/改行(LF/CRLF/混在/なし)/cp932判定/変換往復 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
