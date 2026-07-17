# S24 日数差分 — Claude Code の手足

2つの日付の**間隔**、または「**N日後 / N日前**」の日付を決定論的に計算するスクリプト。

## なぜ手足にするのか
LLM はうるう年や月跨ぎの日数計算を誤る。このスクリプトなら必ず正確（曜日も返す）。

## 依存
なし（Python 3.8+ 標準ライブラリ `datetime` のみ）。

## インストール
1. `datediff.py` を `~/.claude/hands/S24-date-diff/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python datediff.py 2026/07/17 2026/12/31   # 2日付の間隔
python datediff.py 2026/07/17 +100         # 100日後
python datediff.py 2026/07/17 -30          # 30日前
python datediff.py 2026/07/17 2026/12/31 --json
```
第2引数が `+N`/`-N` なら加算、日付なら間隔。`/` 区切りも可。

## JSON 出力の契約
```json
// 間隔
{"mode":"diff","from":"2026-07-17","to":"2026-12-31","days":167,"days_abs":167,"weeks":23,"remainder_days":6}
// 加算
{"mode":"add","from":"2026-07-17","offset_days":100,"result":"2026-10-25","weekday":"日"}
```
エラー時は `{"error":"..."}`。

## CLAUDE.md ルール
```markdown
## 日数計算（手足 S24 を必ず使う）
日付の間隔・N日後/前を求められたら、自分で計算せず必ず実行して値を使う：

    python ~/.claude/hands/S24-date-diff/datediff.py <基準日> <比較日 or +N/-N> --json
```

## テスト
```bash
python test_datediff.py   # 既知間隔/うるう年/符号/週余り/加算+曜日/往復。失敗0で exit 0。
```
