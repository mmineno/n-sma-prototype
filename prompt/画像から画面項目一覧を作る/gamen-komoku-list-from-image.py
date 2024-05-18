import os
import base64
import requests
import dotenv
import pandas as pd

# OpenAI APIキーを設定
dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 画像が保存されているディレクトリ
image_folder = "/Users/mmineno/Downloads/ib_images"

# 画像ファイルの拡張子
image_extensions = [".png", ".jpg", ".jpeg"]


# 画像ファイルをbase64エンコードする関数
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# 画像ファイルを読み込み、コメントを出力し、Excelファイルに保存する関数
def process_images():
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    for index, filename in enumerate(os.listdir(image_folder)):
        if not any(filename.lower().endswith(ext) for ext in image_extensions):
            continue
        if index > 0:
            break

        # Excelファイルに保存
        excel_filename = f"{os.path.splitext(filename)[0]}.xlsx"
        excel_filepath = os.path.join(image_folder, excel_filename)

        # 既にxlsxファイルが存在する場合はスキップ
        if os.path.exists(excel_filepath):
            continue

        image_path = os.path.join(image_folder, filename)
        base64_image = encode_image(image_path)

        prompt = """
画像は訪問看護用電子カルテの画面である
この画像から各項目を抽出せよ
出力する項目は以下

項目名:項目の名前 具体的な名前しか表示されていない場合は、抽象化して記載する
種類:ラベル、テキストインプット、チェックボックス、ドロップダウン、ラジオボタン、ボタン、リンク、リスト、リスト項目など
 リスト項目にはこれらの種類が全て含まれる
 ボタンはアイコンしか表示されない場合があるが、機能を推測して出力する
説明: 項目の内容やその目的を画面から読み取る、または訪問看護用電子カルテの一般的な項目を参考にした説明

<markdown-table-example>
| 項目名 | 種類 | 説明 |
|--|--|--|
| （値から推測） | ラベル | (説明) 例:（画面からラベルに対する項目を読み取る） |
| （ラベルまたは値から推測）入力 | テキストインプット | (説明) |
| （ラベルから推測）選択 | チェックボックス | (説明) |
| （ラベルから推測）選択| ラジオボタン |  (説明) 例: XXX,YYY（表示されている値を読み取り）|                               
| （ラベルから推測）入力 | 日付インプット |  (説明) |   
| （ラベルから推測）選択 | ドロップダウン | (説明) 例:　XXX (表示されている値を読み取り) |                                 
| （ラベルまたは値から推測）入力 | テキストエリア| (説明) |
| （ラベルから取得） | ボタン | (説明) |
| （ラベルから取得） | リンク | （ラベル）へ遷移 |
| （ラベルから取得） | タブ | （ラベル）を表示 |
| （ヘッダーまたはリスト項目から推測する） | リスト | (説明) |
| 　項目名（リストの具体的な値から推測する） | リスト項目 / (種類) | (説明) 例:（具体名の1~3個を出力） |
</markdown-table-example>

アコーディオンなど例に無いものがあれば、その名称と説明を追加すること

デザイン上はボタンに見えないもの、例えば、保存ボタンの横の「キャンセル」のラベル等もボタンとして出力すること

リストは、リストを必ず先頭に出力すること

必ず項目名は抽象化した名称にすること、具体的な名称に決してならないこと 例: 個人名や具体的な住所など

全て日本語で出力せよ
markdownのtableのみ出力せよ
"""
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            "max_tokens": 4096,
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )
        response_json = response.json()
        print(f"response: {response_json}")

        # コメントを取得
        comments = response_json["choices"][0]["message"]["content"]

        # コメントを行ごとに分割し、リスト形式に変換
        rows = [
            line.strip().split("|")[1:-1] for line in comments.strip().split("\n")[2:]
        ]

        # DataFrameに変換
        df = pd.DataFrame(rows, columns=["項目名", "種類", "説明"])

        df.to_excel(excel_filepath, index=False)

        print(f"Processed {index}: {filename}, saved comments to {excel_filename}")


# スクリプトを実行
if __name__ == "__main__":
    process_images()
