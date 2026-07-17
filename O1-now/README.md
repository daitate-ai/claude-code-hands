# O1 正確時刻・日付手足（now）— Claude Code の手足

現在の日時を**決定論的**に返すスクリプト。Claude Code に「登録」して使う旗艦の手足。

## なぜ手足にするのか（＝手足が要る理由の"純度100%"デモ）

**LLM は時計を内蔵していない。** 日付は毎回ハーネスが外から注入して初めて分かる。
注入が無い場面（サブエージェント／スクリプト／長いセッション）では、Claude Code は
"それっぽい日付"を書いてしまう＝**日付のハルシネーション**。
さらに **PC=JST / サーバー=UTC の9時間差**で、日付が前後する（当社でも定期処理の日付が
1日ズレた実例あり）。

この手足を登録し「日時は必ずここから取得・推測禁止・絶対表記に変換」と決めれば、
**時刻は絶対にズレない**。"素でもできそうに見えて実は揺れる"の極致なので、導入デモの掴みに強い。

## 依存

なし。Python 3.8+ 標準ライブラリのみ（`pip install` 不要）。JST は固定オフセット(+09:00)で
扱うため、tzdata / zoneinfo も不要＝どの環境でも同じ結果。

## インストール（利用者の環境に登録する）

1. `now.py` を手足フォルダにコピー（例：`~/.claude/hands/O1-now/`）。
2. 下の「CLAUDE.md ルール」をプロジェクトの `CLAUDE.md` に追記する。

## 使い方（CLI）

```bash
python now.py          # JST と UTC と絶対表記の日付を表示
python now.py --json   # 機械可読JSON（Claude Code はこれを使う）
```

## JSON 出力の契約（Claude Code 向け）

| フィールド | 意味 |
|---|---|
| `utc` / `jst` | ISO 8601（オフセット付き）の現在時刻 |
| `date_jst` / `date_utc` | それぞれの日付（`YYYY-MM-DD` 絶対表記） |
| `weekday_jst` | JST の曜日（月〜日） |
| `time_jst` | JST の時刻（`HH:MM:SS`） |
| `unix` | Unix 時刻（整数秒） |
| `date_differs` | JST と UTC で日付が異なる場合 `true`（取り違え注意） |
| `note` | 使用上の注意 |

例：`python now.py --json`
```json
{"utc":"2026-07-17T03:25:21+00:00","jst":"2026-07-17T12:25:21+09:00","date_jst":"2026-07-17","date_utc":"2026-07-17","weekday_jst":"金","time_jst":"12:25:21","unix":1784258721,"date_differs":false}
```

## CLAUDE.md ルール（このブロックを利用者の CLAUDE.md に貼る）

```markdown
## 現在の日時（手足 O1 を必ず使う）
今日の日付・現在時刻・曜日が必要なときは、**自分で推測せず**必ず次を実行し、
その JSON の値だけを使う：

    python ~/.claude/hands/O1-now/now.py --json

- 日付は `date_jst` を絶対表記（YYYY-MM-DD）で書く。相対表記（今日・昨日）に頼らない。
- サーバー(UTC)処理では `date_utc`、日本時間基準では `date_jst` を使い、取り違えない。
- `date_differs` が true のときは、どちらの日付を意図しているか明示する。
```

## テスト（決定論の担保）

```bash
python test_now.py   # 通常 / 日付ズレ / 桁処理 / TZ正規化 を検証。失敗0で exit 0。
```
時刻自体は動くため、純関数 `snapshot()` に固定の UTC を与えて変換ロジックの正しさを担保している。
