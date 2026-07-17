#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S3 UUID・ULID — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM が"それっぽいID"を書くと、形式が不正だったり乱数が偏ったり
重複したりする。このスクリプトは OS の安全な乱数で正しい形式の ID を発行する。

使い方:
  python uuidgen.py                 # UUID v4 を1つ
  python uuidgen.py --count 5       # 5個
  python uuidgen.py --ulid          # ULID を1つ
  python uuidgen.py --count 3 --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import secrets
import time
import uuid

CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"  # ULID用 base32(I,L,O,U除外)


def gen_uuid4():
    return str(uuid.uuid4())


def gen_ulid(ts_ms=None, rand=None):
    """128bit(48bit時刻 + 80bit乱数)を Crockford Base32 26文字にする。"""
    if ts_ms is None:
        ts_ms = int(time.time() * 1000)
    if rand is None:
        rand = secrets.token_bytes(10)
    num = int.from_bytes(ts_ms.to_bytes(6, "big") + rand, "big")
    chars = []
    for _ in range(26):
        chars.append(CROCKFORD[num & 0x1F])
        num >>= 5
    return "".join(reversed(chars))


def main(argv=None):
    p = argparse.ArgumentParser(description="UUID/ULID を安全な乱数で発行する手足。")
    p.add_argument("--count", type=int, default=1, help="発行個数")
    p.add_argument("--ulid", action="store_true", help="UUIDでなくULIDを発行")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    if a.count < 1:
        print("エラー: --count は1以上です。")
        return 2

    kind = "ulid" if a.ulid else "uuid4"
    gen = gen_ulid if a.ulid else gen_uuid4
    ids = [gen() for _ in range(a.count)]

    if a.json:
        print(json.dumps({"kind": kind, "count": len(ids), "ids": ids}, ensure_ascii=False))
    else:
        for i in ids:
            print(i)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
