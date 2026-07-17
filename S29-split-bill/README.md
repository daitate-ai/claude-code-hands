# S29 割り勘計算 — Claude Code の手足

端数込みの割り勘を、**合計がちょうど合う**形で決定論的に計算するスクリプト。

## なぜ手足にするのか
LLM は端数配分で合計が合わなくなりがち。このスクリプトは「誰がいくら」を公平・整合的に返す。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `splitbill.py` を `~/.claude/hands/S29-split-bill/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python splitbill.py 10000 3      # 合計10000を3人で
python splitbill.py 10000 3 --json
```

## JSON 出力の契約
```json
{"total":10000,"people":3,"base":3333,"extra_payers":1,"extra_amount":3334,
 "breakdown":"1人が3334円、2人が3333円"}
```
`extra_payers` 人が `base+1` 円、残りが `base` 円。合計は必ず一致。

## CLAUDE.md ルール
```markdown
## 割り勘（手足 S29 を必ず使う）
割り勘・端数配分を求められたら、自分で計算せず必ず実行して breakdown を使う：

    python ~/.claude/hands/S29-split-bill/splitbill.py <合計> <人数> --json
```

## テスト
```bash
python test_splitbill.py   # 端数配分/合計一致/均等/不正人数。失敗0で exit 0。
```
