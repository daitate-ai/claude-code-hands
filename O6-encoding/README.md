# O6 文字コード / BOM固定 — Claude Code の手足

ファイルの**エンコーディング・BOM・改行コード**を実バイトから判定し、指定形式へ変換するスクリプト。

## なぜ手足にするのか
文字化け・改行崩れ・BOM有無は**目視では分からず**、LLM は「たぶんUTF-8」と推測して壊す。実際のバイト列を見て判定するので必ず正確。

実例（当社で発生）：**PowerShell 5.1 はスクリプトに UTF-8 BOM を要求**する／Windows で CRLF が混入して差分が汚れる。

## 依存
なし（Python 3.8+ 標準ライブラリのみ。`chardet` 等は不要）。

## インストール
1. `encodingfix.py` を `~/.claude/hands/O6-encoding/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python encodingfix.py inspect file.txt
python encodingfix.py inspect file.txt --json
python encodingfix.py convert file.txt --to-encoding utf-8 --bom --newline crlf
python encodingfix.py convert file.txt --newline lf --out fixed.txt
```
`--newline` は `lf` / `crlf` / `cr`。`--bom` で UTF-8 BOM を付与（PowerShell 5.1 向け）。`--out` 省略時は上書き。

## JSON 出力の契約（inspect）
```json
{"bom":"utf-8-sig","has_bom":true,"encoding":"utf-8-sig","newline":"CRLF",
 "counts":{"crlf":2,"lf":0,"cr":0},"bytes":20,"path":"file.txt"}
```
`newline` は `LF` / `CRLF` / `CR` / `mixed` / `none`。判定不能なら `encoding` が `unknown`。

## CLAUDE.md ルール
```markdown
## 文字コード・改行の確認（手足 O6 を必ず使う）
既存ファイルを編集・生成する前に、推測せず必ず実行して形式を確認する：

    python ~/.claude/hands/O6-encoding/encodingfix.py inspect <パス> --json

- PowerShell 5.1 用スクリプトを書くときは --bom を付けて UTF-8 BOM にする。
- 既存ファイルの newline に合わせる（勝手に CRLF↔LF を変えない）。
```

## テスト
```bash
python test_encodingfix.py   # BOM/改行(LF/CRLF/混在/なし)/cp932判定/変換往復。失敗0で exit 0。
```
