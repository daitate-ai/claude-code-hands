#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S8 JWTデコードの回帰テスト。公知のサンプルトークンで復号を担保。"""

import sys
from jwtdecode import decode_jwt

# jwt.io の公知サンプル(HS256)
SAMPLE = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ."
    "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
)


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    r = decode_jwt(SAMPLE)
    check("header alg", r["header"] == {"alg": "HS256", "typ": "JWT"})
    check("payload sub", r["payload"]["sub"] == "1234567890")
    check("payload name", r["payload"]["name"] == "John Doe")
    check("payload iat", r["payload"]["iat"] == 1516239022)
    check("iat readable", r["times_utc"]["iat"].startswith("2018-01-18"))
    check("signature present", r["signature_present"] is True)
    check("not verified", r["verified"] is False)

    # 署名なし(2パート)も復号できる
    two = SAMPLE.rsplit(".", 1)[0]
    r2 = decode_jwt(two)
    check("2-part payload", r2["payload"]["sub"] == "1234567890")
    check("2-part sig absent", r2["signature_present"] is False)

    # 不正入力は例外
    for bad in ["notajwt", "", "onlyonepart"]:
        try:
            decode_jwt(bad)
            check(f"invalid {bad!r}", False)
        except Exception:
            pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: header/payload/時刻/署名有無/2パート/不正検出 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
