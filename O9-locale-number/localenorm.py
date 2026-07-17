#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
O9 ロケール正規化 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: "1.234,56"(欧州)を 1.23 と読み、"1,234"(米国)を 1.234 と読む —
桁区切りと小数点の流儀違いは、LLM が静かに1000倍間違える所。全角数字・
通貨記号・会計式の括弧マイナスも取りこぼす。このスクリプトは明示ルールで
正規化し、曖昧な入力は ambiguous として申告する。

使い方:
  python localenorm.py "1,234.56"      # 米国式 → 1234.56
  python localenorm.py "1.234,56"      # 欧州式 → 1234.56
  python localenorm.py "１２３４"         # 全角 → 1234
  python localenorm.py "1.234" --style eu   # 流儀を明示 → 1234
  python localenorm.py "¥1,234" --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import re
import sys
import unicodedata

CURRENCIES = "¥$€£₩"


def normalize_number(s, style="auto"):
    original = s
    t = unicodedata.normalize("NFKC", s).strip()  # 全角→半角

    is_percent = t.endswith("%")
    if is_percent:
        t = t[:-1].strip()

    currency = None
    for sym in CURRENCIES:
        if sym in t:
            currency = sym
            t = t.replace(sym, "")
    if "円" in t:
        currency = "円"
        t = t.replace("円", "")

    t = re.sub(r"[\s  _']", "", t)  # 空白系・アンダースコア・アポストロフィ

    neg = False
    if t.startswith("(") and t.endswith(")"):  # 会計式のマイナス
        neg = True
        t = t[1:-1]
    if t.startswith("-"):
        neg = True
        t = t[1:]
    elif t.startswith("+"):
        t = t[1:]
    if not t:
        raise ValueError(f"数値として解釈できません: {original!r}")

    ambiguous = False
    has_c, has_d = "," in t, "." in t

    if has_c and has_d:
        # 両方あるなら「後ろにある方」が小数点
        dec = "," if t.rfind(",") > t.rfind(".") else "."
        thou = "." if dec == "," else ","
        detected = "eu" if dec == "," else "us"
        t = t.replace(thou, "").replace(dec, ".")
    elif has_c or has_d:
        sep = "," if has_c else "."
        count = t.count(sep)
        after = len(t.split(sep)[-1])
        if style == "us":
            role = "thousands" if sep == "," else "decimal"
        elif style == "eu":
            role = "decimal" if sep == "," else "thousands"
        elif count > 1:
            role = "thousands"
        elif after == 3:
            # 例: "1,234" も "1.234" も両方の解釈がありうる → 米国式を既定にして申告
            role = "thousands" if sep == "," else "decimal"
            ambiguous = True
        else:
            role = "decimal"
        if role == "thousands":
            t = t.replace(sep, "")
            detected = "us" if sep == "," else "eu"
        else:
            t = t.replace(sep, ".")
            detected = "eu" if sep == "," else "us"
    else:
        detected = "plain"

    if not re.fullmatch(r"\d+(\.\d+)?", t):
        raise ValueError(f"数値として解釈できません: {original!r}")

    value = float(t) if "." in t else int(t)
    if neg:
        value = -value

    return {
        "input": original,
        "value": value,
        "detected_style": detected,
        "ambiguous": ambiguous,
        "is_percent": is_percent,
        "currency": currency,
        "note": ("桁区切りと小数点の解釈が2通りありえます。--style us|eu で明示してください。"
                 if ambiguous else None),
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="各国式の数値表記を正規化する手足。")
    p.add_argument("input", help='"1,234.56" / "1.234,56" / "１２３４" など')
    p.add_argument("--style", choices=["auto", "us", "eu"], default="auto")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    try:
        r = normalize_number(a.input, a.style)
    except ValueError as e:
        if a.json:
            print(json.dumps({"input": a.input, "error": str(e)}, ensure_ascii=False))
        else:
            print(f"エラー: {e}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        print(r["value"])
        if r["ambiguous"]:
            print(f"  ※ {r['note']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
