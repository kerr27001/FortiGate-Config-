# FortiGate Config 策略清理與重整工具

這是一個專門用來清理和重整 **Fortinet FortiGate 防火牆設定檔（Config）** 的 Python 工具。在進行防火牆設定轉移、批次建立規則或合併設定時，能有效避免 ID 衝突與 UUID 報錯。

---

## 💡 核心功能

* **自動刪除 UUID (`set uuid`)**
  * 防火牆每條 Policy 都帶有獨一無二的 UUID。轉移設定時，保留舊 UUID 會導致匯入失敗。此工具會自動將其濾除。
* **自動重新順序編號 (`edit <ID>`)**
  * 將原本混亂或重複的策略序號（如 `edit 105`、`edit 22`），由上到下重新按順序編號為 `edit 1`、`edit 2`、`edit 3`... 等。

---

## 🛠️ 使用情境

1. **設備汰舊換新**：將舊防火牆的 Policy 複製出來，清洗後貼入新設備。
2. **批次部署規則**：使用 Excel 產出大量設定後，用此腳本一次校正所有序號。
3. **設定備份合併**：將不同設備的策略段落整合時，避免 ID 重複衝突。

---

## 📋 程式碼

請將以下程式碼儲存為 `clean_policy.py`：

```python
import re
import os

def process_policy_file(input_filename, output_filename):
    # 檢查檔案是否存在
    if not os.path.exists(input_filename):
        print(f"錯誤：找不到檔案 '{input_filename}'")
        return

    # 正規表示式：匹配開頭為 edit 且後面接數字的行
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
input_file = "policy.txt"        # 原始 FortiGate 設定檔片段
output_file = "policy_fixed.txt" # 處理後的乾淨設定檔

process_policy_file(input_file, output_file)
```

---

## 🚀 使用步驟

1. **準備來源檔案**
   * 從 FortiGate 備份檔中，將要處理的 `config firewall policy` 區塊複製出來。
   * 貼到一個新文字檔中，並命名為 `policy.txt`。
2. **放置腳本**
   * 將 `policy.txt` 與上述的 `clean_policy.py` 放在同一個資料夾下。
3. **執行程式**
   * 打開終端機或命令提示字元（CMD），執行以下指令：
     ```bash
     python clean_policy.py
     ```
4. **取得結果**
   * 程式執行完成後，會在同目錄下產生 `policy_fixed.txt`。
   * 打開該檔案，即可直接複製內容並貼進新防火牆的 CLI 介面中。

⚠️ **注意事項**：為確保安全，建議**只將需要重整的 Policy 區塊**（如防火牆規則）放入 `policy.txt` 進行處理，避免影響到系統介面或其他非數字編號的設定。
