# S7 JSON⇔CSV変換 — Claude Code の手足

JSON（オブジェクトの配列）と CSV を決定論的に相互変換するスクリプト。

> **YAML は対象外**：標準ライブラリに無く、`pip install` 不要の方針を守るため。JSON⇔CSV のみ。

## なぜ手足にするのか
LLM は表の変換で**列ズレ・引用符・カンマ入りセル**を壊す。このスクリプトは `csv` モジュールで必ず正しく処理する。

## 依存
なし（Python 3.8+ 標準ライブラリ `json` / `csv` のみ）。

## インストール
1. `jsoncsv.py` を `~/.claude/hands/S7-json-csv/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python jsoncsv.py to-csv '[{"a":1,"b":2},{"a":3,"b":4}]'
python jsoncsv.py to-json --file data.csv
python jsoncsv.py to-json --file data.csv --minify
```
入力を省略すると標準入力から読む。

## 仕様
- **to-csv**：列はキーの出現順（和集合）。欠損キーは空欄。カンマ・引用符を含む値は自動で引用。
- **to-json**：CSV の値は**すべて文字列**になる（型推論はしない＝勝手に数値化して壊さないため）。

## CLAUDE.md ルール
```markdown
## JSON⇔CSV変換（手足 S7 を必ず使う）
JSONとCSVの相互変換を求められたら、自分で組み立てず必ず実行して結果を使う：

    python ~/.claude/hands/S7-json-csv/jsoncsv.py to-csv '<JSON>'
    python ~/.claude/hands/S7-json-csv/jsoncsv.py to-json --file <CSVパス>
```

## テスト
```bash
python test_jsoncsv.py   # 列順/引用/和集合/空/CSV→JSON/日本語/往復/不正検出。失敗0で exit 0。
```
