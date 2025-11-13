# 檔案名稱: blender_script.py (V5 - 嚴格檢查版)
# ---------------------------------------------------
#
# 'addon_utils.enable()' 會靜默失敗 (只印出錯誤到 stdout)。
# 我們必須在啟用後使用 'addon_utils.check()' 來驗證。

import bpy
import sys
import os
import addon_utils  # 匯入 add-on 管理工具


def convert_to_usdz(input_file, output_file):
    try:
        # 1. 清空預設場景
        bpy.ops.wm.read_factory_settings(use_empty=True)

        # 2. 載入模型
        file_ext = os.path.splitext(input_file)[1].lower()

        if file_ext == '.obj':
            print(f"正在匯入 OBJ: {input_file}")
            bpy.ops.import_scene.obj(filepath=input_file)
        elif file_ext in ['.glb', '.gltf']:
            print(f"正在匯入 glTF/GLB: {input_file}")
            bpy.ops.import_scene.gltf(filepath=input_file)
        else:
            print(f"錯誤：不支援的檔案格式: {file_ext}")
            sys.exit(1)

        print("匯入成功。")

        # 3. 啟用 USD 匯出 add-on (*** 關鍵修復 ***)
        ADDON_NAME = "io_scene_usd"
        try:
            print(f"正在嘗試啟用 '{ADDON_NAME}' add-on...")
            addon_utils.enable(ADDON_NAME)
        except Exception as e:
            # 捕捉任何罕見的例外
            print(f"啟用 '{ADDON_NAME}' 過程中發生例外: {e}")
            # 即使發生例外，我們仍要進行下一步的檢查

        # *** 嚴格檢查 ***
        # 'addon_utils.check()' 會回傳 (loaded, enabled)
        loaded, enabled = addon_utils.check(ADDON_NAME)

        if not loaded or not enabled:
            print(f"致命錯誤：無法載入 '{ADDON_NAME}' add-on。")
            print(f"  - Add-on Loaded: {loaded}")
            print(f"  - Add-on Enabled: {enabled}")
            print("這幾乎可以肯定是 PYTHONHOME/PYTHONPATH 環境變數衝突。")
            sys.exit(1)  # <-- 強制退出

        print(f"Add-on '{ADDON_NAME}' 已成功載入並啟用。")
        # -------------------------------------------

        # 4. 匯出為 USDZ
        # (只有在上面檢查通過時，才會執行到這裡)
        print(f"正在匯出 USDZ: {output_file}")
        bpy.ops.export_scene.usdz(
            filepath=output_file,
            use_instancing=True,
            use_animation=False,
            use_selection=False,
            check_existing=False
        )

        print("匯出 USDZ 成功。")
        sys.exit(0)  # 回傳成功

    except Exception as e:
        # 捕捉其他可能的錯誤 (例如匯出時失敗)
        print(f"Blender 腳本執行錯誤: {e}")
        sys.exit(1)  # 回傳錯誤


if __name__ == "__main__":
    # --- 從命令列參數解析 (保持不變) ---
    try:
        args = sys.argv
        separator_index = args.index("--")
        input_path = args[separator_index + 1]
        output_path = args[separator_index + 2]

        convert_to_usdz(input_path, output_path)

    except (ValueError, IndexError):
        print("錯誤：未正確傳遞輸入和輸出路徑。")
        print("應使用: blender --background --python blender_script.py -- <input_path> <output_path>")
        sys.exit(1)