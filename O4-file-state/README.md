# O4 ファイル状態ドリフト防止 — Claude Code の手足

読んだ時点の**指紋(sha256)**を記録し、書く前に「変わっていないか」を検証するスクリプト。

## なぜ手足にするのか
読んだ後に他所（別端末・別セッション・人間）で変更されたファイルへそのまま上書きすると、**その変更が消える**（クロバー事故）。目視では気づけないので、機械的に止める。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `filestate.py` を `~/.claude/hands/O4-file-state/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python filestate.py snapshot notes.md              # 読む時: 指紋を取る
python filestate.py verify notes.md --sha256 <値>   # 書く前: 変わっていないか
python filestate.py snapshot notes.md --json
```

**exit code**: `verify` で変更を検知したら **1**（＝書き込みを止める合図）、変更なしなら 0。

## JSON 出力の契約
```json
// snapshot
{"path":"notes.md","sha256":"...","size":11}
// verify
{"path":"notes.md","changed":true,"expected_sha256":"...","actual_sha256":"...","reason":"..."}
```

## CLAUDE.md ルール
```markdown
## ファイル上書き前の確認（手足 O4 を必ず使う）
長い作業の後や、他所で編集された可能性があるファイルを上書きする前に必ず実行する：

    python ~/.claude/hands/O4-file-state/filestate.py verify <パス> --sha256 <読んだ時の値> --json

- changed が true なら**書き込まず**、利用者に差分を報告して指示を仰ぐ。
- ファイルを読んだら snapshot で sha256 を控えておく。
```

## テスト
```bash
python test_filestate.py   # 指紋/変更なし/変更検知/削除検知/不在。失敗0で exit 0。
```
