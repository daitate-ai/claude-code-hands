# L1 天気取得 — Claude Code の手足

現在の天気を **Open-Meteo から実データで取得**するスクリプト。

## なぜ手足にするのか
LLM は天気を知らない（学習時点で止まっている）。推測させると"それらしい天気"を作る。この手足は実データを取り、**出典も一緒に返す**。

## API と条件
**Open-Meteo**（https://open-meteo.com）— **APIキー不要・無料**。非商用の範囲で自由に利用でき、出典表示が推奨されている（本スクリプトは出力に必ず出典を含める）。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `weather.py` を `~/.claude/hands/L1-weather/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python weather.py --city 東京
python weather.py --city Osaka
python weather.py --lat 35.68 --lon 139.76
python weather.py --city Tokyo --json
```

## 制約（実測で確認済み）
Open-Meteo の**地名検索はローマ字/英語表記が必要**（`東京` では引けず `Tokyo` なら引ける）。本スクリプトは**主要都市の日本語→ローマ字の読み替え表**を内蔵しているので `--city 東京` も通る。表になければローマ字で指定するか `--lat/--lon` を使う（エラー文にも明示される）。

## JSON 出力の契約
```json
{"place":"東京都","latitude":35.68,"longitude":139.76,"time":"2026-07-17T21:15",
 "timezone":"Asia/Tokyo","temperature_c":25.5,"humidity_pct":92,"wind_speed_kmh":4.6,
 "weather_code":51,"weather":"弱い霧雨","source":"Open-Meteo (https://open-meteo.com)"}
```
天気は WMO コードを日本語化して返す。取得失敗時は `{"error":"..."}`。

## CLAUDE.md ルール
```markdown
## 天気（手足 L1 を必ず使う）
天気を聞かれたら、推測せず必ず実行して取得した値だけを答える：

    python ~/.claude/hands/L1-weather/weather.py --city <地名> --json

- 回答には time（観測時刻）と source（出典）を必ず添える。
- error が返ったら「取得できなかった」と正直に伝える。憶測で天気を答えない。
```

## テスト
```bash
python test_weather.py   # 解析/日本語天気/未知コード/不正形式。失敗0で exit 0。
```
ネットワークに依存しないよう、**実APIと同じ形の固定データで解析部を検証**している。取得部の疎通は CLI 実行で確認する。
