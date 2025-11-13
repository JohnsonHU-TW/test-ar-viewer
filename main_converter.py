# 檔案名稱: main_converter.py (V3 - 強制 PYTHONHOME 版)
# ---------------------------------------------------

import subprocess
import os
import sys
import copy


def convert_obj_to_usdz_with_blender(input_obj_path, output_usdz_path):
    # --- 1. 設定路徑 ---

    # (您已經手動設定了這個，保持不變)
    BLENDER_EXE_PATH = r"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"

    # (*** 關鍵修復 1 ***)
    # 根據您的日誌，Blender 4.5.4 LTS 將其版本檔案儲存在 "4.5" 資料夾中
    # 我們需要建構 Blender 內部 Python 的路徑
    blender_dir = os.path.dirname(BLENDER_EXE_PATH)
    blender_version_subfolder = "4.5"  # 根據您的日誌 "Blender 4.5.4 LTS"

    # 建立 Blender 的 PYTHONHOME 路徑
    BLENDER_PYTHON_HOME = os.path.join(blender_dir, blender_version_subfolder, "python")

    if not os.path.exists(BLENDER_PYTHON_HOME):
        print(f"錯誤：找不到 Blender 的 Python 目錄: {BLENDER_PYTHON_HOME}")
        print("請檢查 'blender_version_subfolder' 變數是否與您的 Blender 安裝一致。")
        return

    # 腳本路徑
    SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "blender_script.py")
    INPUT_PATH = os.path.abspath(input_obj_path)
    OUTPUT_PATH = os.path.abspath(output_usdz_path)

    if not os.path.exists(INPUT_PATH):
        print(f"錯誤：輸入檔案不存在: {INPUT_PATH}")
        return

    if not os.path.exists(SCRIPT_PATH):
        print(f"錯誤：Blender 腳本不存在: {SCRIPT_PATH}")
        return

    # --- 2. 建立命令 (保持不變) ---
    command = [
        BLENDER_EXE_PATH,
        "--background",
        "--python",
        SCRIPT_PATH,
        "--",
        INPUT_PATH,
        OUTPUT_PATH
    ]

    # --- 3. (關鍵修復 2) 建立乾淨的環境變數 ---
    print("正在準備乾淨的執行環境...")

    # 複製一份當前的環境變數
    clean_env = copy.deepcopy(os.environ)

    # 移除 Anaconda 的 PYTHONPATH
    removed_path = clean_env.pop("PYTHONPATH", " (未找到)")
    print(f"  - 已移除 PYTHONPATH: {removed_path}")

    # *** 強制設定 PYTHONHOME ***
    # 告訴 Blender "這才是你的 Python 函式庫，不要管 Anaconda"
    clean_env["PYTHONHOME"] = BLENDER_PYTHON_HOME
    print(f"  - 已強制設定 PYTHONHOME: {BLENDER_PYTHON_HOME}")

    # --- 4. 執行轉換 ---
    print(f"正在啟動 Blender 進行轉換...")
    print(f"命令: {' '.join(command)}")

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            env=clean_env  # <--- *** 傳入我們修改過的環境 ***
        )

        print("--- Blender 輸出 (STDOUT) ---")
        print(result.stdout)
        print("-------------------------------")

        if result.stderr:
            print("--- Blender 警告/錯誤 (STDERR) ---")
            print(result.stderr)
            print("-----------------------------------")

        print(f"\n轉換成功！已儲存檔案至: {OUTPUT_PATH}")

    except subprocess.CalledProcessError as e:
        print(f"錯誤：Blender 轉換失敗 (Return Code: {e.returncode})。")
        print("--- Blender 輸出 (STDOUT) ---")
        print(e.stdout)
        print("-------------------------------")
        print("--- Blender 錯誤 (STDERR) ---")
        print(e.stderr)
        print("-------------------------------")

    except Exception as e:
        print(f"執行時發生未預期的錯誤: {e}")


# --- 如何使用 ---
if __name__ == "__main__":
    # (保持不變)
    INPUT_FILE = "NCKU_Test_32.glb"
    OUTPUT_FILE = "NCKU_Test_32.usdz"

    convert_obj_to_usdz_with_blender(INPUT_FILE, OUTPUT_FILE)