#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L4 地震情報の回帰テスト。固定GeoJSONで解析・時刻変換・絞り込みを検証。"""

import sys
from quake import parse_quakes, fetch_quakes

# 実際の USGS GeoJSON と同じ形
def feat(mag, place, ms, lon, lat, depth):
    return {"type": "Feature",
            "properties": {"mag": mag, "place": place, "time": ms,
                           "url": "https://earthquake.usgs.gov/x"},
            "geometry": {"type": "Point", "coordinates": [lon, lat, depth]}}


FIXTURE = {"type": "FeatureCollection", "features": [
    feat(4.6, "206 km N of Hadibu, Yemen", 1784288919385, 54.0877, 14.5147, 10),
    feat(6.1, "off the east coast of Honshu, Japan", 1784200000000, 142.0, 38.0, 30),
    feat(3.0, "somewhere small", 1784100000000, 1.0, 2.0, 5),
]}


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    r = parse_quakes(FIXTURE)
    check("count", r["count"] == 3)
    # 新しい順に並ぶ
    check("sorted newest first", r["quakes"][0]["magnitude"] == 4.6)
    check("second", r["quakes"][1]["magnitude"] == 6.1)

    q = r["quakes"][0]
    check("place", q["place"] == "206 km N of Hadibu, Yemen")
    check("lon", q["longitude"] == 54.0877)
    check("lat", q["latitude"] == 14.5147)
    check("depth", q["depth_km"] == 10)
    # epochミリ秒 → UTC/JST(+9時間)。1784288919385ms の実際の変換値。
    check("utc", q["time_utc"] == "2026-07-17T11:48:39+00:00")
    check("jst", q["time_jst"] == "2026-07-17T20:48:39+09:00")

    # マグニチュード絞り込み
    big = parse_quakes(FIXTURE, min_mag=5)
    check("min_mag", big["count"] == 1 and big["quakes"][0]["magnitude"] == 6.1)
    check("total_matched", big["total_matched"] == 1)
    # 件数制限
    check("limit", parse_quakes(FIXTURE, limit=2)["count"] == 2)
    # 該当なし
    check("none", parse_quakes(FIXTURE, min_mag=9)["count"] == 0)

    # 出典と注意書き
    check("source", "USGS" in r["source"])
    check("note", "震度" in r["note"])

    # 不正形式は明示エラー
    for bad in [{}, {"features": None}, {"features": "x"}]:
        try:
            parse_quakes(bad)
            check(f"reject {bad}", False)
        except ValueError:
            pass
    # 未知フィードは取得前に弾く
    try:
        fetch_quakes("bogus_feed")
        check("reject feed", False)
    except ValueError:
        pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 解析/新しい順/UTC・JST変換/絞り込み/制限/不正形式 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
