import os
import dotenv
import anthropic

# .envファイルから環境変数を読み込む
dotenv.load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
# print(api_key)

# Anthropic APIのクライアントを設定
client = anthropic.Anthropic(api_key=api_key)

markdown_header = "|名詞|説明|\n|---|---|"

def process_files(input_folder, output_folder):
    result_markdown = ""
    # 現在のスクリプトのディレクトリを取得
    base_dir = os.path.dirname(__file__)
    
    input_folder = os.path.join(base_dir, input_folder)

    output_folder = os.path.join(base_dir, output_folder)

    # 入力フォルダと出力フォルダの存在確認
    if not os.path.exists(input_folder):
        print("Input folder does not exist.")
        return
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # フォルダ内の全テキストファイルを読み込む
    filenames = [f for f in os.listdir(input_folder) if f.endswith('.md')]
    for i, filename in enumerate(filenames):
        if i != 16:
            continue  
        with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"Processing file {i} {filename}")

#         prompt = f"""
# <markdown>
# {result_markdown}
# </markdown>
# <content>
# {content}
# </content>

# 訪問看護電子カルテのマニュアルから、システムに関連する全ての固有名詞を抜き出しmarkdowのtableで出力。
# |名詞|説明|

# 名詞は、訪問看護の業務、看護一般、システムの機能、ユーザロール、入力項目、関連機能など、マニュアルに登場する全ての名詞を網羅的に抽出してください。
# ロゴや表などの一般的な固有名詞は除外してください。
# 特に、上位概念と下位概念の関係性にも注意を払い、マニュアル中に登場する全ての名詞を漏れなく抽出するよう心がけてください。

# 既に<markdown>に存在する名詞については、元の説明に新たに説明を追記する必要があるか判断してください。
# 必要がある場合は、元の説明に新しい説明を追記して再度出力してください。必要がない場合は出力しないでください。

# <content>に新しく登場する名詞は抽出します。
# マニュアルの記述を参考に、訪問看護の一般的な概念から補足して詳細な説明を付けてください。
# わからない場合は空白のままで構いません。
#         """

#         prompt = f"""
# <markdown>
# {result_markdown}
# </markdown>
# <content>
# {content}
# </content>

# 訪問看護電子カルテのマニュアルから、システムに関連する全ての固有名詞を抜き出しmarkdowのtableで出力。
# |名詞|説明|

# 名詞は、訪問看護の業務、看護一般、システムの機能、ユーザロール、入力項目、関連機能など、マニュアルに登場する全ての名詞を網羅的に抽出してください。
# ロゴや表などの一般的な固有名詞は除外してください。
# 特に、上位概念と下位概念の関係性にも注意を払い、マニュアル中に登場する全ての名詞を漏れなく抽出するよう心がけてください。

# 既に<markdown>に存在する名詞については、元の説明に新たに説明を追記する必要があるか判断してください。
# 必要がある場合は、元の説明に新しい説明を追記して再度出力してください。必要がない場合は出力しないでください。

# <content>に新しく登場する名詞は抽出します。
# マニュアルの記述を参考に、訪問看護の一般的な概念から補足して詳細な説明を付けてください。
# わからない場合は空白のままで構いません。
#         """
#         print(prompt)
        
            prompt = f"""
<content>
{content}
</content>

訪問看護電子カルテのマニュアルから、システムに関連する全ての固有名詞を抜き出しmarkdowのtableで出力。
|名詞|説明|

名詞は、訪問看護の業務、看護一般、システムの機能、ユーザロール、入力項目、関連機能など、マニュアルに登場する全ての名詞を網羅的に抽出してください。
ロゴや表などの一般的な固有名詞は除外してください。
特に、上位概念と下位概念の関係性にも注意を払い、マニュアル中に登場する全ての名詞を漏れなく抽出するよう心がけてください。

既に<markdown>に存在する名詞については、元の説明に新たに説明を追記する必要があるか判断してください。
必要がある場合は、元の説明に新しい説明を追記して再度出力してください。必要がない場合は出力しないでください。

<content>に新しく登場する名詞は抽出します。
マニュアルの記述を参考に、訪問看護の一般的な概念から補足して詳細な説明を付けてください。
わからない場合は空白のままで構いません。
        """
        try:
            # APIを呼び出してメッセージを生成
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=4096,
                temperature=0,
                # system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": markdown_header},
                ]
            )

            result_text = response.content[0].text
            print(response)
            # print(result_text)
            
            # APIの応答を出力フォルダに保存
            output_file_path = os.path.join(output_folder, f"{i+1}_{filename}")
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(result_text)
                
            print(f"Output saved to {output_file_path}")
            result_markdown += f"""
|{i}|{filename}|
{result_text}"""
        
        except Exception as e:
            # エラー発生時の処理
            print(f"Error processing file {filename}: {e}")
            break  # エラーが発生したらループを中断
    print(result_markdown)
    with open(os.path.join(output_folder, "result.txt"), 'w', encoding='utf-8') as output_file:
        output_file.write(markdown_header + result_markdown)

# 使用例
input_folder = 'sections'
output_folder = 'yogoshu-tmp'
process_files(input_folder, output_folder)
