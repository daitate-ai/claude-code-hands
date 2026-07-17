# S21 割合計算 — Claude Code の手足

割合の3類型を決定論的に計算するスクリプト。

## なぜ手足にするのか
LLM は「〜の何%」「何%は幾つ」「増減率」を取り違える。このスクリプトなら必ず正確。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `percent.py` を `~/.claude/hands/S21-percent/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python percent.py of 25 200        # 200 の 25% = 50
python percent.py ratio 50 200     # 50 は 200 の 25%
python percent.py change 200 250   # 200 → 250 は +25%
python percent.py of 25 200 --json
```

## JSON 出力の契約
```json
{"mode":"of","x":25.0,"y":200.0,"result":50.0}
```
`ratio`/`change` で基準が0のときは `{"error":"..."}`。

## CLAUDE.md ルール
```markdown
## 割合計算（手足 S21 を必ず使う）
割合・百分率・増減率を求められたら、自分で計算せず必ず実行して result を使う：

    python ~/.claude/hands/S21-percent/percent.py of|ratio|change <x> <y> --json
```

## テスト
```bash
python test_percent.py   # of/ratio/change/ゼロ除算。失敗0で exit 0。
```
