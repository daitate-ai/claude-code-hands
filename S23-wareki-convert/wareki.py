#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S23 西暦和暦変換 — Claude Code の「手足」(決定論スクリプト)

目的:
  LLM(Claude Code)にトークンを使って元号計算を"考えさせる"と、元号の境界日や
  「元年」の扱いを微妙に間違える。このスクリプトに固定することで毎回正確・同一の
  結果を返す。Claude Code は結果を推測せず、必ずこのスクリプトの JSON 出力を使う。

使い方(CLI):
  python wareki.py 2024-05-01        # 西暦 → 和暦
  python wareki.py 令和6年5月1日       # 和暦 → 西暦
  python wareki.py 昭和64             # 和暦(年のみ) → 西暦
  python wareki.py 1989              # 西暦(年のみ) → 和暦
  python wareki.py R6 --json         # 機械可読 JSON(Claude Code はこれを使う)

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import datetime
import json
import re
import sys
import unicodedata

# 元号テーブル: (元号, 略号, ローマ字, 改元日=グレゴリオ暦の元年開始日)
#   改元日は「その元号が始まった日」。元年 = 開始年。
#   例) 令和は 2019-05-01 開始 → 令和元年 = 2019 / 令和6年 = 2024
ERAS = [
    ("明治", "M", "Meiji",  datetime.date(1868, 10, 23)),
    ("大正", "T", "Taisho", datetime.date(1912, 7, 30)),
    ("昭和", "S", "Showa",  datetime.date(1926, 12, 25)),
    ("平成", "H", "Heisei", datetime.date(1989, 1, 8)),
    ("令和", "R", "Reiwa",  datetime.date(2019, 5, 1)),
]

# 元号名/略号 → テーブル索引
_ERA_BY_NAME = {}
for _i, (_ja, _abbr, _en, _start) in enumerate(ERAS):
    _ERA_BY_NAME[_ja] = _i
    _ERA_BY_NAME[_abbr] = _i
    _ERA_BY_NAME[_abbr.lower()] = _i
    _ERA_BY_NAME[_en.lower()] = _i

EARLIEST = ERAS[0][3]  # 明治改元日。これより前は非対応(和暦以前 / 旧暦)


class WarekiError(ValueError):
    """変換不能な入力に対して送出。"""


def _normalize(s: str) -> str:
    """全角英数を半角に、余分な空白を除去して素直な形にする。"""
    s = unicodedata.normalize("NFKC", s.strip())
    return s


def _era_index_for_date(d: datetime.date) -> int:
    """グレゴリオ暦の日付が属する元号の索引を返す。"""
    if d < EARLIEST:
        raise WarekiError(
            f"{d.isoformat()} は明治改元({EARLIEST.isoformat()})より前で非対応です。"
        )
    idx = 0
    for i, (_ja, _abbr, _en, start) in enumerate(ERAS):
        if d >= start:
            idx = i
        else:
            break
    return idx


def gregorian_to_wareki(year, month=None, day=None):
    """西暦 → 和暦。month/day 省略時は年のみ変換(境界年は注記付き)。"""
    notes = []
    if month and day:
        d = datetime.date(year, month, day)
        idx = _era_index_for_date(d)
        ja, abbr, en, start = ERAS[idx]
        era_year = year - start.year + 1
        return {
            "direction": "gregorian_to_wareki",
            "input_kind": "date",
            "gregorian": d.isoformat(),
            "era": ja,
            "era_abbr": abbr,
            "era_en": en,
            "era_year": era_year,
            "era_year_label": "元" if era_year == 1 else str(era_year),
            "formatted": f"{ja}{'元' if era_year == 1 else era_year}年{month}月{day}日",
            "notes": notes,
        }

    # --- 年のみ ---
    # その年に改元があるか(=複数の元号にまたがるか)を調べる
    matches = []
    for i, (ja, abbr, en, start) in enumerate(ERAS):
        # 次の元号の開始年
        next_start_year = ERAS[i + 1][3].year if i + 1 < len(ERAS) else None
        in_range = start.year <= year and (next_start_year is None or year <= next_start_year)
        if in_range:
            matches.append(i)
    if not matches:
        raise WarekiError(f"{year}年 は対応範囲(明治以降)外です。")

    # 年末時点で有効な元号を主結果にする(慣例)
    primary = matches[-1]
    ja, abbr, en, start = ERAS[primary]
    era_year = year - start.year + 1

    if len(matches) > 1:
        # 改元年: 主(年末)以外の元号も併記
        alt = []
        for i in matches[:-1]:
            aja, aabbr, aen, astart = ERAS[i]
            change = ERAS[i + 1][3]
            aey = year - astart.year + 1
            alt.append({
                "era": aja, "era_year": aey,
                "era_year_label": "元" if aey == 1 else str(aey),
                "until": (change - datetime.timedelta(days=1)).isoformat(),
            })
        change_here = ERAS[primary][3]
        notes.append(
            f"{year}年は改元年です。{change_here.isoformat()}以降が{ja}"
            f"{'元' if era_year == 1 else era_year}年、それ以前は "
            + " / ".join(f"{a['era']}{a['era_year_label']}年(〜{a['until']})" for a in alt)
            + "。正確には月日を指定してください。"
        )
    else:
        alt = []

    return {
        "direction": "gregorian_to_wareki",
        "input_kind": "year",
        "gregorian": str(year),
        "era": ja,
        "era_abbr": abbr,
        "era_en": en,
        "era_year": era_year,
        "era_year_label": "元" if era_year == 1 else str(era_year),
        "formatted": f"{ja}{'元' if era_year == 1 else era_year}年",
        "alternatives": alt,
        "notes": notes,
    }


def wareki_to_gregorian(era_key, era_year, month=None, day=None):
    """和暦 → 西暦。"""
    if era_key not in _ERA_BY_NAME:
        raise WarekiError(f"未知の元号: {era_key!r}(対応: 明治/大正/昭和/平成/令和)")
    idx = _ERA_BY_NAME[era_key]
    ja, abbr, en, start = ERAS[idx]
    if era_year < 1:
        raise WarekiError("和暦の年は1(元年)以上で指定してください。")
    greg_year = start.year + era_year - 1

    notes = []
    # その元号の存在範囲を超えていないか軽くチェック
    if idx + 1 < len(ERAS):
        next_start = ERAS[idx + 1][3]
        # 元号の最終年(次の改元年)
        last_year = next_start.year
        if greg_year > last_year:
            notes.append(
                f"{ja}は{ERAS[idx+1][0]}への改元({next_start.isoformat()})で終わっています。"
                f"{ja}{era_year}年は実在しない可能性があります。"
            )

    result = {
        "direction": "wareki_to_gregorian",
        "era": ja,
        "era_abbr": abbr,
        "era_en": en,
        "era_year": era_year,
        "era_year_label": "元" if era_year == 1 else str(era_year),
        "gregorian_year": greg_year,
        "notes": notes,
    }
    if month and day:
        d = datetime.date(greg_year, month, day)
        result["input_kind"] = "date"
        result["gregorian"] = d.isoformat()
        result["formatted"] = d.isoformat()
    else:
        result["input_kind"] = "year"
        result["gregorian"] = str(greg_year)
        result["formatted"] = str(greg_year)
    return result


# --- 入力パース ---------------------------------------------------------------

_ERA_ALT = "|".join(sorted(_ERA_BY_NAME.keys(), key=len, reverse=True))
_RE_WAREKI = re.compile(
    r"^(?P<era>" + _ERA_ALT + r")\s*"
    r"(?P<y>元|\d{1,2})\s*年?\s*"
    r"(?:(?P<m>\d{1,2})\s*月\s*(?P<d>\d{1,2})\s*日?)?$"
)
_RE_GREG = re.compile(
    r"^(?P<y>\d{3,4})\s*(?:年|[-/])?\s*"
    r"(?:(?P<m>\d{1,2})\s*(?:月|[-/])\s*(?P<d>\d{1,2})\s*日?)?$"
)


def parse_and_convert(raw: str) -> dict:
    """入力文字列から向きを自動判定して変換する。"""
    s = _normalize(raw)
    if not s:
        raise WarekiError("入力が空です。")

    m = _RE_WAREKI.match(s)
    if m:
        era = m.group("era")
        y = 1 if m.group("y") == "元" else int(m.group("y"))
        mo = int(m.group("m")) if m.group("m") else None
        da = int(m.group("d")) if m.group("d") else None
        return wareki_to_gregorian(era, y, mo, da)

    m = _RE_GREG.match(s)
    if m:
        y = int(m.group("y"))
        mo = int(m.group("m")) if m.group("m") else None
        da = int(m.group("d")) if m.group("d") else None
        return gregorian_to_wareki(y, mo, da)

    raise WarekiError(
        f"入力を解釈できません: {raw!r}\n"
        "例) 2024-05-01 / 令和6年5月1日 / 昭和64 / 1989 / R6"
    )


def main(argv=None):
    p = argparse.ArgumentParser(
        description="西暦↔和暦を決定論的に変換する手足(Claude Code 用)。",
    )
    p.add_argument("input", nargs="+", help="西暦 or 和暦(例: 2024-05-01, 令和6年, 昭和64)")
    p.add_argument("--json", action="store_true", help="機械可読なJSONで出力(Claude Codeはこれを使う)")
    args = p.parse_args(argv)

    raw = " ".join(args.input)
    try:
        result = parse_and_convert(raw)
    except WarekiError as e:
        if args.json:
            print(json.dumps({"error": str(e), "input": raw}, ensure_ascii=False))
        else:
            print(f"エラー: {e}", file=sys.stderr)
        return 2

    result["input"] = raw
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(result["formatted"])
        for note in result.get("notes", []):
            print(f"  ※ {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
