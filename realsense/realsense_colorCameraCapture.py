# %%
import pyrealsense2 as rs
import numpy as np
import cv2
import tkinter as tk
from tkinter import Button
from PIL import Image, ImageTk

# ======== RealSenseの設定 ========
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline_profile = pipeline.start(config)
color_profile = pipeline_profile.get_stream(rs.stream.color).as_video_stream_profile()
color_intrinsics = color_profile.get_intrinsics()

# ======== 画像保存関数 ========
def capture_image():
    if color_image is not None:
        cv2.imwrite("color_capture.png", color_image)
        print("Saved: color_capture.png")

# ======== 終了関数（修正） ========
def exit_program():
    global running
    if running:  # すでに止まっていないか確認
        running = False
        pipeline.stop()  # RealSenseの停止
        root.quit()      # GUIのメインループを終了
        root.destroy()   # tkinterのウィンドウを完全に閉じる
        print("Program exited successfully.")

# ======== カメラパラメータを表示 ========
def print_intrinsics(label, intrinsics):
    print(f"=== {label} ===")
    print(f" Width: {intrinsics.width}, Height: {intrinsics.height}")
    print(f" fx: {intrinsics.fx}, fy: {intrinsics.fy}")
    print(f" cx: {intrinsics.ppx}, cy: {intrinsics.ppy}")
    print(f" Distortion Model: {intrinsics.model}")
    print(f" Distortion Coeffs: {intrinsics.coeffs}\n")

print_intrinsics("Color Camera Intrinsics", color_intrinsics)

# ======== GUI（tkinter）設定 ========
root = tk.Tk()
root.title("RealSense Capture")
root.geometry("700x550")

# ラベル（カメラ映像を表示するためのキャンバス）
label = tk.Label(root)
label.pack()

# ボタン
btn_capture = Button(root, text="Capture", command=capture_image, height=2, width=10)
btn_capture.pack()

btn_exit = Button(root, text="Exit", command=exit_program, height=2, width=10)
btn_exit.pack()

# ======== 画像取得ループ ========
running = True
def update_frame():
    global color_image
    if running:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if color_frame:
            color_image = np.asanyarray(color_frame.get_data())

            # OpenCV形式 → PIL形式 に変換して表示
            img = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)

        root.after(10, update_frame)  # 10msごとに更新

# フレーム更新開始
update_frame()

# GUIループ
root.mainloop()


# %%



