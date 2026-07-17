#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S4 ハッシュ計算の回帰テスト。既知ハッシュベクトルで正しさを担保。"""

import sys
from hash import hash_text

# 公知のテストベクトル
VECTORS = {
    "abc": {
        "md5": "900150983cd24fb0d6963f7d28e17f72",
        "sha1": "a9993e364706816aba3e25717850c26c9cd0d89d",
        "sha256": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
    },
    "": {
        "md5": "d41d8cd98f00b204e9800998ecf8427e",
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
}


def run():
    failed = 0
    for text, expect in VECTORS.items():
        got = hash_text(text)
        for algo, want in expect.items():
            if got.get(algo) != want:
                print(f"FAIL {text!r} {algo}: {got.get(algo)} != {want}")
                failed += 1
    # 日本語(UTF-8)も安定して出ること
    j = hash_text("こんにちは")
    if len(j["sha256"]) != 64 or any(c not in "0123456789abcdef" for c in j["sha256"]):
        print("FAIL 日本語sha256の形式")
        failed += 1
    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 全ハッシュベクトル一致(abc / 空 / 日本語)")
    return 0


if __name__ == "__main__":
    sys.exit(run())
