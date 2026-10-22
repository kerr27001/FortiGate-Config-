import re
import os

def process_policy_file(input_filename, output_filename):
    # 檢查檔案是否存在
    if not os.path.exists(input_filename):
        print(f"錯誤：找不到檔案 '{input_filename}'")
        return

    edit_pattern = re.compile(r'^(\s*)edit\s+\d+')
    uuid_pattern = re.compile(r'^\s*set uuid')
    
    current_id = 1
    processed_lines = []

    with open(input_filename, 'r', encoding='utf-8') as f:
        for line in f:
            # 1. 跳過 UUID 行
            if uuid_pattern.search(line):
                continue
            
            # 2. 重新編號 edit
            edit_match = edit_pattern.match(line)
            if edit_match:
                indent = edit_match.group(1)
                processed_lines.append(f"{indent}edit {current_id}\n")
                current_id += 1
            else:
                # 3. 其他行原樣保留
                processed_lines.append(line)

    # 4. 寫入新檔案
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)
    
    print(f"處理完成！已產出新檔案：{output_filename}")

# --- 設定區 ---
input_file = "policy.txt"        # 你的原始檔名
output_file = "policy_fixed.txt" # 處理後的檔名

process_policy_file(input_file, output_file)
