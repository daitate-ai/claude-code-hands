#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
O7 冪等化 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: 「もう送ったか?」をLLMの記憶に頼ると、二重送信・二重通知・
二重投稿が起きる(セッションが変われば記憶は消える)。このスクリプトは
台帳(JSONファイル)に処理済みキーを残し、機械的に一度きりを保証する。

使い方:
  python idem.py key '{"to":"x","msg":"hi"}'                  # 内容から安定キーを作る
  python idem.py claim --ledger sent.json --key <キー>          # 初回だけ true
  python idem.py claim --ledger sent.json --payload '{"a":1}'  # payloadから自動でキー化
  python idem.py list --ledger sent.json

exit code: claim が既に処理済みなら 1 (=実行を止める合図)、初回なら 0

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import hashlib
import json
import os
import sys


def payload_key(text):
    """内容から安定したキーを作る。JSONならキー順の違いを吸収する。"""
    try:
        obj = json.loads(text)
        canonical = json.dumps(obj, sort_keys=True, separators=(",", ":"),
                               ensure_ascii=False)
    except (json.JSONDecodeError, TypeError):
        canonical = text
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _load(ledger):
    if not os.path.exists(ledger):
        return {}
    try:
        with open(ledger, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        raise ValueError(f"台帳を読めません(壊れている可能性): {ledger}")


def _save(ledger, data):
    tmp = ledger + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, ledger)  # 原子的に置換(書き込み中の破損を防ぐ)


def claim(ledger, key, note=None):
    """初回なら台帳に記録して claimed=True。既にあれば False。"""
    data = _load(ledger)
    if key in data:
        return {"key": key, "claimed": False, "first_seen": data[key].get("at"),
                "reason": "既に処理済みです（二重実行を防ぎました）"}
    data[key] = {"at": None, "note": note}
    _save(ledger, data)
    return {"key": key, "claimed": True, "reason": "初回です（実行してよい）"}


def main(argv=None):
    p = argparse.ArgumentParser(description="二重実行を機械的に防ぐ手足。")
    sub = p.add_subparsers(dest="mode", required=True)

    pk = sub.add_parser("key", help="内容から安定キーを作る")
    pk.add_argument("payload")

    pc = sub.add_parser("claim", help="初回だけ true を返す(台帳に記録)")
    pc.add_argument("--ledger", required=True)
    pc.add_argument("--key")
    pc.add_argument("--payload", help="キーの代わりに内容を渡す(自動でキー化)")
    pc.add_argument("--note")

    pl = sub.add_parser("list", help="台帳の内容")
    pl.add_argument("--ledger", required=True)

    for sp in (pk, pc, pl):
        sp.add_argument("--json", action="store_true")

    a = p.parse_args(argv)

    try:
        if a.mode == "key":
            k = payload_key(a.payload)
            out, text = {"key": k}, k
        elif a.mode == "claim":
            if not a.key and not a.payload:
                raise ValueError("--key か --payload のどちらかが必要です。")
            k = a.key or payload_key(a.payload)
            out = claim(a.ledger, k, a.note)
            text = out["reason"]
        else:
            data = _load(a.ledger)
            out = {"ledger": a.ledger, "count": len(data), "keys": list(data)}
            text = "\n".join(data) or "(空)"
    except ValueError as e:
        if a.json:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
        else:
            print(f"エラー: {e}", file=sys.stderr)
        return 2

    print(json.dumps(out, ensure_ascii=False) if a.json else text)
    return 1 if a.mode == "claim" and not out["claimed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
