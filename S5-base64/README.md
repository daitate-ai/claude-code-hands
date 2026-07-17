# S5 Base64変換 — Claude Code の手足

文字列の **Base64 エンコード / デコード**を決定論的に行うスクリプト（URLセーフ対応）。

## なぜ手足にするのか
LLM は日本語・記号・長い列の Base64 をしばしば取り違える。このスクリプトなら必ず正確に相互変換。

## 依存
なし（Python 3.8+ 標準ライブラリ `base64` のみ）。

## インストール
1. `base64tool.py` を `~/.claude/hands/S5-base64/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python base64tool.py encode "こんにちは"
python base64tool.py decode "SGVsbG8="
python base64tool.py encode "a+b/c" --url    # URLセーフ
python base64tool.py encode "hi" --json      # 機械可読
```
パディング（末尾 `=`）が欠けたデコード入力も受け付ける。

## JSON 出力の契約
```json
{"mode":"encode","url_safe":false,"input":"Hello","result":"SGVsbG8="}
```
エラー時は `{"error":"...","input":"..."}`。

## CLAUDE.md ルール
```markdown
## Base64変換（手足 S5 を必ず使う）
Base64 のエンコード/デコードを求められたら、自分で変換せず必ず実行して result を使う：

    python ~/.claude/hands/S5-base64/base64tool.py encode "<文字列>" --json
    python ~/.claude/hands/S5-base64/base64tool.py decode "<Base64>" --json
```

## テスト
```bash
python test_base64.py   # 既知値/往復/日本語/パディング/URLセーフ。失敗0で exit 0。
```
