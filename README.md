# Claude Code Hands（手足を配る）

**Claude Code に「手足」を持たせるための、決定論スクリプト集。**

Claude Code にトークンを使って"考えさせる"と、計算・変換・整形などで微妙に間違えることがある。
このリポジトリの各「手足」は、**PCに登録して Claude Code から呼ぶ小さなスクリプト**。
同じ入力 → 同じ手順 → 同じ結果。推測せず、確定した答えを返す。

- 完成アプリを配るのではなく、**あなたの Claude Code に手足を足す**。
- あなたは目的（ゴール）を言うだけ。Claude Code が必要な手足を選び、実行し、成果物を報告する。

## 使い方 — 手足の入れ方（いちばん簡単）

入れたい手足のフォルダの URL を、**自分の Claude Code のチャットにこう貼るだけ**：

```
この「手足」を私の Claude Code に入れて。
参照: https://github.com/USERNAME/claude-code-hands/tree/main/S23-wareki-convert

やってほしいこと:
1. スクリプトを ~/.claude/hands/<フォルダ名>/ に保存
2. そのフォルダの README.md にある「CLAUDE.md ルール」を私の CLAUDE.md に追記
3. 動作確認コマンドを実行して結果を見せて
以後、この用途の依頼は必ずこの手足を使って。
```

Claude Code が URL を読み、スクリプトを保存し、CLAUDE.md に発火条件を書き込む。
次からその用途（例：西暦和暦変換）は、**必ずこの手足が使われる**。

> ポータルサイトのカタログでは、この貼り付け文を「📋 手足を入れる」ボタンでコピーできます。

## 手足の一覧

| ID | 手足 | 何をするか | 動作確認 |
|----|------|-----------|---------|
| [O1](O1-now/) | 正確時刻・日付 | 現在の日時を決定論的に返す。LLMの日付ハルシネーションとJST/UTCズレを消す。 | `python now.py --json` |
| [S3](S3-uuid-ulid/) | UUID・ULID | 安全な乱数で正しい形式のIDを発行。 | `python uuidgen.py --json` |
| [S4](S4-hash/) | ハッシュ計算 | MD5/SHA-1/256/512。LLMが計算できないものを確実に。 | `python hash.py hello --json` |
| [S5](S5-base64/) | Base64変換 | エンコード/デコード（URLセーフ対応）。 | `python base64tool.py encode hi --json` |
| [S6](S6-json-format/) | JSON整形・検証 | 整形/圧縮/検証。崩れたJSONの場所を指す。 | `python jsonfmt.py '{"a":1}' --json` |
| [S8](S8-jwt-decode/) | JWTデコード | header/payloadを復号（署名は検証しない）。 | `python jwtdecode.py <token> --json` |
| [S9](S9-url-encode/) | URLエンコード | パーセントエンコード/デコード。 | `python urltool.py encode "a b" --json` |
| [S11](S11-char-count/) | 文字数カウンタ | 文字/単語/行/出現数。LLMが数え間違うものを確実に。 | `python countchars.py strawberry --find r --json` |
| [S12](S12-case-convert/) | ケース変換 | camel/snake/kebab/constant 等を相互変換。 | `python casetool.py helloWorldFoo --json` |
| [S19](S19-radix/) | 進数変換 | 2/8/10/16進を相互変換（負数・接頭辞対応）。 | `python radix.py 0xFF --json` |
| [S23](S23-wareki-convert/) | 西暦和暦変換 | 西暦↔和暦（明治〜令和）を正確に変換。境界日・元年・改元年を間違えない。 | `python wareki.py 2024-05-01` |
| [S24](S24-date-diff/) | 日数差分 | 2日付の間隔・N日後/前をうるう年込みで正確に。 | `python datediff.py 2026/07/17 +100 --json` |

（順次追加）

## 各手足の作り（共通フォーマット）

1つの手足 = 1フォルダ。中身は：

- **スクリプト本体** … 標準ライブラリ中心・依存最小。
- **README.md** … 目的 / インストール / 使い方 / **AI 向け登録手順（CLAUDE.md ルール）** / JSON 出力契約。
- **test_*.py** … 決定論（＝常に正しい）を担保する回帰テスト。

Claude Code は各手足の README にある「CLAUDE.md ルール」ブロックを、利用者の `CLAUDE.md` に貼ることで
「その依頼が来たら必ずこの手足を使う」を固定する。

## 依存

各手足のフォルダ README を参照。多くは **Python 3.8+ 標準ライブラリのみ**（`pip install` 不要）。

## ライセンス

[MIT License](LICENSE)。自由に使用・改変・再配布できます。
