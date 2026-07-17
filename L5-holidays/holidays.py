#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L5 祝日カレンダー — Claude Code の「手足」(実データ取得)

なぜ手足か: LLM は祝日を間違える(移動祝日・法改正・国ごとの違い)。
「来週の月曜は祝日?」を推測させると事故る。この手足は実データを引く。

API: Nager.Date (https://date.nager.at) — APIキー不要・無料
注意: 日本の場合、振替休日・国民の休日も含まれるが、最終確認は
      内閣府の公表(https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html)で。

使い方:
  python holidays.py 2026              # 日本の2026年の祝日
  python holidays.py 2026 --country US
  python holidays.py 2026 --after 2026-07-17 --limit 3
  python holidays.py 2026 --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import sys
import urllib.request


def _get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "claude-code-hands/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as f:
        return json.load(f)


def fetch_holidays(year, country="JP"):
    return _get(f"https://date.nager.at/api/v3/PublicHolidays/{int(year)}/{country.upper()}")


def parse_holidays(raw, after=None, limit=None):
    """APIレスポンスを整形する純関数(テスト可能)。日付順。"""
    if not isinstance(raw, list):
        raise ValueError("祝日データの形式が想定と違います(配列ではない)。")
    items = []
    for h in raw:
        d = h.get("date")
        if after and d and d <= after:
            continue
        items.append({
            "date": d,
            "name_local": h.get("localName"),
            "name_en": h.get("name"),
            "country": h.get("countryCode"),
        })
    items.sort(key=lambda x: x["date"] or "")
    if limit:
        items = items[:limit]
    return {
        "count": len(items),
        "holidays": items,
        "source": "Nager.Date (https://date.nager.at)",
        "note": "日本の祝日は内閣府の公表が最終確認先。",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="祝日を実データで取得する手足(Nager.Date)。")
    p.add_argument("year", type=int)
    p.add_argument("--country", default="JP", help="国コード(既定 JP)")
    p.add_argument("--after", help="この日付より後だけ(YYYY-MM-DD)")
    p.add_argument("--limit", type=int)
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    try:
        r = parse_holidays(fetch_holidays(a.year, a.country), a.after, a.limit)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        msg = f"祝日を取得できません: {e}（国コードや年を確認してください）"
        if a.json:
            print(json.dumps({"error": msg}, ensure_ascii=False))
        else:
            print(f"エラー: {msg}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        for h in r["holidays"]:
            print(f"{h['date']}  {h['name_local']}  ({h['name_en']})")
        print(f"計{r['count']}件  出典: {r['source']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
