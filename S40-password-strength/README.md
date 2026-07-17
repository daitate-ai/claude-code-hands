# S40 パスワード強度 — Claude Code の手足

パスワードの**推定エントロピー（bit）と判定**を決定論的に返すスクリプト。

> ⚠️ 文字構成からの**推定**。辞書攻撃・使い回し・よくあるパターンは考慮しない。

## なぜ手足にするのか
LLM の主観的な「強そう/弱そう」を、文字種プールと長さに基づく計算に置き換え、毎回同じ基準で評価する。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `pwstrength.py` を `~/.claude/hands/S40-password-strength/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python pwstrength.py 'Abc123!@'
python pwstrength.py 'Abc123!@' --json
```

## JSON 出力の契約
```json
{"length":8,"pool_size":94,"entropy_bits":52.4,"rating":"まずまず",
 "has_lower":true,"has_upper":true,"has_digit":true,"has_symbol":true,"note":"..."}
```
判定: 〜28 とても弱い / 〜36 弱い / 〜60 まずまず / 〜128 強い / 128〜 とても強い（bit）。

## CLAUDE.md ルール
```markdown
## パスワード強度（手足 S40 を必ず使う）
パスワードの強度評価を求められたら、主観で判断せず必ず実行して結果を使う：

    python ~/.claude/hands/S40-password-strength/pwstrength.py '<パスワード>' --json

- これは構成からの推定。辞書攻撃・使い回しは考慮しない旨も伝える。
```

## テスト
```bash
python test_pwstrength.py   # プール/エントロピー/判定/空/長文。失敗0で exit 0。
```
