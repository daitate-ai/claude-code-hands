#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
O11 出典接地 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM は「出典にあった風」の引用を作る(引用のねつ造)。
少し言い回しが違うだけでも、引用としては誤り。このスクリプトは
出典ファイルに"その通りの文字列"が実在するかを機械的に照合し、
無ければ最も近い箇所と一致度を示す(=どう違うかが分かる)。

使い方:
  python quotecheck.py "引用したい一文" --file source.md
  python quotecheck.py "引用" --file source.md --normalize-space
  python quotecheck.py "引用" --file source.md --json

exit code: 出典に見つからなければ 1 (=その引用を使わない合図)

依存: なし(Python 3.8+ 標準ライブラリ difflib のみ)
"""

import argparse
import difflib
import json
import re
import sys


def _ws(s):
    return re.sub(r"\s+", " ", s).strip()


def check_quote(quote, source, normalize=False):
    q = _ws(quote) if normalize else quote
    src = _ws(source) if normalize else source

    if q and q in src:
        r = {"quote": quote, "found": True, "similarity": 1.0,
             "normalized": normalize,
             "reason": "出典に一致する記述があります（引用して差し支えありません）"}
        if not normalize:
            r["line"] = source[:src.index(q)].count("\n") + 1
        return r

    # 見つからない → 最も近い行を示す(どこが違うか分かるように)
    best_ratio, best_line, best_text = 0.0, None, None
    for i, line in enumerate(source.splitlines(), 1):
        cand = _ws(line) if normalize else line
        ratio = difflib.SequenceMatcher(None, q, cand).ratio()
        if ratio > best_ratio:
            best_ratio, best_line, best_text = ratio, i, line
    return {
        "quote": quote,
        "found": False,
        "similarity": round(best_ratio, 3),
        "closest": best_text,
        "closest_line": best_line,
        "normalized": normalize,
        "reason": "出典に見つかりません（言い回しが違う＝引用のねつ造の可能性）",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="引用が出典に実在するか照合する手足。")
    p.add_argument("quote", help="引用しようとしている文字列")
    p.add_argument("--file", required=True, help="出典ファイル")
    p.add_argument("--normalize-space", action="store_true",
                   help="空白・改行の違いを無視して照合")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    try:
        with open(a.file, encoding="utf-8") as f:
            source = f.read()
    except OSError as e:
        msg = f"出典ファイルを開けません: {e}"
        if a.json:
            print(json.dumps({"error": msg}, ensure_ascii=False))
        else:
            print(f"エラー: {msg}", file=sys.stderr)
        return 2

    r = check_quote(a.quote, source, a.normalize_space)
    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    elif r["found"]:
        print(f"一致（{a.file}"
              + (f" の {r['line']}行目" if "line" in r else "") + "）")
    else:
        print(f"見つかりません（最も近い箇所: {a.file} の {r['closest_line']}行目 "
              f"/ 一致度 {r['similarity']}）")
        print(f"  近い記述: {r['closest']!r}")
    return 0 if r["found"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
