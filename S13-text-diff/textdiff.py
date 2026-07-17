#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S13 テキスト差分 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM は2つの文章の差分を正確に取れず、変わっていない行を
"変わった"と言ったりする。このスクリプトは unified diff を必ず正しく出す。

使い方:
  python textdiff.py old.txt new.txt          # 2ファイルの差分
  python textdiff.py "a b c" "a B c" --text    # 文字列として比較
  python textdiff.py old.txt new.txt --json

依存: なし(Python 3.8+ 標準ライブラリ difflib のみ)
"""

import argparse
import difflib
import json
import sys


def diff_texts(old, new):
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    ud = list(difflib.unified_diff(old_lines, new_lines, lineterm=""))
    added = sum(1 for l in ud if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in ud if l.startswith("-") and not l.startswith("---"))
    return {"added": added, "removed": removed, "changed": added > 0 or removed > 0,
            "diff": "\n".join(ud)}


def main(argv=None):
    p = argparse.ArgumentParser(description="2つのテキストの差分を決定論的に出す手足。")
    p.add_argument("a", help="旧(ファイルパス、--text時は文字列)")
    p.add_argument("b", help="新(ファイルパス、--text時は文字列)")
    p.add_argument("--text", action="store_true", help="引数を文字列として扱う")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    if a.text:
        old, new = a.a, a.b
    else:
        try:
            with open(a.a, encoding="utf-8") as f:
                old = f.read()
            with open(a.b, encoding="utf-8") as f:
                new = f.read()
        except OSError as e:
            print(f"エラー: ファイルを開けません: {e}", file=sys.stderr)
            return 2

    r = diff_texts(old, new)
    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        print(r["diff"] if r["diff"] else "(差分なし)")
        print(f"\n+{r['added']} / -{r['removed']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
