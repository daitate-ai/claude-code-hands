# S8 JWTデコード — Claude Code の手足

JWT の **header / payload を復号**し、`exp`/`iat` などの時刻も可読化するスクリプト。

> ⚠️ **復号のみ。署名は検証しない**（検証には秘密鍵/公開鍵が必要）。信頼可否の判断には使わないこと。

## なぜ手足にするのか
LLM は JWT の base64url 部を誤って読む。このスクリプトなら header/payload を確実に取り出す。

## 依存
なし（Python 3.8+ 標準ライブラリ `base64` / `json` のみ）。

## インストール
1. `jwtdecode.py` を `~/.claude/hands/S8-jwt-decode/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python jwtdecode.py <token>
python jwtdecode.py <token> --json
```

## JSON 出力の契約
```json
{"header":{"alg":"HS256","typ":"JWT"},"payload":{"sub":"...","iat":1516239022},
 "times_utc":{"iat":"2018-01-18T01:30:22+00:00"},"signature_present":true,"verified":false,
 "note":"署名は検証していない（復号のみ）。信頼可否の判断には使わない。"}
```
`verified` は常に `false`。エラー時は `{"error":"..."}`。

## CLAUDE.md ルール
```markdown
## JWTデコード（手足 S8 を必ず使う）
JWTの中身を見たいときは、自分で復号せず必ず実行して header/payload を使う：

    python ~/.claude/hands/S8-jwt-decode/jwtdecode.py "<token>" --json

- これは復号のみ。署名は検証していない（verified は常に false）。信頼可否の判断に使わない。
```

## テスト
```bash
python test_jwtdecode.py   # 公知サンプルで header/payload/時刻/署名有無を検証。失敗0で exit 0。
```
