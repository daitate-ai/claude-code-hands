#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
O4 ファイル状態ドリフト防止 — Claude Code の「手足」(決定論スクリプト)

なぜ手足か: 読んだ後に他所で変更されたファイルへ、そのまま上書きすると
変更が消える(クロバー事故)。このスクリプトは読んだ時点の指紋(sha256)を
記録し、書く前に「変わっていないか」を機械的に検証する。

使い方:
  python filestate.py snapshot notes.md            # 指紋を取る
  python filestate.py verify notes.md --sha256 <値> # 変わっていないか確認
  python filestate.py snapshot notes.md --json

exit code: verify で変更を検知したら 1 (=書き込みを止める合図)

依存: なし(Python 3.8+ 標準ライブラリのみ)
"""

import argparse
import hashlib
import json
import os
import sys


def snapshot(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    st = os.stat(path)
    return {"path": path, "sha256": h.hexdigest(), "size": st.st_size}


def verify(path, expected_sha256):
    try:
        snap = snapshot(path)
    except FileNotFoundError:
        return {"path": path, "changed": True, "reason": "ファイルが存在しません（削除された）"}
    changed = snap["sha256"] != expected_sha256
    return {
        "path": path,
        "changed": changed,
        "expected_sha256": expected_sha256,
        "actual_sha256": snap["sha256"],
        "size": snap["size"],
        "reason": "読み取り後に変更されています（上書きすると変更が消えます）" if changed
                  else "変更されていません（安全に書き込めます）",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="ファイルの変更を検知して上書き事故を防ぐ手足。")
    p.add_argument("mode", choices=["snapshot", "verify"])
    p.add_argument("path")
    p.add_argument("--sha256", help="verify時の期待ハッシュ")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    try:
        if a.mode == "snapshot":
            r = snapshot(a.path)
        else:
            if not a.sha256:
                raise ValueError("verify には --sha256 が必要です。")
            r = verify(a.path, a.sha256)
    except (OSError, ValueError) as e:
        if a.json:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
        else:
            print(f"エラー: {e}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    elif a.mode == "snapshot":
        print(f"sha256 {r['sha256']}  ({r['size']} bytes)")
    else:
        print(r["reason"])

    return 1 if a.mode == "verify" and r["changed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
