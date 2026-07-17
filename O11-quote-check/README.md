# O11 出典接地 — Claude Code の手足

引用しようとしている文字列が**出典に実在するか**を機械的に照合するスクリプト。

## なぜ手足にするのか
LLM は「出典にあった風」の引用を作る（**引用のねつ造**）。少し言い回しが違うだけでも引用としては誤り。このスクリプトは出典ファイルに"その通りの文字列"があるかを照合し、無ければ**最も近い箇所と一致度**を示すので、どう違うかが分かる。

## 依存
なし（Python 3.8+ 標準ライブラリ `difflib` のみ）。

## インストール
1. `quotecheck.py` を `~/.claude/hands/O11-quote-check/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python quotecheck.py "引用したい一文" --file source.md
python quotecheck.py "引用" --file source.md --normalize-space   # 空白差を無視
python quotecheck.py "引用" --file source.md --json
```

**exit code**: 出典に見つからなければ **1**（＝その引用を使わない合図）。

## JSON 出力の契約
```json
// 一致
{"quote":"...","found":true,"similarity":1.0,"line":28,"reason":"..."}
// 不一致(ねつ造の可能性)
{"quote":"...","found":false,"similarity":0.82,"closest":"実際の記述","closest_line":28,"reason":"..."}
```

## CLAUDE.md ルール
```markdown
## 引用の裏取り（手足 O11 を必ず使う）
資料から引用する時は、記憶で書かず必ず実行して実在を確認する：

    python ~/.claude/hands/O11-quote-check/quotecheck.py "<引用文>" --file <出典> --json

- found が false なら**その引用を使わない**。closest を見て正しい表現に直すか、引用をやめる。
- 引用には出典ファイル名と line を添える。
```

## テスト
```bash
python test_quotecheck.py   # 一致/行番号/ねつ造検知/近似箇所/空白正規化。失敗0で exit 0。
```
