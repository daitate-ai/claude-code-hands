#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S25 ローン返済の回帰テスト。PMT・無利子・総額を担保。"""

import sys
from loan import monthly_payment


def run():
    failed = 0

    def close(a, b, tol=0.01):
        return abs(a - b) <= tol

    def check(label, cond):
        nonlocal failed
        if not cond:
            print(f"FAIL {label}")
            failed += 1

    # 独立参照値: 元金100万・年利12%・12回 → 毎月 ≈ 88,848.79
    # (total_paid は丸め前の月額×12 なので、表示月額×12 とは数銭ずれる)
    r = monthly_payment(1000000, 12, 12)
    check("PMT", close(r["monthly_payment"], 88848.79))
    check("total_paid", close(r["total_paid"], 88848.79 * 12, tol=0.5))
    check("interest", close(r["total_interest"], r["total_paid"] - 1000000, tol=0.02))

    # 無利子は 元金/回数
    z = monthly_payment(1200, 0, 12)
    check("zero-rate PMT", z["monthly_payment"] == 100.0)
    check("zero-rate interest", z["total_interest"] == 0.0)

    # 不正期間
    try:
        monthly_payment(1000, 5, 0)
        check("reject 0 months", False)
    except ValueError:
        pass

    if failed:
        print(f"\n{failed} 件失敗")
        return 1
    print("OK: PMT参照値/無利子/総額/不正期間 全パス")
    return 0


if __name__ == "__main__":
    sys.exit(run())
