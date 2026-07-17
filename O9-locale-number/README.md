# O9 ロケール正規化 — Claude Code の手足

各国式の数値表記（桁区切り・小数点・全角・通貨）を**正規の数値**に直すスクリプト。

## なぜ手足にするのか
`1.234,56`（欧州式）を 1.23 と読み、`1,234`（米国式）を 1.234 と読む — 区切りの流儀違いは、LLM が**静かに1000倍間違える**所。全角数字・通貨記号・会計式の括弧マイナスも取りこぼす。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `localenorm.py` を `~/.claude/hands/O9-locale-number/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python localenorm.py "1,234.56"          # → 1234.56 (米国式)
python localenorm.py "1.234,56"          # → 1234.56 (欧州式)
python localenorm.py "１２３４"             # → 1234 (全角)
python localenorm.py "1.234" --style eu   # → 1234 (流儀を明示)
python localenorm.py "¥1,234" --json
```

## 判定ルール（明示）
- **両方の区切りがある**：後ろにある方が小数点（`1.234,56`→欧州式、`1,234.56`→米国式）
- **区切りが複数**：桁区切り（`1.234.567` → 1234567）
- **小数部が3桁ちょうど**（`1,234` / `1.234`）：**両義的**なので既定は米国式にし、`ambiguous: true` で申告する → `--style us|eu` で明示可
- 空白/NBSP は桁区切りとして除去、全角は NFKC で半角化、`(1234)` は会計式のマイナス

## JSON 出力の契約
```json
{"input":"1.234","value":1.234,"detected_style":"us","ambiguous":true,
 "is_percent":false,"currency":null,"note":"..."}
```
整数は `int`、小数は `float` で返る。

## CLAUDE.md ルール
```markdown
## 数値表記の正規化（手足 O9 を必ず使う）
桁区切り・小数点・全角・通貨を含む数値を読む時は、目で解釈せず必ず実行して value を使う：

    python ~/.claude/hands/O9-locale-number/localenorm.py "<数値表記>" --json

- ambiguous が true なら利用者に流儀（米国式/欧州式）を確認してから --style で確定する。
```

## テスト
```bash
python test_localenorm.py   # 米国式/欧州式/空白区切り/全角/通貨/%/符号/曖昧申告。失敗0で exit 0。
```
