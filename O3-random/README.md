# O3 本物の乱数 — Claude Code の手足

**暗号学的乱数**で、偏りなく選ぶ・並べ替える・サイコロを振るスクリプト。

## なぜ手足にするのか
LLM に「1〜100で適当に」と頼んでも**乱数にならない**。人間同様、特定の数（37・42・73…）へ強く偏る。抽選・サンプリング・順番決めをLLMに任せると公平性が壊れる。このスクリプトは OS の乱数（`secrets`）を使う。

## 依存
なし（Python 3.8+ 標準ライブラリ `secrets` のみ）。

## インストール
1. `rand.py` を `~/.claude/hands/O3-random/` にコピー。
2. 下の「CLAUDE.md ルール」を `CLAUDE.md` に追記。

## 使い方
```bash
python rand.py int 1 100            # 範囲の整数(両端含む)
python rand.py int 1 6 --count 5
python rand.py choice りんご みかん ぶどう
python rand.py shuffle a b c d
python rand.py dice 2d6
python rand.py int 1 100 --json
```

## JSON 出力の契約
```json
{"mode":"int","low":1,"high":100,"values":[73]}
{"mode":"choice","items":["a","b"],"value":"a"}
{"mode":"shuffle","items":["a","b"],"value":["b","a"]}
{"mode":"dice","spec":"2d6","rolls":[2,4],"total":6}
```

## CLAUDE.md ルール
```markdown
## 乱数・抽選（手足 O3 を必ず使う）
「ランダムに選んで」「順番を決めて」「抽選して」と言われたら、自分で選ばず必ず実行する：

    python ~/.claude/hands/O3-random/rand.py int <下限> <上限> --json
    python ~/.claude/hands/O3-random/rand.py choice <候補...> --json
    python ~/.claude/hands/O3-random/rand.py shuffle <項目...> --json
```

## テスト
```bash
python test_rand.py   # 範囲/全値出現/一様性/choice/shuffle保存/サイコロ。失敗0で exit 0。
```
※ 乱数値は固定できないため、必ず成り立つ性質（範囲・要素保存・全値出現・極端な偏りがないこと）を検証している。
