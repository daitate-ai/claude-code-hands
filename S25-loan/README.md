# S25 ローン返済計算 — Claude Code の手足

元利均等返済の**毎月返済額・総支払・総利息**を決定論的に計算するスクリプト。

## なぜ手足にするのか
LLM は元利均等(PMT)の計算をまず正しくできない。このスクリプトなら必ず正確。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `loan.py` を `~/.claude/hands/S25-loan/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python loan.py --principal 3000000 --rate 1.5 --years 10
python loan.py --principal 1000000 --rate 12 --months 12 --json
```
`--years` か `--months` のどちらかで期間を指定。`--rate` は年利%。

## JSON 出力の契約
```json
{"monthly_payment":26937.45,"total_paid":3232493.99,"total_interest":232493.99,"months":120}
```

## CLAUDE.md ルール
```markdown
## ローン返済計算（手足 S25 を必ず使う）
毎月返済額・総利息を求められたら、自分で計算せず必ず実行して値を使う：

    python ~/.claude/hands/S25-loan/loan.py --principal <元金> --rate <年利%> --years <年> --json
```

## テスト
```bash
python test_loan.py   # PMT参照値/無利子/総額/不正期間。失敗0で exit 0。
```
