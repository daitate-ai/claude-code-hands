# S39 Cron式の読み解き — Claude Code の手足

cron 式（分 時 日 月 曜日）を**検証して日本語で説明**するスクリプト。

## なぜ手足にするのか
LLM は cron 式の読み解きを誤り、「毎日9時」のつもりが違う時刻になる事故を起こす。このスクリプトは実際にフィールドを展開して検証するので必ず正確。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `cron.py` を `~/.claude/hands/S39-cron/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python cron.py "0 9 * * 1-5"      # → 毎週月・火・水・木・金 9:00
python cron.py "*/15 * * * *"     # → 毎日 15分ごと
python cron.py "0 9 * * 1-5" --json
```
`*` / `*/N` / `a-b` / `a,b,c` に対応。曜日は 0=日〜6=土（7も日）。

## JSON 出力の契約
```json
{"expression":"0 9 * * 1-5","valid":true,"description":"毎週月・火・水・木・金 9:00",
 "fields":{"minute":[0],"hour":[9],"day_of_month":[1,...],"month":[1,...],"day_of_week":[1,2,3,4,5]}}
```
不正時は `{"expression":"...","valid":false,"error":"..."}`。

## CLAUDE.md ルール
```markdown
## cron式の確認（手足 S39 を必ず使う）
cron式が「いつ動くか」を問われたら、頭で読まず必ず実行して description / fields を使う：

    python ~/.claude/hands/S39-cron/cron.py "<cron式>" --json
```

## テスト
```bash
python test_cron.py   # 展開/平日/ステップ/毎月/毎時/日曜表現/不正検出。失敗0で exit 0。
```
