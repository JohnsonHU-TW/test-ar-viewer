import trimesh
from trimesh.visual.material import PBRMaterial
from trimesh.visual import TextureVisuals
import os

def to_glb(case):
    try:
        mesh1 = trimesh.load(rf'W:\隨機11例(.obj)\{case}\model_gland.obj')
        mesh2 = trimesh.load(rf'W:\隨機11例(.obj)\{case}\model_pz.obj')
        mesh3 = trimesh.load(rf'W:\隨機11例(.obj)\{case}\mesh_lesion.obj')
    except Exception as e:
        print(f"錯誤：無法載入 STL 檔案。請檢查檔案路徑。 {e}")
        exit()

    # --- 2. 為每個網格建立並指派"明確的"PBR材質 ---
    SCALE_FACTOR = 0.001
    # --- 1B. 應用縮放 ---
    # *** 在設定材質前，將所有模型套用相同的縮放 ***
    mesh1.apply_scale(SCALE_FACTOR)
    mesh2.apply_scale(SCALE_FACTOR)
    mesh3.apply_scale(SCALE_FACTOR)
    # mesh1: 紅色, 完全不透明 (預設 alphaMode 是 OPAQUE)
    # PBRMaterial 的 baseColorFactor 接受 0-255 的 RGBA
    mat1 = PBRMaterial(baseColorFactor=[0, 0, 255, 128],
                       alphaMode='BLEND'
                       )
    # 使用 .visual.material 來指派材質
    mesh1.visual = TextureVisuals(material=mat1)
    # mesh2: 綠色, 50% 半透明
    mat2 = PBRMaterial(
        baseColorFactor=[0, 255, 0, 192],  # 50% Alpha
        alphaMode='BLEND'                  # <-- 這是關鍵！
    )
    mesh2.visual = TextureVisuals(material=mat2)

    # mesh3: 藍色, 30% 半透明
    mat3 = PBRMaterial(
        baseColorFactor=[255, 0, 0, 255]   # 30% Alpha                  # <-- 這是關鍵！
    )
    mesh3.visual = TextureVisuals(material=mat3)


    # 3. 將三個網格合併到一個 "場景" (Scene) 中
    scene = trimesh.Scene([mesh1, mesh2, mesh3])

    # 4. 將場景匯出為 GLB 檔案
    try:
        output_file = f'{case}.glb'
        scene.export(output_file)
        print(f"成功匯出 {output_file}")
    except Exception as e:
        print(f"匯出 GLB 時發生錯誤: {e}")

cases = os.listdir(r'W:\隨機11例(.obj)')
for case in cases:
    to_glb(case)