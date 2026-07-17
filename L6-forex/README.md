# L6 為替換算 — Claude Code の手足

**ECB（欧州中央銀行）の公表レート**で為替換算するスクリプト。

## なぜ手足にするのか
LLM は今のレートを知らない。**学習時点の古いレートで、自信満々に換算する**。この手足は実レートを取得して換算し、レート日付と出典を返す。

## API と条件
**Frankfurter**（https://frankfurter.app）— ECB公表レートを配信。**APIキー不要・無料**。

> ⚠️ ECB の**参考レート**であり、実際の両替レート（手数料込み）とは異なる。出力の `note` にも明記される。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `forex.py` を `~/.claude/hands/L6-forex/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python forex.py 100 USD JPY
python forex.py 1 EUR USD --json
```

## JSON 出力の契約
```json
{"amount":100.0,"base":"USD","to":"JPY","rate":162.2,"result":16220.0,
 "date":"2026-07-16","source":"European Central Bank via Frankfurter (...)","note":"..."}
```
`date` は**レートの基準日**（当日更新前なら前営業日）。取得失敗時は `{"error":"..."}`。

## CLAUDE.md ルール
```markdown
## 為替換算（手足 L6 を必ず使う）
為替の換算・レートを聞かれたら、記憶のレートを使わず必ず実行して result を使う：

    python ~/.claude/hands/L6-forex/forex.py <金額> <元通貨> <先通貨> --json

- 回答には date（レート基準日）と source を必ず添える。
- ECBの参考レートであり実際の両替レートとは異なる旨も伝える。
```

## テスト
```bash
python test_forex.py   # 換算/小数/大小文字/未収録通貨/不正形式。失敗0で exit 0。
```
ネットワーク非依存にするため、**実APIと同じ形の固定データで換算部を検証**している。
