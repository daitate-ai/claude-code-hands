# O7 冪等化 — Claude Code の手足

「もう実行したか？」を台帳で機械的に保証し、**二重実行を防ぐ**スクリプト。

## なぜ手足にするのか
「もう送ったか？」をLLMの記憶に頼ると、**二重送信・二重通知・二重投稿**が起きる（セッションが変われば記憶は消える）。台帳（JSONファイル）に処理済みキーを残せば、何度呼ばれても一度きりを保証できる。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `idem.py` を `~/.claude/hands/O7-idempotency/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python idem.py key '{"to":"x","msg":"hi"}'                   # 内容から安定キー
python idem.py claim --ledger sent.json --payload '{"to":"x"}'  # 初回だけ通す
python idem.py claim --ledger sent.json --key <キー>
python idem.py list --ledger sent.json
```

**exit code**: `claim` が**既に処理済みなら 1**（＝実行を止める合図）、初回なら 0。

## 仕様
- キーは内容の sha256。**JSONならキーの順序差を吸収**する（`{"a":1,"b":2}` と `{"b":2,"a":1}` は同じキー）。
- 台帳は一時ファイル経由で**原子的に置換**して書く（書き込み中の破損を防ぐ）。
- 台帳が壊れていたらエラーにする（黙って"未処理"扱いにして二重実行しない）。

## JSON 出力の契約
```json
{"key":"...","claimed":true,"reason":"初回です（実行してよい）"}
{"key":"...","claimed":false,"first_seen":null,"reason":"既に処理済みです（二重実行を防ぎました）"}
```

## CLAUDE.md ルール
```markdown
## 二重実行の防止（手足 O7 を必ず使う）
送信・通知・投稿・課金など「一度きりであるべき操作」の前に必ず実行する：

    python ~/.claude/hands/O7-idempotency/idem.py claim --ledger <台帳> --payload '<内容>' --json

- claimed が false なら**実行しない**（既に済んでいる）。
- 記憶や会話履歴で「送ったっけ？」を判断しない。台帳が唯一の真実源。
```

## テスト
```bash
python test_idem.py   # キー安定性/JSON順吸収/初回のみ/永続化/壊れ台帳検知。失敗0で exit 0。
```
