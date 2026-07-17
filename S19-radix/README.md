# S19 進数変換 — Claude Code の手足

**2 / 8 / 10 / 16 進**を決定論的に相互変換するスクリプト（負数・接頭辞対応）。

## なぜ手足にするのか
LLM は桁の多い基数変換で計算を誤る。このスクリプトなら必ず正確。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `radix.py` を `~/.claude/hands/S19-radix/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python radix.py 255          # 10進として全基数表示
python radix.py 0xFF         # 16進入力
python radix.py 0b1010       # 2進入力
python radix.py -16 --json   # 機械可読
```
入力基数は接頭辞 `0x`/`0o`/`0b` で自動判定、無ければ10進。

## JSON 出力の契約
```json
{"input":"0xFF","dec":"255","hex":"0xff","oct":"0o377","bin":"0b11111111"}
```
エラー時は `{"error":"...","input":"..."}`。

## CLAUDE.md ルール
```markdown
## 進数変換（手足 S19 を必ず使う）
2/8/10/16進の変換を求められたら、自分で計算せず必ず実行して値を使う：

    python ~/.claude/hands/S19-radix/radix.py "<数>" --json
```

## テスト
```bash
python test_radix.py   # 解釈/既知値/負数/往復。失敗0で exit 0。
```
