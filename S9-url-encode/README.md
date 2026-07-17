# S9 URLエンコード — Claude Code の手足

文字列の **URLパーセントエンコード / デコード**を決定論的に行うスクリプト（フォーム形式 `+` 対応）。

## なぜ手足にするのか
LLM は `%20` などのパーセントエンコードを取りこぼす/取り違える。このスクリプトなら必ず正確。

## 依存
なし（Python 3.8+ 標準ライブラリ `urllib` のみ）。

## インストール
1. `urltool.py` を `~/.claude/hands/S9-url-encode/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python urltool.py encode "a b&c=d"      # a%20b%26c%3Dd
python urltool.py decode "a%20b"        # a b
python urltool.py encode "a b" --plus   # a+b (フォーム形式)
python urltool.py encode "x" --json
```

## JSON 出力の契約
```json
{"mode":"encode","plus":false,"input":"a b","result":"a%20b"}
```
エラー時は `{"error":"...","input":"..."}`。

## CLAUDE.md ルール
```markdown
## URLエンコード（手足 S9 を必ず使う）
URLエンコード/デコードを求められたら、自分で変換せず必ず実行して result を使う：

    python ~/.claude/hands/S9-url-encode/urltool.py encode "<文字列>" --json
    python ~/.claude/hands/S9-url-encode/urltool.py decode "<文字列>" --json
```

## テスト
```bash
python test_urltool.py   # 空白/予約文字/スラッシュ/plus/デコード/日本語。失敗0で exit 0。
```
