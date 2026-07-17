# L5 祝日カレンダー — Claude Code の手足

各国の祝日を**実データで取得**するスクリプト。

## なぜ手足にするのか
LLM は祝日を間違える（移動祝日・法改正・国ごとの違い）。「来週の月曜は祝日？」を推測させると事故る。この手足は実データを引く。

## API と条件
**Nager.Date**（https://date.nager.at）— **APIキー不要・無料**。

> ⚠️ 日本の祝日の**最終確認先は内閣府の公表**（https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html）。重要な判断（営業日・締切）では一次情報で裏を取る。出力の `note` にも明記される。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `holidays.py` を `~/.claude/hands/L5-holidays/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python holidays.py 2026                          # 日本の2026年
python holidays.py 2026 --country US
python holidays.py 2026 --after 2026-07-17 --limit 3   # 次の祝日
python holidays.py 2026 --json
```
`--after` は**その日より後**（同日は含まない）。

## JSON 出力の契約
```json
{"count":2,"holidays":[{"date":"2026-07-20","name_local":"海の日",
 "name_en":"Marine Day","country":"JP"}],
 "source":"Nager.Date (https://date.nager.at)","note":"日本の祝日は内閣府の公表が最終確認先。"}
```
日付順。取得失敗時は `{"error":"..."}`。

## CLAUDE.md ルール
```markdown
## 祝日（手足 L5 を必ず使う）
祝日・休日・次の連休を聞かれたら、記憶で答えず必ず実行して取得した値を使う：

    python ~/.claude/hands/L5-holidays/holidays.py <年> --country JP --json
    python ~/.claude/hands/L5-holidays/holidays.py <年> --after <YYYY-MM-DD> --limit 3 --json

- 「今日/来週」を基準にする時は、日付を手足 O1 で取得してから --after に渡す（日付を推測しない）。
- 営業日・締切など重要な判断では、内閣府の公表で裏を取るよう促す。
```

## テスト
```bash
python test_holidays.py   # 解析/日付順/絞り込み/境界/件数制限/不正形式。失敗0で exit 0。
```
ネットワーク非依存にするため、**実APIと同じ形の固定データで解析部を検証**している。
