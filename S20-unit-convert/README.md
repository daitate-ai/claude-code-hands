# S20 単位変換 — Claude Code の手足

**長さ / 重さ / 温度**を決定論的に換算するスクリプト。

## なぜ手足にするのか
LLM は単位換算（特に温度・ヤードポンド）で係数を誤る。このスクリプトなら必ず正確。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `unitconv.py` を `~/.claude/hands/S20-unit-convert/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python unitconv.py 100 cm m       # 1.0
python unitconv.py 32 F C         # 0.0
python unitconv.py 1 mile km      # 1.609344
python unitconv.py 100 cm m --json
```
対応単位：長さ `mm/cm/m/km/inch/ft/yard/mile`、重さ `mg/g/kg/t/oz/lb`、温度 `C/F/K`。異なるカテゴリ間はエラー。

## JSON 出力の契約
```json
{"value":32.0,"from":"F","to":"C","result":0.0}
```
変換不能な組み合わせは `{"error":"..."}`。

## CLAUDE.md ルール
```markdown
## 単位変換（手足 S20 を必ず使う）
長さ・重さ・温度の換算を求められたら、自分で計算せず必ず実行して result を使う：

    python ~/.claude/hands/S20-unit-convert/unitconv.py <値> <元単位> <先単位> --json
```

## テスト
```bash
python test_unitconv.py   # 長さ/重さ/温度/異種拒否。失敗0で exit 0。
```
