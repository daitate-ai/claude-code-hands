# S26 複利積立計算 — Claude Code の手足

元本＋毎月積立の**将来価値（月複利）**を決定論的に計算するスクリプト。

## なぜ手足にするのか
LLM は複利＋積立の将来価値を正しく計算できない。このスクリプトなら必ず正確。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `compound.py` を `~/.claude/hands/S26-compound/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python compound.py --principal 1000000 --monthly 30000 --rate 5 --years 20
python compound.py --monthly 100 --rate 12 --months 2 --json
```
`--rate` は年利%。`--years` か `--months` で期間指定。`--principal`/`--monthly` は省略可(既定0)。

## JSON 出力の契約
```json
{"future_value":...,"total_contributed":...,"total_interest":...,"months":240}
```

## CLAUDE.md ルール
```markdown
## 複利積立計算（手足 S26 を必ず使う）
積立の将来価値・運用益を求められたら、自分で計算せず必ず実行して値を使う：

    python ~/.claude/hands/S26-compound/compound.py --principal <元本> --monthly <毎月> --rate <年利%> --years <年> --json
```

## テスト
```bash
python test_compound.py   # 参照値/無利子/元本のみ複利。失敗0で exit 0。
```
