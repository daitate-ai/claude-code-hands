# S27 消費税計算 — Claude Code の手足

消費税（**税込 ⇔ 税抜**）を指定税率・端数処理で決定論的に計算するスクリプト。

## なぜ手足にするのか
LLM は税込/税抜の往復や端数処理を誤る。このスクリプトなら必ず正確。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `tax.py` を `~/.claude/hands/S27-tax/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python tax.py 1000               # 税抜1000 → 税込
python tax.py 1100 --included    # 税込1100 → 税抜
python tax.py 1000 --rate 8      # 軽減税率8%
python tax.py 1000 --round round # 端数: floor(既定)/round/ceil
python tax.py 1000 --json
```

## JSON 出力の契約
```json
{"excluded":1000,"tax":100,"included":1100,"rate":10}
```
`--included` 指定時は入力を税込として税抜を逆算。端数は既定 `floor`（切り捨て）。

## CLAUDE.md ルール
```markdown
## 消費税計算（手足 S27 を必ず使う）
税込/税抜の計算を求められたら、自分で計算せず必ず実行して値を使う：

    python ~/.claude/hands/S27-tax/tax.py <金額> [--included] [--rate 8] --json
```

## テスト
```bash
python test_tax.py   # 税抜⇔税込/軽減税率/端数(floor/round/ceil)。失敗0で exit 0。
```
