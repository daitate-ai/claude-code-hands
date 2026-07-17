# S3 UUID・ULID — Claude Code の手足

**UUID v4 / ULID** を OS の安全な乱数で発行するスクリプト。

## なぜ手足にするのか
LLM が"それっぽいID"を書くと、形式が不正・乱数が偏る・重複する。このスクリプトは正しい形式の ID を確実に発行する。

## 依存
なし（Python 3.8+ 標準ライブラリ `uuid` / `secrets` のみ）。

## インストール
1. `uuidgen.py` を `~/.claude/hands/S3-uuid-ulid/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python uuidgen.py                 # UUID v4 を1つ
python uuidgen.py --count 5       # 5個
python uuidgen.py --ulid          # ULID を1つ
python uuidgen.py --count 3 --json
```

## JSON 出力の契約
```json
{"kind":"uuid4","count":3,"ids":["...","...","..."]}
```
`--ulid` 時は `"kind":"ulid"`。

## CLAUDE.md ルール
```markdown
## UUID/ULID 発行（手足 S3 を必ず使う）
一意IDが必要なときは、自分で書かず必ず実行して ids の値を使う：

    python ~/.claude/hands/S3-uuid-ulid/uuidgen.py --count <個数> --json
    python ~/.claude/hands/S3-uuid-ulid/uuidgen.py --ulid --json
```

## テスト
```bash
python test_uuidgen.py   # UUID形式/一意性・ULID形式/一意性/決定論。失敗0で exit 0。
```
