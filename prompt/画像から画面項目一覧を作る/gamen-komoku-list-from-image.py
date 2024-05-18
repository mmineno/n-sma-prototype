import os
import base64
import requests
import dotenv

# OpenAI APIキーを設定
dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 画像が保存されているディレクトリ
image_folder = "/Users/mmineno/Downloads/ib_images"
output_folder = "output"

# 画像ファイルの拡張子
image_extensions = [".png", ".jpg", ".jpeg"]


# 画像ファイルをbase64エンコードする関数
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# 画像ファイルを読み込み、コメントを出力し、Markdownファイルに保存する関数
def process_images():
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    for index, filename in enumerate(os.listdir(image_folder)):
        if not any(filename.lower().endswith(ext) for ext in image_extensions):
            continue
        if index > 0:
            break

        image_path = os.path.join(image_folder, filename)
        base64_image = encode_image(image_path)

        # print(f"Processed {index}: {filename}, saved comments to {base64_image}")

        prompt = """
画像は訪問看護用電子カルテの画面である
この画像から各項目を抽出せよ
出力する項目は以下

項目名:項目の名前
種類:ラベル、テキストインプット、チェックボックス、ドロップダウン、ラジオボタン、ボタン、リンク、リスト、リスト項目など
　リストとリスト項目は分けて出力する
説明: 項目の内容やその目的を画面から読み取る、または訪問看護用電子カルテの一般的な項目を参考にした説明

markdown tableの例
| 項目名 | 種類 | 説明 |
|--|--|--|
| 会社名 | ラベル | 会社名を表示 例: 株式会社xxx（画面からラベルに対する項目を読み取る） |
| 名前 | テキストインプット | 職員の名前を入力 |
| 資格あり | チェックボックス | 職員が資格を保有すれば選択 |
| 性別 | ラジオボタン | 性別を選択 例 男性、女性、その他（画面から読み取り記載）|                               
| 生年月日 | 日付インプット | 職員の生年月日を選択 |   
| 登録情報 | ドロップダウン | 訪問看護用電子カルテの登録情報を選択 例: (表示されている項目を記載) |                                 
| メモ | テキストエリア| 備考を入力 |
| 保存 | ボタン | 職員の情報を保存 |
| ホーム | リンク | ホーム画面へ遷移 |
| 資格リスト | リスト | 職員が保有する資格のリスト。|
| 　資格名 | リスト項目 - ラベル | 資格の名称 |
| 　取得日 | リスト項目 - ラベル | 資格を取得した年月日 |
| 職員情報 | タブ | 職員情報を表示 |

アコーディオンなど例に無いものがあれば、その名称と説明を追加すること

デザイン上はボタンに見えないもの、例えば、保存ボタンの横の「キャンセル」のラベル等もボタンとして出力すること

markdownのtableのみ出力せよ
出力する前に抜け漏れがないか再度確認せよ
"""
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "List the UI elements in this web application screenshot, as markdown table.",
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
            "max_tokens": 300,
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )
        response_json = response.json()
        print(f"response: {response_json}")

        # コメントを取得
        comments = response_json["choices"][0]["message"]["content"]

        # Markdownファイルに保存
        markdown_filename = f"{os.path.splitext(filename)[0]}.md"
        markdown_filepath = os.path.join(image_folder, markdown_filename)

        with open(markdown_filepath, "w") as markdown_file:
            markdown_file.write(comments)

        print(f"Processed {index}: {filename}, saved comments to {markdown_filename}")


# スクリプトを実行
if __name__ == "__main__":
    process_images()
