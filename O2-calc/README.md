# O2 算術・カウント手足 — Claude Code の手足

算術式を**実際に計算**して返すスクリプト（暗算させない）。

## なぜ手足にするのか
LLM は暗算を間違える。特に桁の多い掛け算・累乗で**静かに誤る**（それらしい数字を書く）。整数は多倍長で厳密に計算するので、`2**100` のような桁でも正確。

## 安全性
`eval` は使わない。`ast` で構文木を解析し、**数値と算術演算子のみ**を許可する。関数呼び出し・変数・属性アクセス・文字列は全て拒否（`__import__('os')` などは実行されない）。巨大累乗は上限で停止。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `calc.py` を `~/.claude/hands/O2-calc/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python calc.py "1234*5678"
python calc.py "(1+2)**10"
python calc.py "7/2" --json
```
使える演算子: `+ - * / // % **` と括弧。

## JSON 出力の契約
```json
{"expression":"1234*5678","result":7006652,"type":"int"}
```
エラー時は `{"expression":"...","error":"..."}`。

## CLAUDE.md ルール
```markdown
## 算術計算（手足 O2 を必ず使う）
数値計算を求められたら、暗算せず必ず実行して result を使う：

    python ~/.claude/hands/O2-calc/calc.py "<式>" --json
```

## テスト
```bash
python test_calc.py   # 算術/多倍長/安全性(コード実行拒否)/上限/例外。失敗0で exit 0。
```
