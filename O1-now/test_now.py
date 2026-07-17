#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O1 正確時刻・日付手足の回帰テスト。

時刻自体は動くので、純関数 snapshot() に固定の UTC を与えて
「変換・書式・JST/UTCの日付ズレ検知」が決定論的に正しいことを担保する。

  python test_now.py    # 失敗0で exit 0。
"""

import datetime
import sys
from now import snapshot

UTC = datetime.timezone.utc


def run():
    failed = 0

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # 通常ケース: 2026-07-17 01:23:45 UTC → JST 10:23:45(金)
    s = snapshot(datetime.datetime(2026, 7, 17, 1, 23, 45, tzinfo=UTC))
    check("utc iso", s["utc"] == "2026-07-17T01:23:45+00:00")
    check("jst iso", s["jst"] == "2026-07-17T10:23:45+09:00")
    check("date_jst", s["date_jst"] == "2026-07-17")
    check("date_utc", s["date_utc"] == "2026-07-17")
    check("weekday", s["weekday_jst"] == "金")
    check("time_jst", s["time_jst"] == "10:23:45")
    check("no drift", s["date_differs"] is False)

    # 日付ズレの肝: UTC 2026-07-16 15:30 → JST 2026-07-17 00:30(日付が+1)
    d = snapshot(datetime.datetime(2026, 7, 16, 15, 30, 0, tzinfo=UTC))
    check("drift date_utc", d["date_utc"] == "2026-07-16")
    check("drift date_jst", d["date_jst"] == "2026-07-17")
    check("drift flag", d["date_differs"] is True)

    # マイクロ秒は落とす / unix は整数
    m = snapshot(datetime.datetime(2026, 1, 1, 0, 0, 0, 999999, tzinfo=UTC))
    check("microsecond dropped", m["utc"] == "2026-01-01T00:00:00+00:00")
    check("unix int", isinstance(m["unix"], int) and m["unix"] == 1767225600)

    # naive でない別TZ入力も UTC 基準に正規化される(JST入力 → 同じ瞬間)
    n = snapshot(datetime.datetime(2026, 7, 17, 10, 23, 45,
                                   tzinfo=datetime.timezone(datetime.timedelta(hours=9))))
    check("tz-normalize utc", n["utc"] == "2026-07-17T01:23:45+00:00")

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: 全検証パス(通常 / 日付ズレ / 桁処理 / TZ正規化)")
    return 0


if __name__ == "__main__":
    sys.exit(run())
