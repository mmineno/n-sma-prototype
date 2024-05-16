import csv
from collections import defaultdict

def merge_markdown_rows(input_filepath, output_filepath):
    # データを格納する辞書を準備
    data_dict = defaultdict(lambda: defaultdict(set))

    # ファイルを読み込む
    with open(input_filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='|')
        next(reader)  # ヘッダー行をスキップ
        next(reader)  # 区切り行をスキップ
        for row in reader:
            if len(row) < 4:
                continue
            noun, description, filename = [x.strip() for x in row[1:4]]
            data_dict[noun][description].add(filename)

    # 新しいマークダウンテーブルを構築
    with open(output_filepath, 'w', encoding='utf-8') as file:
        file.write("|名詞|説明|ファイル名|\n")
        file.write("|--|--|--|\n")
        for noun in sorted(data_dict.keys()):  # 名詞をソート
            descriptions = data_dict[noun]
            first = True
            for description, filenames in descriptions.items():
                files = ','.join(sorted(filenames))
                if first:
                    file.write(f"|{noun}|{description}|{files}|\n")
                    first = False
                else:
                    file.write(f"||{description}|{files}|\n")
# 使用例
input_filepath = 'generate-yogoshu/modified-result.md'
output_filepath = 'generate-yogoshu/merged-result.md'
merge_markdown_rows(input_filepath, output_filepath)
