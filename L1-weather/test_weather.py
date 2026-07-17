#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L1 天気の回帰テスト。

ネットワークに依存させないため、実APIと同じ形の固定データ(fixture)で
解析部 parse_weather() を検証する。取得部(fetch_weather)は CLI 実行で確認する。
"""

import sys
from weather import parse_weather, WMO

# 実際の Open-Meteo レスポンスと同じ形
FIXTURE = {
    "latitude": 35.68, "longitude": 139.76, "timezone": "Asia/Tokyo",
    "current_units": {"temperature_2m": "°C"},
    "current": {
        "time": "2026-07-17T21:00", "interval": 900,
        "temperature_2m": 25.6, "relative_humidity_2m": 92,
        "weather_code": 2, "wind_speed_10m": 5.2,
    },
}


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    r = parse_weather(FIXTURE, place="東京")
    check("place", r["place"] == "東京")
    check("temp", r["temperature_c"] == 25.6)
    check("humidity", r["humidity_pct"] == 92)
    check("wind", r["wind_speed_kmh"] == 5.2)
    check("time", r["time"] == "2026-07-17T21:00")
    check("code", r["weather_code"] == 2)
    check("weather ja", r["weather"] == "一部曇り")
    check("lat/lon", r["latitude"] == 35.68 and r["longitude"] == 139.76)
    check("source", "Open-Meteo" in r["source"])

    # 主要な天気コードが日本語化される
    check("code 0", WMO[0] == "快晴")
    check("code 61", WMO[61] == "弱い雨")
    check("code 95", WMO[95] == "雷雨")
    # 未知コードでも落ちない
    unknown = dict(FIXTURE, current=dict(FIXTURE["current"], weather_code=999))
    check("unknown code", "不明" in parse_weather(unknown)["weather"])

    # 形式が違えば明示的にエラー(黙って推測しない)
    for bad in [{}, {"current": None}, {"current": "x"}]:
        try:
            parse_weather(bad)
            check(f"reject {bad}", False)
        except ValueError:
            pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 解析/日本語天気/未知コード/不正形式 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
