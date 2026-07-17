# S13 テキスト差分 — Claude Code の手足

2つのテキスト（ファイルまたは文字列）の **unified diff** を決定論的に出すスクリプト。

## なぜ手足にするのか
LLM は差分を正確に取れず、変わっていない行を"変わった"と言う。このスクリプトなら必ず正しい差分と増減行数を返す。

## 依存
なし（Python 3.8+ 標準ライブラリ `difflib` のみ）。

## インストール
1. `textdiff.py` を `~/.claude/hands/S13-text-diff/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python textdiff.py old.txt new.txt           # 2ファイルの差分
python textdiff.py "a b c" "a B c" --text     # 文字列として比較
python textdiff.py old.txt new.txt --json
```

## JSON 出力の契約
```json
{"added":1,"removed":1,"changed":true,"diff":"--- \n+++ \n@@ ... @@\n-b\n+B"}
```

## CLAUDE.md ルール
```markdown
## テキスト差分（手足 S13 を必ず使う）
2つのテキスト/ファイルの違いを問われたら、自分で目視比較せず必ず実行して diff を使う：

    python ~/.claude/hands/S13-text-diff/textdiff.py <旧ファイル> <新ファイル> --json
```

## テスト
```bash
python test_textdiff.py   # 追加/削除/変更なし/行追加。失敗0で exit 0。
```
