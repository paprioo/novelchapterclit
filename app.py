import tkinter as tk
from tkinter import filedialog
import re
import chardet
import os
import zhconv

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        return encoding


def convert_to_utf8(input_file, output_file, encoding):
    with open(input_file, 'r', encoding=encoding) as f:
        content = f.read()
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)




def main(input_file):
    encoding = detect_encoding(input_file)

    with open(input_file, 'r', encoding=encoding) as f:
        lines = f.readlines()

    i = 0
    count = 0  # 新增計數器

    # 獲取檔案名稱（不包含副檔名）
    file_name = os.path.splitext(os.path.basename(input_file))[0]

    # 創建與檔案同名的資料夾
    output_folder = f"{file_name}"
    os.makedirs(output_folder, exist_ok=True)

    while i < len(lines):
        line = lines[i].strip()
        content = ""  # 新增 content 變數
        i += 1

        # 使用正則表達式進行匹配
        match = re.match(r'.*第.{1,7}章.*', line)
        if match:
            output_file = f"{count:03d}. {zhconv.convert(line, 'zh-hant')}.txt"  # 使用計數器和格式化輸出
            count += 1

            while i < len(lines) and not lines[i].strip().startswith("第"):
                content += lines[i]
                i += 1
                content = zhconv.convert(content, 'zh-hant') # 文件內容簡轉繁

            # 將結果放在資料夾內
            output_file_path = os.path.join(output_folder, output_file)

            convert_to_utf8(input_file, output_file_path, encoding)
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(content)


def select_input_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        main(file_path)


if __name__ == '__main__':
    select_input_file()
