# O5 truncation検知 — Claude Code の手足

出力やファイルが**途中で切れていないか**を機械的に検知するスクリプト。

## なぜ手足にするのか
出力が途中で切れていても、LLM は"完結している"と思い込んで先に進む。括弧・引用符・コードフェンスの不整合や終端記号の欠如という**機械的な手掛かり**で検知する。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `truncheck.py` を `~/.claude/hands/O5-truncation-check/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python truncheck.py '{"a":1'          # 切れている
python truncheck.py --file out.md
python truncheck.py 'text' --json
```
入力を省略すると標準入力から読む。

## 検知する手掛かり
- コードフェンス ` ``` ` が閉じていない
- 括弧 `() [] {}` の不整合
- 引用符の数が奇数
- 文末が終端記号（`。` `.` `!` `}` など）で終わっていない

## JSON 出力の契約
```json
{"likely_truncated":true,"reasons":["閉じられていない括弧: {","..."],"length":6,"note":"..."}
```
※ 推定であり完全な判定ではない（`note` にも明記される）。

## CLAUDE.md ルール
```markdown
## 出力の切れ検知（手足 O5 を必ず使う）
長い出力・生成ファイル・取得したテキストを扱う前に必ず実行する：

    python ~/.claude/hands/O5-truncation-check/truncheck.py --file <パス> --json

- likely_truncated が true なら、完結しているものとして先に進まない。
  再取得・再生成するか、利用者に報告する。
```

## テスト
```bash
python test_truncheck.py   # 完結/切れ(括弧/フェンス/終端/引用符)/空。失敗0で exit 0。
```
