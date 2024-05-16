def process_markdown(input_filepath, output_filepath):
    # ファイルを読み込む
    with open(input_filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 新しいマークダウンテーブルを構築
    new_lines = ['|名詞|説明|ファイル名|\n', '|--|--|--|\n']
    current_filename = None

    for i, line in enumerate(lines):
        # if i > 10:
        #     break
        if line.strip() and line.startswith('|') and not line.startswith('|--'):
            parts = line.strip().split('|')
            if len(parts) > 1 and parts[1].endswith('.md'):
                # ファイル名とインデックスが記載されている行
                current_filename = parts[1].strip().replace('.md', '')
            elif len(parts) > 2 and parts[2].endswith('.md'):
                # ファイル名とインデックスが記載されている行
                current_filename = parts[2].strip().replace('.md', '')
            elif current_filename:
                # 通常のデータ行、ファイル名を追加
                new_line = f'|{parts[1].strip()}|{parts[2].strip()}|{current_filename}|\n'
                new_lines.append(new_line)

    # 変更したマークダウンをファイルに書き込む
    with open(output_filepath, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

# 使用例
input_filepath = 'generate-yogoshu/result.md'
output_filepath = 'generate-yogoshu/modified-result.md'
process_markdown(input_filepath, output_filepath)
