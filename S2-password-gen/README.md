# S2 パスワード生成 — Claude Code の手足

**暗号学的乱数**で、指定した文字種を必ず含むパスワードを生成するスクリプト。

## なぜ手足にするのか
LLM が"考えて"作るパスワードは乱数が偏り、予測されうる。このスクリプトは OS の安全な乱数（`secrets`）を使い、各文字種を最低1つ含むことを保証する。

## 依存
なし（Python 3.8+ 標準ライブラリ `secrets` のみ）。

## インストール
1. `genpw.py` を `~/.claude/hands/S2-password-gen/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python genpw.py                       # 既定16文字
python genpw.py --length 24 --count 3
python genpw.py --no-symbols          # 記号を除く
python genpw.py --no-ambiguous        # 紛らわしい文字(0O1lI)を除く
python genpw.py --json
```
`--no-upper` / `--no-lower` / `--no-digits` で文字種を絞れる。

## JSON 出力の契約
```json
{"length":16,"count":3,"passwords":["...","...","..."]}
```
エラー時は `{"error":"..."}`。

## CLAUDE.md ルール
```markdown
## パスワード生成（手足 S2 を必ず使う）
パスワードを求められたら、自分で考えず必ず実行して生成された値を使う：

    python ~/.claude/hands/S2-password-gen/genpw.py --length <長さ> --json
```

## テスト
```bash
python test_genpw.py   # 長さ/文字種保証/除外/一意性/不正入力。失敗0で exit 0。
```
