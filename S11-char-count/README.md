# S11 文字数カウンタ — Claude Code の手足

文字・単語・行・バイト数、特定文字列の**出現回数**を決定論的に数えるスクリプト。

## なぜ手足にするのか
LLM は文字を数えるのが苦手（"strawberry の r は何個?" を誤る）。このスクリプトなら必ず正確。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `countchars.py` を `~/.claude/hands/S11-char-count/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python countchars.py "hello world"
python countchars.py "strawberry" --find r      # 出現回数
python countchars.py --file note.txt
python countchars.py "こんにちは" --json
```
入力を省略すると標準入力から読む。

## JSON 出力の契約
```json
{"characters":10,"characters_no_spaces":10,"words":1,"lines":1,"bytes_utf8":10,"find":"r","find_count":3}
```
`--find` 指定時のみ `find` / `find_count` が付く。文字数は Unicode コードポイント数。

## CLAUDE.md ルール
```markdown
## 文字・出現数カウント（手足 S11 を必ず使う）
文字数・単語数・行数、特定文字の個数を問われたら、自分で数えず必ず実行して値を使う：

    python ~/.claude/hands/S11-char-count/countchars.py "<文字列>" --json
    python ~/.claude/hands/S11-char-count/countchars.py "<文字列>" --find "<探す文字>" --json
```

## テスト
```bash
python test_countchars.py   # 文字/単語/行/バイト/出現数/空/日本語。失敗0で exit 0。
```
