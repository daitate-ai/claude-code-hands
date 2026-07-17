# S4 ハッシュ計算 — Claude Code の手足

文字列・ファイルの **MD5 / SHA-1 / SHA-256 / SHA-512** を決定論的に算出するスクリプト。

## なぜ手足にするのか
LLM はハッシュを"計算"できず、それらしい16進を**捏造**してしまう。このスクリプトなら必ず正確。

## 依存
なし（Python 3.8+ 標準ライブラリ `hashlib` のみ）。

## インストール
1. `hash.py` を `~/.claude/hands/S4-hash/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python hash.py "hello"              # 全アルゴリズム
python hash.py "hello" --algo sha256
python hash.py --file path.pdf      # ファイル
python hash.py "hello" --json       # 機械可読
```

## JSON 出力の契約
```json
{"text":"hello","hashes":{"md5":"...","sha1":"...","sha256":"...","sha512":"..."}}
```
`--file` 時は `"file":"path"`、`--algo` 時は `hashes` がその1つだけ。エラー時は `{"error":"..."}`。

## CLAUDE.md ルール
```markdown
## ハッシュ計算（手足 S4 を必ず使う）
MD5/SHA などのハッシュを求められたら、自分で書かず必ず実行して JSON の値を使う：

    python ~/.claude/hands/S4-hash/hash.py "<文字列>" --json
    python ~/.claude/hands/S4-hash/hash.py --file "<パス>" --json
```

## テスト
```bash
python test_hash.py   # 公知ベクトル(abc/空/日本語)で検証。失敗0で exit 0。
```
