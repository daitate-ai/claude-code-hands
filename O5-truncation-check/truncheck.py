#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
O5 truncation検知 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: 出力やファイルが途中で切れていても、LLM は"完結している"と
思い込んで先に進んでしまう。このスクリプトは機械的な手掛かり
(括弧・引用符・コードフェンスの不整合、終端記号の欠如)で切れを検知する。

使い方:
  python truncheck.py '{"a":1'          # 切れている
  python truncheck.py --file out.md
  python truncheck.py 'text' --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import sys

PAIRS = {"(": ")", "[": "]", "{": "}"}
CLOSERS = {v: k for k, v in PAIRS.items()}
TERMINALS = ".!?。！？…:;)]}\"'`>」』】”’"


def check(text):
    reasons = []

    # 1) コードフェンスの数が奇数 = 閉じていない
    if text.count("```") % 2 == 1:
        reasons.append("コードフェンス(```)が閉じていません")

    # 2) 括弧の対応(フェンス外・引用符外だけを見るのは過剰なので単純カウント)
    stack = []
    for ch in text:
        if ch in PAIRS:
            stack.append(ch)
        elif ch in CLOSERS:
            if stack and stack[-1] == CLOSERS[ch]:
                stack.pop()
            else:
                reasons.append(f"閉じ括弧 {ch} に対応する開き括弧がありません")
                break
    if stack:
        reasons.append(f"閉じられていない括弧: {''.join(stack)}")

    # 3) 引用符の数が奇数
    for q, name in (('"', "ダブルクォート"), ("'", "シングルクォート")):
        if text.count(q) % 2 == 1:
            reasons.append(f"{name}の数が奇数です")

    # 4) 終端記号なしで終わっている(空でない場合)
    stripped = text.rstrip()
    if stripped and stripped[-1] not in TERMINALS:
        reasons.append("文末が終端記号で終わっていません(途中で切れた可能性)")

    return {
        "likely_truncated": bool(reasons),
        "reasons": reasons,
        "length": len(text),
        "note": "機械的な手掛かりによる推定。完全な判定ではない。",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="出力が途中で切れていないか検知する手足。")
    p.add_argument("input", nargs="*", help="検査するテキスト(省略時は標準入力)")
    p.add_argument("--file", help="このファイルを検査")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    if a.file:
        try:
            with open(a.file, encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            print(f"エラー: ファイルを開けません: {e}", file=sys.stderr)
            return 2
    elif a.input:
        text = " ".join(a.input)
    else:
        text = sys.stdin.read()

    r = check(text)
    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        if r["likely_truncated"]:
            print("切れている可能性あり:")
            for x in r["reasons"]:
                print(f"  - {x}")
        else:
            print("完結しているように見えます")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
