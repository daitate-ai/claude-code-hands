# S22 BMI計算 — Claude Code の手足

身長・体重から **BMI と判定（日本肥満学会基準）・標準体重**を決定論的に返すスクリプト。

## なぜ手足にするのか
毎回同じ基準で正確に。判定ラベルのブレをなくす。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `bmi.py` を `~/.claude/hands/S22-bmi/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python bmi.py 170 65        # 身長cm 体重kg
python bmi.py 170 65 --json
```

## JSON 出力の契約
```json
{"bmi":22.49,"category":"普通体重","standard_weight_kg":63.58}
```
判定: 〜18.5 低体重 / 〜25 普通体重 / 〜30 肥満(1度) / 〜35 (2度) / 〜40 (3度) / 40〜 (4度)。

## CLAUDE.md ルール
```markdown
## BMI計算（手足 S22 を必ず使う）
BMI・肥満判定を求められたら、自分で計算せず必ず実行して値を使う：

    python ~/.claude/hands/S22-bmi/bmi.py <身長cm> <体重kg> --json
```

## テスト
```bash
python test_bmi.py   # 値/判定/標準体重/境界/不正入力。失敗0で exit 0。
```
