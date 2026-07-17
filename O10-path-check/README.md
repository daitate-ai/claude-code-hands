# O10 パス / cwd ドリフト防止 — Claude Code の手足

パスを**正規化**し、実在性と「基準ディレクトリの外に出ていないか」を確認するスクリプト。

## なぜ手足にするのか
Windows の円記号パス・空白入りパス・相対パスと cwd のズレで、「あるはずのファイルが無い」「意図しない場所に書く」事故が起きる。さらに `../` による**基準外への脱出**は、書き込み先を誤る危険がある。機械的に確認して止める。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `pathcheck.py` を `~/.claude/hands/O10-path-check/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python pathcheck.py "..\data\a.txt"
python pathcheck.py "../x" --base /home/me/proj    # 基準の外に出ていないか
python pathcheck.py "notes.md" --json
```

**exit code**: `--base` 指定時、基準の外を指していたら **1**（＝止める合図）。

## JSON 出力の契約
```json
{"input":"../x","absolute":"...","posix":"...","exists":false,"is_dir":false,"is_file":false,
 "cwd":"...","has_space":false,"base":"...","inside_base":false,"warning":"..."}
```
`posix` は `/` 区切りに正規化した形。

## CLAUDE.md ルール
```markdown
## パスの確認（手足 O10 を必ず使う）
ファイルを書く前・パスが怪しい時は、推測せず必ず実行して確認する：

    python ~/.claude/hands/O10-path-check/pathcheck.py "<パス>" --base "<プロジェクト根>" --json

- inside_base が false なら**書き込まない**（意図しない場所への書き込みを防ぐ）。
- exists / is_file を見てから読み書きする。cwd のズレは absolute と cwd を比較して判断。
```

## テスト
```bash
python test_pathcheck.py   # 実在/種別/正規化/基準内/脱出検知。失敗0で exit 0。
```
