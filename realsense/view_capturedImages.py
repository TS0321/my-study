# %%
import cv2
import os
import natsort

# 保存フォルダ
save_dir = "captured_frames"

# 画像リストを取得（自然順にソート）
image_files = natsort.natsorted([f for f in os.listdir(save_dir) if f.endswith(".png")])

if not image_files:
    print("No images found in", save_dir)
    exit()

# 現在のインデックス
index = 0

while True:
    # 画像を読み込んで表示
    img_path = os.path.join(save_dir, image_files[index])
    image = cv2.imread(img_path)
    
    if image is None:
        print(f"Failed to load: {img_path}")
        break

    cv2.imshow("Captured Image Viewer", image)
    print(f"Showing {index+1}/{len(image_files)}: {image_files[index]}")

    # キー入力を待つ
    key = cv2.waitKey(0)

    if key == ord('q'):  # 'q'キーで終了
        break
    elif key == ord('d') or key == 2555904:  # '→'キー (Next)
        index = (index + 1) % len(image_files)
    elif key == ord('a') or key == 2424832:  # '←'キー (Prev)
        index = (index - 1) % len(image_files)

cv2.destroyAllWindows()


# %%



