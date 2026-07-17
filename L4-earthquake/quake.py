#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L4 地震情報 — Claude Code の「手足」(実データ取得)

なぜ手足か: LLM は最近の地震を知らない。推測すると"それらしい地震"を
作ってしまう。この手足は USGS(米国地質調査所)の公式フィードから実データを取る。

API: USGS Earthquake Hazards Program — APIキー不要・公的機関・出典明記で利用可
注意: 世界の地震(USGS観測)。日本の震度階級は含まない(マグニチュードのみ)。

使い方:
  python quake.py                       # 直近1日・M4.5以上
  python quake.py --feed 2.5_day --limit 5
  python quake.py --min-mag 6 --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import datetime
import json
import sys
import urllib.request

FEEDS = ["significant_day", "4.5_day", "2.5_day", "significant_week", "4.5_week", "all_hour"]
JST = datetime.timezone(datetime.timedelta(hours=9), "JST")


def _get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "claude-code-hands/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as f:
        return json.load(f)


def fetch_quakes(feed="4.5_day"):
    if feed not in FEEDS:
        raise ValueError(f"未知のフィード: {feed}（{', '.join(FEEDS)}）")
    return _get(f"https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{feed}.geojson")


def parse_quakes(raw, min_mag=None, limit=10):
    """GeoJSONを整形する純関数(テスト可能)。新しい順。"""
    feats = raw.get("features")
    if not isinstance(feats, list):
        raise ValueError("地震データの形式が想定と違います(features が無い)。")
    out = []
    for f in feats:
        p = f.get("properties") or {}
        g = (f.get("geometry") or {}).get("coordinates") or [None, None, None]
        mag = p.get("mag")
        if min_mag is not None and (mag is None or mag < min_mag):
            continue
        ms = p.get("time")
        utc = jst = None
        if isinstance(ms, (int, float)):
            dt = datetime.datetime.fromtimestamp(ms / 1000, datetime.timezone.utc)
            utc = dt.replace(microsecond=0).isoformat()
            jst = dt.astimezone(JST).replace(microsecond=0).isoformat()
        out.append({
            "magnitude": mag, "place": p.get("place"),
            "time_utc": utc, "time_jst": jst,
            "longitude": g[0], "latitude": g[1], "depth_km": g[2],
            "url": p.get("url"),
        })
    out.sort(key=lambda x: x["time_utc"] or "", reverse=True)
    return {
        "count": len(out[:limit]),
        "total_matched": len(out),
        "quakes": out[:limit],
        "source": "USGS Earthquake Hazards Program (https://earthquake.usgs.gov)",
        "note": "USGS観測のマグニチュード。日本の震度階級ではない。",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="実際の地震情報を取得する手足(USGS)。")
    p.add_argument("--feed", default="4.5_day", choices=FEEDS)
    p.add_argument("--min-mag", type=float)
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    try:
        r = parse_quakes(fetch_quakes(a.feed), a.min_mag, a.limit)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        msg = f"地震情報を取得できません: {e}"
        if a.json:
            print(json.dumps({"error": msg}, ensure_ascii=False))
        else:
            print(f"エラー: {msg}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        if not r["quakes"]:
            print("該当する地震はありません")
        for q in r["quakes"]:
            print(f"M{q['magnitude']} {q['place']}")
            print(f"  {q['time_jst']} (JST) 深さ{q['depth_km']}km")
        print(f"出典: {r['source']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
