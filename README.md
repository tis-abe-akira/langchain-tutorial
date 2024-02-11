# このプロジェクトについて

このプロジェクトはLangChainのTutorialです。

## 勉強会のコード

勉強会の説明資料は、こちらです。
https://qiita.com/akiraabe/items/1a9b941a7bf73b1bbb16

[TBD]

## その他のコード

src/ExcelAIConnector.py

Excelファイルを入力として、AIを呼び出し、結果を出力するプログラムです。

### 使い方

プロジェクトディレクトリ直下のconfig.yamlを必要に応じて編集してください。

```yaml
# 入力ファイル
INPUT_FILE: data/参加者アンケート.xlsx
# 出力ファイル
OUTPUT_FILE: data/result.csv
# テンプレートファイル
TEMPLATE_FILE: data/template.txt
# チャンクサイズ（一度に処理する件数を指定します。AI呼び出しがエラーになった場合に、処理結果が失われるため、ある程度の件数ごとに処理することを推奨。）
CHUNK_SIZE: 100
# 開始位置（処理の開始位置。この値以上のNUMBER_LOCが処理対象となります。）
START_POSITION: 1
# モデルID
MODEL_ID: anthropic.claude-v2
# Excelファイルの入力ファイルのキーの位置（例では、アンケート回収時に連番が自動的に付与されます。）
NUMBER_LOC: 0
# Excelファイル中の値の位置（例では、アンケートの回答）
VALUE_LOC: 1

```

TEMPLATE_FILEの内容をAIに指示したい内容に書き換えてください。
* 以下は、テンプレートの例です。
* {message}の部分には、Excelから読み込んだ値の回答が入ります。(ここのプレースホルダーは**必ず {message} としてください。**)

```txt
以下は、プレゼント配布イベントのアンケート結果です。これをポジティブと捉えるか？ネガティブと捉えるか？
今後の改善のヒントとして何が得られるのか？というのを答えてください。
対応の優先度（至急、高い、普通、低い）も付けてください。

アンケート回答###
{message}
###

回答形式###
ポジティブな要素：
ネガティブな要素：
改善のヒント：
対応の優先度：
###
```