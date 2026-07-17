#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S8 JWTデコード — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM は JWT の base64url 部を誤って読む。このスクリプトは
header / payload を確実に復号し、exp/iat などの時刻も可読化する。

重要: これは【復号のみ】。署名は検証しない（検証には秘密鍵/公開鍵が要る）。
      信頼可否の判断に使わないこと。

使い方:
  python jwtdecode.py <token>
  python jwtdecode.py <token> --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import base64
import datetime
import json
import sys


def _b64url_decode(seg):
    pad = "=" * (-len(seg) % 4)
    return base64.urlsafe_b64decode(seg + pad)


def decode_jwt(token):
    parts = token.strip().split(".")
    if len(parts) < 2:
        raise ValueError("JWTは header.payload.signature 形式です。")
    header = json.loads(_b64url_decode(parts[0]))
    payload = json.loads(_b64url_decode(parts[1]))

    times = {}
    for k in ("iat", "nbf", "exp"):
        v = payload.get(k)
        if isinstance(v, (int, float)):
            times[k] = datetime.datetime.fromtimestamp(
                v, datetime.timezone.utc).isoformat()

    return {
        "header": header,
        "payload": payload,
        "times_utc": times,
        "signature_present": len(parts) >= 3 and parts[2] != "",
        "verified": False,
        "note": "署名は検証していない（復号のみ）。信頼可否の判断には使わない。",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="JWTを復号する手足（署名検証はしない）。")
    p.add_argument("token", help="JWT 文字列")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    try:
        result = decode_jwt(a.token)
    except Exception as e:  # 復号失敗は多様(base64/JSON/UTF-8等)なのでまとめて扱う
        msg = f"JWTを復号できません: {e}"
        if a.json:
            print(json.dumps({"error": msg}, ensure_ascii=False))
        else:
            print(f"エラー: {msg}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print("[header]")
        print(json.dumps(result["header"], ensure_ascii=False, indent=2))
        print("[payload]")
        print(json.dumps(result["payload"], ensure_ascii=False, indent=2))
        if result["times_utc"]:
            print("[times UTC]")
            for k, v in result["times_utc"].items():
                print(f"  {k}: {v}")
        print(f"※ {result['note']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
