#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S3 UUID・ULID の回帰テスト。形式・一意性・ULIDの決定論部分を担保。"""

import re
import sys
from uuidgen import gen_uuid4, gen_ulid, CROCKFORD

UUID4_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # UUID v4 形式
    check("uuid4 format", all(UUID4_RE.match(gen_uuid4()) for _ in range(200)))
    # 一意性(1000個)
    check("uuid4 unique", len({gen_uuid4() for _ in range(1000)}) == 1000)

    # ULID 形式: 26文字・Crockford英字のみ
    u = gen_ulid()
    check("ulid length", len(u) == 26)
    check("ulid alphabet", all(c in CROCKFORD for c in u))
    check("ulid unique", len({gen_ulid() for _ in range(1000)}) == 1000)

    # ULID 決定論: 固定入力なら固定出力
    check("ulid zero", gen_ulid(ts_ms=0, rand=b"\x00" * 10) == "0" * 26)
    check("ulid fixed",
          gen_ulid(ts_ms=1, rand=b"\x00" * 10) == "00000000010000000000000000")

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: UUID形式/一意性 ・ ULID形式/一意性/決定論 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
