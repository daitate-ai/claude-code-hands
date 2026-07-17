#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S7 JSON⇔CSV変換 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: LLM は表の変換で列ズレ・引用符・カンマ入りセルを壊す。
このスクリプトは csv モジュールで必ず正しく相互変換する。

注意: YAML は標準ライブラリに無いため対象外(pip不要の方針を守るため)。

使い方:
  python jsoncsv.py to-csv '[{"a":1,"b":2},{"a":3,"b":4}]'
  python jsoncsv.py to-json --file data.csv
  echo 'a,b\\n1,2' | python jsoncsv.py to-json

依存: なし(Python 3.8+ 標準ライブラリ json / csv のみ)
"""

import argparse
import csv
import io
import json
import sys


def json_to_csv(text):
    data = json.loads(text)
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list) or not all(isinstance(r, dict) for r in data):
        raise ValueError("JSONはオブジェクトの配列（または単一オブジェクト）にしてください。")
    if not data:
        return ""
    keys = []
    for row in data:  # 出現順で列を決める(union)
        for k in row:
            if k not in keys:
                keys.append(k)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=keys, lineterminator="\n")
    w.writeheader()
    for row in data:
        w.writerow({k: row.get(k, "") for k in keys})
    return buf.getvalue()


def csv_to_json(text, minify=False):
    rows = [dict(r) for r in csv.DictReader(io.StringIO(text))]
    return json.dumps(rows, ensure_ascii=False,
                      separators=(",", ":") if minify else None,
                      indent=None if minify else 2)


def main(argv=None):
    p = argparse.ArgumentParser(description="JSON⇔CSVを決定論的に変換する手足。")
    p.add_argument("mode", choices=["to-csv", "to-json"])
    p.add_argument("input", nargs="*", help="入力(省略時は標準入力)")
    p.add_argument("--file", help="このファイルを読む")
    p.add_argument("--minify", action="store_true", help="to-json時に圧縮")
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

    try:
        out = json_to_csv(text) if a.mode == "to-csv" else csv_to_json(text, a.minify)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"エラー: 変換できません: {e}", file=sys.stderr)
        return 2

    print(out, end="" if a.mode == "to-csv" else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
