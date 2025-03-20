# %%
import pyrealsense2 as rs
import numpy as np
import cv2
import tkinter as tk
from tkinter import Button
import threading

# ======== RealSenseの設定 ========
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline_profile = pipeline.start(config)
color_profile = pipeline_profile.get_stream(rs.stream.color).as_video_stream_profile()
color_intrinsics = color_profile.get_intrinsics()

# 画像を保存する関数
def capture_image():
    if color_image is not None:
        cv2.imwrite("color_capture.png", color_image)
        print("Saved: color_capture.png")

# プログラム終了処理
def exit_program():
    global running
    running = False
    pipeline.stop()  # RealSenseの停止
    root.quit()      # tkinterのメインループを終了
    root.destroy()   # GUIウィンドウを閉じる
    print("Program exited successfully.")

# RealSenseから画像を取得し、OpenCVで表示するスレッド関数
def show_camera():
    global color_image, running
    while running:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if color_frame:
            color_image = np.asanyarray(color_frame.get_data())

            # 画像を表示
            cv2.imshow("RealSense Camera", color_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q'キーで終了
            exit_program()
            break

    cv2.destroyAllWindows()

# ======== GUI（tkinter）設定 ========
root = tk.Tk()
root.title("RealSense Control")
root.geometry("200x100")

# ボタン
btn_capture = Button(root, text="Capture", command=capture_image, height=2, width=10)
btn_capture.pack()

btn_exit = Button(root, text="Exit", command=exit_program, height=2, width=10)
btn_exit.pack()

# ======== 画像取得スレッド開始 ========
running = True
thread = threading.Thread(target=show_camera, daemon=True)
thread.start()

# GUIループ
root.mainloop()


# %%



