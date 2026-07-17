#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S23 西暦和暦変換の回帰テスト。手足の価値=決定論的に正しいこと、を担保する。

  python test_wareki.py    # 全ケース検証。失敗0で exit 0。
"""

import sys
from wareki import parse_and_convert, WarekiError

# (入力, 期待するキー: 期待値) — 主要な境界を網羅
CASES = [
    # 西暦 → 和暦(日付)
    ("2024-05-01", {"era": "令和", "era_year": 6, "formatted": "令和6年5月1日"}),
    ("2019-05-01", {"era": "令和", "era_year": 1, "formatted": "令和元年5月1日"}),
    ("2019-04-30", {"era": "平成", "era_year": 31, "formatted": "平成31年4月30日"}),
    ("1989-01-08", {"era": "平成", "era_year": 1, "formatted": "平成元年1月8日"}),
    ("1989-01-07", {"era": "昭和", "era_year": 64, "formatted": "昭和64年1月7日"}),
    ("1926-12-25", {"era": "昭和", "era_year": 1, "formatted": "昭和元年12月25日"}),
    ("1926-12-24", {"era": "大正", "era_year": 15, "formatted": "大正15年12月24日"}),
    ("1912-07-30", {"era": "大正", "era_year": 1, "formatted": "大正元年7月30日"}),
    ("1912-07-29", {"era": "明治", "era_year": 45, "formatted": "明治45年7月29日"}),
    ("1868-10-23", {"era": "明治", "era_year": 1, "formatted": "明治元年10月23日"}),
    ("2024年5月1日", {"era": "令和", "era_year": 6}),
    ("2000/1/1", {"era": "平成", "era_year": 12}),
    # 西暦 → 和暦(年のみ・改元年は年末の元号が主)
    ("2019", {"era": "令和", "era_year": 1}),
    ("1989", {"era": "平成", "era_year": 1}),
    ("2023", {"era": "令和", "era_year": 5}),
    # 和暦 → 西暦
    ("令和6年5月1日", {"gregorian": "2024-05-01"}),
    ("令和元年", {"gregorian_year": 2019}),
    ("平成31年4月30日", {"gregorian": "2019-04-30"}),
    ("昭和64", {"gregorian_year": 1989}),
    ("昭和元年", {"gregorian_year": 1926}),
    ("大正15年", {"gregorian_year": 1926}),
    ("明治元年", {"gregorian_year": 1868}),
    ("R6", {"gregorian_year": 2024}),
    ("S39", {"gregorian_year": 1964}),   # 昭和39年=東京五輪
    ("H1", {"gregorian_year": 1989}),
    ("令和6", {"gregorian_year": 2024}),
]

ERROR_CASES = ["1867", "明治", "", "こんにちは", "令和0年"]


def run():
    failed = 0
    for raw, expect in CASES:
        try:
            got = parse_and_convert(raw)
        except WarekiError as e:
            print(f"FAIL {raw!r}: 予期せぬエラー {e}")
            failed += 1
            continue
        for k, v in expect.items():
            if got.get(k) != v:
                print(f"FAIL {raw!r}: {k}={got.get(k)!r} 期待={v!r}")
                failed += 1
    for raw in ERROR_CASES:
        try:
            parse_and_convert(raw)
            print(f"FAIL {raw!r}: エラーになるべきが通過した")
            failed += 1
        except WarekiError:
            pass
    total = sum(len(e) for _, e in CASES) + len(ERROR_CASES)
    if failed:
        print(f"\n{failed} 件失敗 / 全{total}検証")
        return 1
    print(f"OK: 全{total}検証パス({len(CASES)}変換 + {len(ERROR_CASES)}エラー検出)")
    return 0


if __name__ == "__main__":
    sys.exit(run())
