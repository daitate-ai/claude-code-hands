#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
O1 正確時刻・日付手足（now）— Claude Code の「手足」(決定論スクリプト)

なぜ手足が要るか（"純度100%"デモ）:
  LLM(Claude Code)は時計を内蔵していない。日付は毎回ハーネスが外から注入して
  初めて分かる。注入が無い場面（サブエージェント／スクリプト／長いセッション）
  では"それっぽい日付"を書いてしまう＝日付のハルシネーション。
  さらに PC=JST / サーバー=UTC の9時間差で日付が前後する。
  この手足を登録し「日時は必ずここから取得・推測禁止・絶対表記に変換」と決めれば、
  時刻は絶対にズレない。

使い方(CLI):
  python now.py            # JST と UTC を表示
  python now.py --json     # 機械可読JSON(Claude Codeはこれを使う)

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import datetime
import json

# JSTは夏時間が無いので固定オフセット(+09:00)。zoneinfo/tzdata不要=どの環境でも同じ。
JST = datetime.timezone(datetime.timedelta(hours=9), "JST")
WEEKDAYS_JA = ["月", "火", "水", "木", "金", "土", "日"]


def snapshot(now_utc):
    """aware な UTC datetime を受け取り、時刻情報の dict を返す純関数（テスト可能）。"""
    now_utc = now_utc.astimezone(datetime.timezone.utc).replace(microsecond=0)
    now_jst = now_utc.astimezone(JST)
    return {
        "utc": now_utc.isoformat(),
        "jst": now_jst.isoformat(),
        "date_jst": now_jst.date().isoformat(),
        "date_utc": now_utc.date().isoformat(),
        "weekday_jst": WEEKDAYS_JA[now_jst.weekday()],
        "time_jst": now_jst.strftime("%H:%M:%S"),
        "unix": int(now_utc.timestamp()),
        "date_differs": now_jst.date() != now_utc.date(),
        "note": (
            "日時はこの手足の値を使い、推測しない。"
            "日付が要る箇所は date_jst を絶対表記(YYYY-MM-DD)で使う。"
            "サーバー(UTC)とPC(JST)で日付が違う場合があるため date_jst / date_utc を取り違えない。"
        ),
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="現在の日時を決定論的に返す手足(Claude Code 用)。")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力(Claude Codeはこれを使う)")
    args = p.parse_args(argv)

    snap = snapshot(datetime.datetime.now(datetime.timezone.utc))
    if args.json:
        print(json.dumps(snap, ensure_ascii=False))
    else:
        flag = "  ※JSTとUTCで日付が違います" if snap["date_differs"] else ""
        print(f"JST {snap['jst']} ({snap['weekday_jst']}){flag}")
        print(f"UTC {snap['utc']}")
        print(f"日付(絶対表記): {snap['date_jst']} (JST)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
