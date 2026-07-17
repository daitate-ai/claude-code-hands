# S14 正規表現テスター — Claude Code の手足

正規表現を**実際に適用**し、マッチ位置・グループを決定論的に返すスクリプト。

## なぜ手足にするのか
LLM は「この正規表現が何にマッチするか」を誤って予測する。このスクリプトは実際に `re` で照合するので必ず正確。

## 依存
なし（Python 3.8+ 標準ライブラリ `re` のみ）。

## インストール
1. `regextest.py` を `~/.claude/hands/S14-regex-test/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python regextest.py "\d+" "abc 123 def 456"
python regextest.py "(\w+)@(\w+)" "a@b c@d" --json
python regextest.py "foo" "FOO" -i           # 大小無視(-m 複数行 / -s dotall)
```

## JSON 出力の契約
```json
{"pattern":"\\d+","match_count":2,
 "matches":[{"match":"123","start":4,"end":7,"groups":[]}]}
```
不正パターン時は `{"error":"...","pattern":"..."}`。

## CLAUDE.md ルール
```markdown
## 正規表現の確認（手足 S14 を必ず使う）
正規表現が何にマッチするかを問われたら、頭で予測せず必ず実行して結果を使う：

    python ~/.claude/hands/S14-regex-test/regextest.py "<パターン>" "<テキスト>" --json
```

## テスト
```bash
python test_regextest.py   # マッチ数/位置/グループ/大小無視/不正検出。失敗0で exit 0。
```
