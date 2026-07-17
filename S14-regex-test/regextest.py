#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S14 正規表現テスター — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM は正規表現が何にマッチするかを誤って予測する。
このスクリプトは実際に re でマッチさせ、位置・グループを正確に返す。

使い方:
  python regextest.py "\\d+" "abc 123 def 456"
  python regextest.py "(\\w+)@(\\w+)" "a@b c@d" --json
  python regextest.py "foo" "FOO" -i          # 大小無視

依存: なし(Python 3.8+ 標準ライブラリ re のみ)
"""

import argparse
import json
import re
import sys


def find_matches(pattern, text, flags=0):
    rx = re.compile(pattern, flags)
    out = []
    for m in rx.finditer(text):
        out.append({
            "match": m.group(0),
            "start": m.start(),
            "end": m.end(),
            "groups": list(m.groups()),
        })
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description="正規表現を実際に適用してマッチを返す手足。")
    p.add_argument("pattern", help="正規表現パターン")
    p.add_argument("text", help="対象テキスト")
    p.add_argument("-i", "--ignorecase", action="store_true")
    p.add_argument("-m", "--multiline", action="store_true")
    p.add_argument("-s", "--dotall", action="store_true")
    p.add_argument("--json", action="store_true", help="機械可読JSONで出力")
    a = p.parse_args(argv)

    flags = 0
    if a.ignorecase:
        flags |= re.IGNORECASE
    if a.multiline:
        flags |= re.MULTILINE
    if a.dotall:
        flags |= re.DOTALL

    try:
        matches = find_matches(a.pattern, a.text, flags)
    except re.error as e:
        msg = f"不正な正規表現: {e}"
        if a.json:
            print(json.dumps({"error": msg, "pattern": a.pattern}, ensure_ascii=False))
        else:
            print(f"エラー: {msg}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps({"pattern": a.pattern, "match_count": len(matches),
                          "matches": matches}, ensure_ascii=False))
    else:
        print(f"{len(matches)} 件マッチ")
        for m in matches:
            g = f"  groups={m['groups']}" if m["groups"] else ""
            print(f"  [{m['start']}:{m['end']}] {m['match']!r}{g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
