# L4 地震情報取得 — Claude Code の手足

**USGS（米国地質調査所）**の公式フィードから最新の地震を取得するスクリプト。

## なぜ手足にするのか
LLM は最近の地震を知らない。推測させると"それらしい地震"を作る。この手足は公的機関の実データを取り、出典を返す。

## API と条件
**USGS Earthquake Hazards Program**（https://earthquake.usgs.gov）— **APIキー不要**・米国政府の公開フィード。

> ⚠️ **USGS観測のマグニチュード**であり、**日本の震度階級ではない**。日本国内の詳細は気象庁が一次情報。出力の `note` にも明記される。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `quake.py` を `~/.claude/hands/L4-earthquake/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python quake.py                          # 直近1日・M4.5以上
python quake.py --feed 2.5_day --limit 5
python quake.py --min-mag 6 --json
```
`--feed`: `significant_day` / `4.5_day` / `2.5_day` / `significant_week` / `4.5_week` / `all_hour`

## JSON 出力の契約
```json
{"count":1,"total_matched":1,
 "quakes":[{"magnitude":5.2,"place":"42 km NE of Shwebo, Burma (Myanmar)",
            "time_utc":"2026-07-17T01:26:06+00:00","time_jst":"2026-07-17T10:26:06+09:00",
            "longitude":95.9,"latitude":22.4,"depth_km":10,"url":"https://..."}],
 "source":"USGS ...","note":"USGS観測のマグニチュード。日本の震度階級ではない。"}
```
時刻は **UTC と JST の両方**を返す（取り違え防止）。新しい順。

## CLAUDE.md ルール
```markdown
## 地震情報（手足 L4 を必ず使う）
最近の地震を聞かれたら、推測せず必ず実行して取得した値だけを答える：

    python ~/.claude/hands/L4-earthquake/quake.py --min-mag <下限> --json

- 回答には time_jst と source、url を添える。
- 「マグニチュードであって震度ではない」ことを明示する。日本国内の詳細は気象庁が一次情報。
```

## テスト
```bash
python test_quake.py   # 解析/新しい順/UTC・JST変換/絞り込み/不正形式。失敗0で exit 0。
```
ネットワーク非依存にするため、**実APIと同じ形の固定GeoJSONで解析部を検証**している。
