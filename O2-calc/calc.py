#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
O2 算術・カウント手足 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM は暗算を間違える。特に桁の多い掛け算・累乗で静かに誤る。
このスクリプトは式を実際に計算して返す。整数は多倍長で厳密。

安全性: eval は使わない。ast で構文木を解析し、算術演算のみを許可する
        (関数呼び出し・変数・属性アクセスは全て拒否)。

使い方:
  python calc.py "1234*5678"
  python calc.py "(1+2)**10"
  python calc.py "7/2" --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import ast
import json
import operator
import sys

OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod, ast.Pow: operator.pow,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}
MAX_EXPONENT = 10000  # 巨大累乗で固まるのを防ぐ


def _eval(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise ValueError("数値以外は使えません。")
        return node.value
    if isinstance(node, ast.BinOp):
        op = OPS.get(type(node.op))
        if op is None:
            raise ValueError("使用できない演算子です。")
        left, right = _eval(node.left), _eval(node.right)
        if isinstance(node.op, ast.Pow) and isinstance(right, int) and right > MAX_EXPONENT:
            raise ValueError(f"指数が大きすぎます(上限 {MAX_EXPONENT})。")
        return op(left, right)
    if isinstance(node, ast.UnaryOp):
        op = OPS.get(type(node.op))
        if op is None:
            raise ValueError("使用できない演算子です。")
        return op(_eval(node.operand))
    raise ValueError("算術式に使えない要素が含まれています。")


def calc(expression):
    """算術式を評価する。許可するのは数値と + - * / // % ** と括弧のみ。"""
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"式を解釈できません: {e.msg}")
    return _eval(tree.body)


def main(argv=None):
    p = argparse.ArgumentParser(description="算術式を実際に計算する手足(暗算させない)。")
    p.add_argument("expression", nargs="+", help="算術式")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    expr = " ".join(a.expression)
    try:
        result = calc(expr)
    except (ValueError, ZeroDivisionError, OverflowError) as e:
        if a.json:
            print(json.dumps({"expression": expr, "error": str(e)}, ensure_ascii=False))
        else:
            print(f"エラー: {e}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps({"expression": expr, "result": result,
                          "type": type(result).__name__}, ensure_ascii=False))
    else:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
