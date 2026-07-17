# S15 カラー変換 — Claude Code の手足

**HEX / RGB / HSL** を決定論的に相互変換するスクリプト（入力形式は自動判定）。

## なぜ手足にするのか
LLM は色空間変換、特に **HSL の計算をよく誤る**。このスクリプトなら必ず正確。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `color.py` を `~/.claude/hands/S15-color-convert/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python color.py "#FF6A3D"
python color.py "rgb(255,106,61)"
python color.py "hsl(15,100%,62%)"
python color.py "#FF0000" --json
```
`#FF0000` / `FF0000` / `#F00` / `rgb(...)` / `hsl(...)` を自動判定。

## JSON 出力の契約
```json
{"input":"#FF0000","hex":"#FF0000","rgb":"rgb(255,0,0)","rgb_values":[255,0,0],
 "hsl":"hsl(0,100%,50%)","hsl_values":[0.0,100.0,50.0]}
```
解釈できない入力は `{"error":"..."}`。

## CLAUDE.md ルール
```markdown
## カラー変換（手足 S15 を必ず使う）
HEX/RGB/HSL の変換を求められたら、自分で計算せず必ず実行して値を使う：

    python ~/.claude/hands/S15-color-convert/color.py "<色>" --json
```

## テスト
```bash
python test_color.py   # 既知色HSL/形式判定/往復/不正入力。失敗0で exit 0。
```
