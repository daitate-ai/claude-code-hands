#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S15 カラー変換 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM は HEX→HSL などの色空間変換をよく誤る(特にHSLの計算)。
このスクリプトは HEX / RGB / HSL を必ず正確に相互変換する。

使い方:
  python color.py "#FF6A3D"
  python color.py "rgb(255,106,61)"
  python color.py "hsl(15,100%,62%)"
  python color.py "#FF0000" --json

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import json
import re
import sys


def parse_color(s):
    """HEX / rgb() / hsl() を (r,g,b) 0-255 に。"""
    s = s.strip()
    m = re.fullmatch(r"#?([0-9a-fA-F]{6})", s)
    if m:
        h = m.group(1)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = re.fullmatch(r"#?([0-9a-fA-F]{3})", s)
    if m:
        h = m.group(1)
        return tuple(int(c * 2, 16) for c in h)
    m = re.fullmatch(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", s, re.I)
    if m:
        rgb = tuple(int(x) for x in m.groups())
        if any(v > 255 for v in rgb):
            raise ValueError("RGB各値は0-255です。")
        return rgb
    m = re.fullmatch(r"hsla?\(\s*(-?[\d.]+)\s*,\s*([\d.]+)%?\s*,\s*([\d.]+)%?\s*\)", s, re.I)
    if m:
        h, sv, lv = (float(x) for x in m.groups())
        return hsl_to_rgb(h, sv, lv)
    raise ValueError(f"色として解釈できません: {s!r}（例: #FF6A3D / rgb(255,106,61) / hsl(15,100%,62%)）")


def rgb_to_hsl(r, g, b):
    r_, g_, b_ = r / 255, g / 255, b / 255
    mx, mn = max(r_, g_, b_), min(r_, g_, b_)
    l = (mx + mn) / 2
    if mx == mn:
        return 0.0, 0.0, l * 100
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r_:
        h = ((g_ - b_) / d) % 6
    elif mx == g_:
        h = (b_ - r_) / d + 2
    else:
        h = (r_ - g_) / d + 4
    return h * 60 % 360, s * 100, l * 100


def hsl_to_rgb(h, s, l):
    h = h % 360
    s, l = s / 100, l / 100
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    seg = int(h // 60) % 6
    r1, g1, b1 = [(c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x)][seg]
    return tuple(round((v + m) * 255) for v in (r1, g1, b1))


def describe(s):
    r, g, b = parse_color(s)
    h, sv, lv = rgb_to_hsl(r, g, b)
    return {
        "input": s,
        "hex": "#{:02X}{:02X}{:02X}".format(r, g, b),
        "rgb": f"rgb({r},{g},{b})",
        "rgb_values": [r, g, b],
        "hsl": f"hsl({round(h)},{round(sv)}%,{round(lv)}%)",
        "hsl_values": [round(h, 1), round(sv, 1), round(lv, 1)],
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="HEX/RGB/HSL を決定論的に相互変換する手足。")
    p.add_argument("color", help="#FF6A3D / rgb(255,106,61) / hsl(15,100%%,62%%)")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    try:
        r = describe(a.color)
    except ValueError as e:
        if a.json:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
        else:
            print(f"エラー: {e}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        print(f"HEX {r['hex']}")
        print(f"RGB {r['rgb']}")
        print(f"HSL {r['hsl']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
