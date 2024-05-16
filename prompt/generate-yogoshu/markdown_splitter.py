import os

def split_and_save_markdown(file_path, output_directory):
    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # マークダウンファイルを読み込む
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # '### 'でセクションを分割する
    sections = content.split('### ')
    
    # 最初の要素は通常空またはヘッダーなので除外
    for section in sections[1:]:
        # 最初の改行までが見出しとなる
        header_end = section.find('\n')
        if header_end != -1:
            title = section[:header_end].strip()
            body = section[header_end + 1:].strip()
            
            # ファイル名に使用できない文字を置換
            filename = "".join([c for c in title if c.isalnum() or c in (' ', '_')]).rstrip()
            file_path = os.path.join(output_directory, f"{filename}.md")
            
            # ファイルに書き出す
            with open(file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(body)
            print(f"Saved: {file_path}")

# 使用例
if __name__ == "__main__":
    split_and_save_markdown('iBowサポート.md', 'sections')