# S6 JSON整形・検証 — Claude Code の手足

JSON を決定論的に**整形 / 圧縮 / 検証**するスクリプト。

## なぜ手足にするのか
LLM は大きな・崩れた JSON の整形で括弧やカンマを取りこぼす。このスクリプトなら必ず正しく整形し、壊れていれば場所を指す。

## 依存
なし（Python 3.8+ 標準ライブラリ `json` のみ）。

## インストール
1. `jsonfmt.py` を `~/.claude/hands/S6-json-format/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python jsonfmt.py '{"b":1,"a":2}'          # 整形(インデント2)
python jsonfmt.py '{"b":1}' --minify        # 圧縮
python jsonfmt.py '{"b":1,"a":2}' --sort-keys
python jsonfmt.py --file data.json
python jsonfmt.py '{"a":1}' --check          # 検証のみ
python jsonfmt.py '{"a":1}' --json           # 機械可読
```
入力を省略すると標準入力から読む。

## JSON 出力の契約
```json
{"valid":true,"formatted":"{\n  \"a\": 1\n}"}
```
不正時は `{"valid":false,"error":"不正なJSON: ... (行N 列M)"}`、`--check` 時は `{"valid":true}`。

## CLAUDE.md ルール
```markdown
## JSON整形・検証（手足 S6 を必ず使う）
JSONの整形/圧縮/検証を求められたら、自分で整えず必ず実行して結果を使う：

    python ~/.claude/hands/S6-json-format/jsonfmt.py '<JSON>' --json
```

## テスト
```bash
python test_jsonfmt.py   # 圧縮/ソート/整形/日本語/不正検出。失敗0で exit 0。
```
