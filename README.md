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
| [L1](L1-weather/) | 天気取得 | 現在の天気を実データで取得（Open-Meteo・キー不要）。 | `python weather.py --city 東京 --json` |
| [L4](L4-earthquake/) | 地震情報取得 | 世界の最新地震を実データで取得（USGS・キー不要）。 | `python quake.py --min-mag 5 --json` |
| [L5](L5-holidays/) | 祝日カレンダー | 各国の祝日を実データで取得（Nager.Date・キー不要）。 | `python holidays.py 2026 --json` |
| [L6](L6-forex/) | 為替換算 | ECB公表レートで実換算（Frankfurter・キー不要）。 | `python forex.py 100 USD JPY --json` |
| [O1](O1-now/) | 正確時刻・日付 | 現在の日時を決定論的に返す。LLMの日付ハルシネーションとJST/UTCズレを消す。 | `python now.py --json` |
| [O2](O2-calc/) | 算術・カウント | 式を実際に計算（多倍長で厳密・eval不使用）。 | `python calc.py "1234*5678" --json` |
| [O3](O3-random/) | 本物の乱数 | 暗号学的乱数で偏りなく抽選・並べ替え。 | `python rand.py int 1 100 --json` |
| [O4](O4-file-state/) | ファイル状態ドリフト防止 | 読んだ後の変更を検知し上書き事故を止める。 | `python filestate.py snapshot notes.md --json` |
| [O5](O5-truncation-check/) | truncation検知 | 出力が途中で切れていないか機械的に検知。 | `python truncheck.py '{"a":1' --json` |
| [O6](O6-encoding/) | 文字コード・BOM | エンコーディング/BOM/改行を実バイトから判定・変換。 | `python encodingfix.py inspect file.txt --json` |
| [O7](O7-idempotency/) | 冪等化 | 台帳で二重送信・二重通知を機械的に防ぐ。 | `python idem.py claim --ledger l.json --payload '{"to":"x"}'` |
| [O9](O9-locale-number/) | ロケール正規化 | `1.234,56`(欧州式)等の1000倍誤読を防ぐ。 | `python localenorm.py "1.234,56" --json` |
| [O10](O10-path-check/) | パス・cwdドリフト防止 | パス正規化・実在確認・基準外への脱出検知。 | `python pathcheck.py "notes.md" --json` |
| [O11](O11-quote-check/) | 出典接地 | 引用が出典に実在するか照合（ねつ造防止）。 | `python quotecheck.py "引用" --file src.md --json` |
| [S2](S2-password-gen/) | パスワード生成 | 暗号学的乱数で文字種を保証して生成。 | `python genpw.py --length 20 --json` |
| [S3](S3-uuid-ulid/) | UUID・ULID | 安全な乱数で正しい形式のIDを発行。 | `python uuidgen.py --json` |
| [S7](S7-json-csv/) | JSON⇔CSV | 列ズレ・引用符を壊さず相互変換（YAML非対応）。 | `python jsoncsv.py to-csv '[{"a":1}]'` |
| [S4](S4-hash/) | ハッシュ計算 | MD5/SHA-1/256/512。LLMが計算できないものを確実に。 | `python hash.py hello --json` |
| [S5](S5-base64/) | Base64変換 | エンコード/デコード（URLセーフ対応）。 | `python base64tool.py encode hi --json` |
| [S6](S6-json-format/) | JSON整形・検証 | 整形/圧縮/検証。崩れたJSONの場所を指す。 | `python jsonfmt.py '{"a":1}' --json` |
| [S8](S8-jwt-decode/) | JWTデコード | header/payloadを復号（署名は検証しない）。 | `python jwtdecode.py <token> --json` |
| [S9](S9-url-encode/) | URLエンコード | パーセントエンコード/デコード。 | `python urltool.py encode "a b" --json` |
| [S11](S11-char-count/) | 文字数カウンタ | 文字/単語/行/出現数。LLMが数え間違うものを確実に。 | `python countchars.py strawberry --find r --json` |
| [S12](S12-case-convert/) | ケース変換 | camel/snake/kebab/constant 等を相互変換。 | `python casetool.py helloWorldFoo --json` |
| [S22](S22-bmi/) | BMI計算 | BMIと肥満判定・標準体重。 | `python bmi.py 170 65 --json` |
| [S25](S25-loan/) | ローン返済 | 元利均等の毎月返済額・総利息。 | `python loan.py --principal 3000000 --rate 1.5 --years 10 --json` |
| [S26](S26-compound/) | 複利積立 | 積立の将来価値（月複利）。 | `python compound.py --monthly 30000 --rate 5 --years 20 --json` |
| [S29](S29-split-bill/) | 割り勘 | 端数込みで合計がちょうど合う割り勘。 | `python splitbill.py 10000 3 --json` |
| [S39](S39-cron/) | Cron式の読み解き | cron式を展開・検証し日本語で説明。 | `python cron.py "0 9 * * 1-5" --json` |
| [S13](S13-text-diff/) | テキスト差分 | 2テキストのunified diffと増減行数。 | `python textdiff.py a.txt b.txt --json` |
| [S15](S15-color-convert/) | カラー変換 | HEX/RGB/HSL を相互変換（HSLも正確）。 | `python color.py "#FF6A3D" --json` |
| [S14](S14-regex-test/) | 正規表現テスター | 実際に照合しマッチ位置・グループを返す。 | `python regextest.py "\d+" "a1 b22" --json` |
| [S19](S19-radix/) | 進数変換 | 2/8/10/16進を相互変換（負数・接頭辞対応）。 | `python radix.py 0xFF --json` |
| [S20](S20-unit-convert/) | 単位変換 | 長さ/重さ/温度を換算。 | `python unitconv.py 32 F C --json` |
| [S21](S21-percent/) | 割合計算 | 〜の何%/何%は幾つ/増減率。 | `python percent.py of 25 200 --json` |
| [S27](S27-tax/) | 消費税計算 | 税込⇔税抜（軽減税率・端数対応）。 | `python tax.py 1000 --json` |
| [S40](S40-password-strength/) | パスワード強度 | 推定エントロピー(bit)と判定。 | `python pwstrength.py 'Abc123!@' --json` |
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
