import os
import openai
import dotenv
from PIL import Image

# OpenAI APIキーを設定
dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 画像が保存されているディレクトリ
image_folder = "/Users/mmineno/Downloads/ib_images"

# 画像ファイルの拡張子
image_extensions = [".png", ".jpg", ".jpeg"]


# 画像ファイルを読み込み、コメントを出力し、Markdownファイルに保存する関数
def process_images():
    for filename in os.listdir(image_folder):
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            image_path = os.path.join(image_folder, filename)
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()

            # 画像からコメントを取得
            response = openai.Image.create(
                image=image_data,
                n=1,
                size="512x512",
                prompt="Please describe the contents of this web application screenshot in detail.",
                temperature=0,
            )

            # コメントを取得
            comments = response["data"][0]["text"]

            # Markdownファイルに保存
            markdown_filename = f"{os.path.splitext(filename)[0]}.md"
            markdown_filepath = os.path.join(image_folder, markdown_filename)

            with open(markdown_filepath, "w") as markdown_file:
                markdown_file.write(comments)

            print(f"Processed {filename}, saved comments to {markdown_filename}")


# スクリプトを実行
if __name__ == "__main__":
    process_images()
