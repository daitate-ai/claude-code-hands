#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S24 日数差分 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM はうるう年や月跨ぎの日数計算を誤る。このスクリプトは
2日付の間隔、または「N日後/前」を必ず正確に返す。

使い方:
  python datediff.py 2026-07-17 2026-12-31   # 2日付の間隔
  python datediff.py 2026-07-17 +100         # 100日後の日付
  python datediff.py 2026-07-17 -30          # 30日前の日付
  python datediff.py 2026-07-17 2026-12-31 --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import datetime
import json
import re
import sys

WEEKDAYS_JA = ["月", "火", "水", "木", "金", "土", "日"]


def parse_date(s):
    return datetime.date.fromisoformat(s.strip().replace("/", "-"))


def date_diff(d1, d2):
    days = (d2 - d1).days
    return {
        "mode": "diff",
        "from": d1.isoformat(),
        "to": d2.isoformat(),
        "days": days,
        "days_abs": abs(days),
        "weeks": abs(days) // 7,
        "remainder_days": abs(days) % 7,
    }


def add_days(d, n):
    r = d + datetime.timedelta(days=n)
    return {
        "mode": "add",
        "from": d.isoformat(),
        "offset_days": n,
        "result": r.isoformat(),
        "weekday": WEEKDAYS_JA[r.weekday()],
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="日付の間隔・N日後を決定論的に計算する手足。")
    p.add_argument("date", help="基準日 (YYYY-MM-DD)")
    p.add_argument("second", help="比較日(YYYY-MM-DD) または オフセット(+100 / -30)")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    try:
        d1 = parse_date(a.date)
        if re.fullmatch(r"[+-]\d+", a.second.strip()):
            out = add_days(d1, int(a.second))
        else:
            out = date_diff(d1, parse_date(a.second))
    except ValueError as e:
        msg = f"日付を解釈できません: {e}"
        if a.json:
            print(json.dumps({"error": msg}, ensure_ascii=False))
        else:
            print(f"エラー: {msg}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps(out, ensure_ascii=False))
    elif out["mode"] == "diff":
        print(f"{out['from']} → {out['to']}: {out['days']}日 "
              f"({out['weeks']}週 {out['remainder_days']}日)")
    else:
        print(f"{out['from']} の {out['offset_days']:+d}日 → {out['result']} ({out['weekday']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
