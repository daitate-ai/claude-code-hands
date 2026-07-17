#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L6 為替換算 — Claude Code の「手足」(実データ取得)

なぜ手足か: LLM は今のレートを知らない。学習時点の古いレートで換算して
しまう(しかも自信満々に)。この手足は ECB(欧州中央銀行)の公式レートを
Frankfurter API 経由で取得して換算する。

API: Frankfurter (https://frankfurter.app) — ECB公表レート・APIキー不要・無料
注意: ECBの参考レートであり、実際の両替レート(手数料込み)とは異なる。

使い方:
  python forex.py 100 USD JPY
  python forex.py 1 EUR USD --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request


def _get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "claude-code-hands/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as f:
        return json.load(f)


def fetch_rate(base, to):
    q = urllib.parse.urlencode({"from": base.upper(), "to": to.upper()})
    return _get(f"https://api.frankfurter.app/latest?{q}")


def convert(raw, amount, to):
    """APIレスポンスと金額から換算する純関数(テスト可能)。"""
    rates = raw.get("rates")
    if not isinstance(rates, dict) or not rates:
        raise ValueError("レートを取得できませんでした(通貨コードを確認してください)。")
    to = to.upper()
    if to not in rates:
        raise ValueError(f"レートに {to} が含まれていません。")
    rate = rates[to]
    return {
        "amount": amount,
        "base": raw.get("base"),
        "to": to,
        "rate": rate,
        "result": round(amount * rate, 4),
        "date": raw.get("date"),
        "source": "European Central Bank via Frankfurter (https://frankfurter.app)",
        "note": "ECBの参考レート。実際の両替レート(手数料込み)とは異なる。",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="実レートで為替換算する手足(ECB/Frankfurter)。")
    p.add_argument("amount", type=float)
    p.add_argument("base", help="元の通貨(例: USD)")
    p.add_argument("to", help="変換先の通貨(例: JPY)")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    try:
        r = convert(fetch_rate(a.base, a.to), a.amount, a.to)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        msg = f"為替レートを取得できません: {e}"
        if a.json:
            print(json.dumps({"error": msg}, ensure_ascii=False))
        else:
            print(f"エラー: {msg}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        print(f"{r['amount']} {r['base']} = {r['result']} {r['to']}")
        print(f"  レート 1 {r['base']} = {r['rate']} {r['to']} ({r['date']} 時点)")
        print(f"  出典: {r['source']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
