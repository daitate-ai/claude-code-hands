# S12 ケース変換 — Claude Code の手足

識別子を **camelCase / PascalCase / snake_case / kebab-case / CONSTANT_CASE / Title Case** に決定論的に変換するスクリプト。

## なぜ手足にするのか
命名規則の変換を一貫ルールで確実に行う。頭字語（HTTP）や数字の境界でブレない。

## 依存
なし（Python 3.8+ 標準ライブラリのみ）。

## インストール
1. `casetool.py` を `~/.claude/hands/S12-case-convert/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python casetool.py "helloWorldFoo"       # 全ケース表示
python casetool.py "my_var_name" --to camel
python casetool.py "HTTPServer" --json
```

## JSON 出力の契約
```json
{"words":["hello","world","foo"],"snake":"hello_world_foo","kebab":"hello-world-foo",
 "constant":"HELLO_WORLD_FOO","camel":"helloWorldFoo","pascal":"HelloWorldFoo","title":"Hello World Foo"}
```

## CLAUDE.md ルール
```markdown
## ケース変換（手足 S12 を必ず使う）
命名規則(camel/snake/kebab等)の変換を求められたら、自分で変換せず必ず実行して値を使う：

    python ~/.claude/hands/S12-case-convert/casetool.py "<識別子>" --json
    python ~/.claude/hands/S12-case-convert/casetool.py "<識別子>" --to snake
```

## テスト
```bash
python test_casetool.py   # 分解(camel/snake/kebab/頭字語)/各形式。失敗0で exit 0。
```
