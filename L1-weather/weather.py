#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L1 天気 — Claude Code の「手足」(実データ取得)

なぜ手足か: LLM は天気を知らない(学習時点で止まっている)。推測すると
"それらしい天気"を作ってしまう。この手足は Open-Meteo から実データを取る。

API: Open-Meteo (https://open-meteo.com) — APIキー不要・無料・出典明記で利用可

使い方:
  python weather.py --city 東京
  python weather.py --lat 35.68 --lon 139.76
  python weather.py --city Osaka --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request

# WMO天気コード → 日本語
WMO = {
    0: "快晴", 1: "晴れ", 2: "一部曇り", 3: "曇り",
    45: "霧", 48: "霧氷",
    51: "弱い霧雨", 53: "霧雨", 55: "強い霧雨",
    56: "弱い着氷性霧雨", 57: "着氷性霧雨",
    61: "弱い雨", 63: "雨", 65: "強い雨",
    66: "弱い着氷性の雨", 67: "着氷性の雨",
    71: "弱い雪", 73: "雪", 75: "強い雪", 77: "霧雪",
    80: "弱いにわか雨", 81: "にわか雨", 82: "激しいにわか雨",
    85: "弱いにわか雪", 86: "にわか雪",
    95: "雷雨", 96: "雹を伴う雷雨", 99: "激しい雹を伴う雷雨",
}


def _get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "claude-code-hands/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as f:
        return json.load(f)


# Open-Meteoの地名検索は日本語表記を引けない(実測: "東京"→該当なし / "Tokyo"→東京都)。
# 主要都市はローマ字へ読み替える。表示名はAPIが日本語で返す。
JP_ALIASES = {
    "東京": "Tokyo", "大阪": "Osaka", "名古屋": "Nagoya", "横浜": "Yokohama",
    "札幌": "Sapporo", "福岡": "Fukuoka", "京都": "Kyoto", "神戸": "Kobe",
    "仙台": "Sendai", "広島": "Hiroshima", "那覇": "Naha", "新潟": "Niigata",
    "金沢": "Kanazawa", "静岡": "Shizuoka", "岡山": "Okayama", "熊本": "Kumamoto",
    "鹿児島": "Kagoshima", "松山": "Matsuyama", "高松": "Takamatsu", "長崎": "Nagasaki",
    "宇都宮": "Utsunomiya", "千葉": "Chiba", "さいたま": "Saitama", "川崎": "Kawasaki",
    "北九州": "Kitakyushu", "堺": "Sakai", "浜松": "Hamamatsu", "青森": "Aomori",
    "秋田": "Akita", "盛岡": "Morioka", "山形": "Yamagata", "福島": "Fukushima",
    "水戸": "Mito", "前橋": "Maebashi", "長野": "Nagano", "岐阜": "Gifu",
    "津": "Tsu", "大津": "Otsu", "奈良": "Nara", "和歌山": "Wakayama",
    "鳥取": "Tottori", "松江": "Matsue", "山口": "Yamaguchi", "徳島": "Tokushima",
    "高知": "Kochi", "佐賀": "Saga", "大分": "Oita", "宮崎": "Miyazaki",
}


def geocode(city):
    """都市名から緯度経度を引く(Open-Meteo Geocoding)。日本語の主要都市は読み替える。"""
    query = JP_ALIASES.get(city.strip(), city)
    q = urllib.parse.urlencode({"name": query, "count": 1, "language": "ja"})
    data = _get(f"https://geocoding-api.open-meteo.com/v1/search?{q}")
    results = data.get("results") or []
    if not results:
        raise ValueError(
            f"地名が見つかりません: {city!r}"
            "（Open-Meteoの地名検索はローマ字/英語表記が必要です。例: Tokyo, Osaka。"
            "または --lat/--lon で座標を直接指定してください）"
        )
    r = results[0]
    return r["latitude"], r["longitude"], r.get("name", city)


def fetch_weather(lat, lon, timezone="Asia/Tokyo"):
    q = urllib.parse.urlencode({
        "latitude": lat, "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "timezone": timezone, "forecast_days": 1,
    })
    return _get(f"https://api.open-meteo.com/v1/forecast?{q}")


def parse_weather(raw, place=None):
    """APIレスポンスを整形する純関数(テスト可能)。"""
    cur = raw.get("current")
    if not isinstance(cur, dict):
        raise ValueError("天気データの形式が想定と違います(current が無い)。")
    code = cur.get("weather_code")
    return {
        "place": place,
        "latitude": raw.get("latitude"),
        "longitude": raw.get("longitude"),
        "time": cur.get("time"),
        "timezone": raw.get("timezone"),
        "temperature_c": cur.get("temperature_2m"),
        "humidity_pct": cur.get("relative_humidity_2m"),
        "wind_speed_kmh": cur.get("wind_speed_10m"),
        "weather_code": code,
        "weather": WMO.get(code, f"不明(code {code})"),
        "source": "Open-Meteo (https://open-meteo.com)",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="実際の天気を取得する手足(Open-Meteo)。")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--city", help="地名(例: 東京)")
    g.add_argument("--lat", type=float, help="緯度(--lon と併用)")
    p.add_argument("--lon", type=float)
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    try:
        if a.city:
            lat, lon, place = geocode(a.city)
        else:
            if a.lon is None:
                raise ValueError("--lat と --lon は両方指定してください。")
            lat, lon, place = a.lat, a.lon, None
        r = parse_weather(fetch_weather(lat, lon), place)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        msg = f"天気を取得できません: {e}"
        if a.json:
            print(json.dumps({"error": msg}, ensure_ascii=False))
        else:
            print(f"エラー: {msg}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        where = r["place"] or f"({r['latitude']}, {r['longitude']})"
        print(f"{where} {r['time']}")
        print(f"  {r['weather']} {r['temperature_c']}℃ 湿度{r['humidity_pct']}% 風{r['wind_speed_kmh']}km/h")
        print(f"  出典: {r['source']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
