# %%
import pyrealsense2 as rs
import numpy as np
import cv2
import os
import threading
import tkinter as tk
from tkinter import Button
from datetime import datetime

# ======== RealSenseの設定 ========
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

# 保存フォルダ
save_dir = "captured_frames"
os.makedirs(save_dir, exist_ok=True)

# ループ制御用フラグ
running = False
exit_flag = False  # 終了フラグ（プレビューの停止用）

# ======== 画像保存関数 ========
def save_frame(frame):
    """ フレームをファイル名の衝突なしで保存 """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # ミリ秒3桁
    filename = os.path.join(save_dir, f"frame_{timestamp}.png")
    cv2.imwrite(filename, frame)
    print(f"Saved: {filename}")

# ======== カメラプレビュー（常に表示） ========
def update_preview():
    """ Start前でもリアルタイムで映像を表示する """
    global exit_flag
    while not exit_flag:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        color_image = np.asanyarray(color_frame.get_data())

        # OpenCVで表示（Start前は保存せず、表示のみ）
        cv2.imshow("RealSense", color_image)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' で完全終了
            stop_all()
            break

# ======== 画像取得スレッド（Start後に保存） ========
def capture_frames():
    global running
    while running:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        color_image = np.asanyarray(color_frame.get_data())

        # フレームを保存
        save_frame(color_image)

# ======== GUI（tkinter）設定 ========
root = tk.Tk()
root.title("RealSense Capture")
root.geometry("300x200")

def start_capture():
    """ 撮影を開始 """
    global running
    if not running:
        running = True
        thread = threading.Thread(target=capture_frames, daemon=True)
        thread.start()
        print("Capture started")

def stop_capture():
    """ 撮影を停止（プレビューは続行） """
    global running
    running = False
    print("Capture stopped")

def stop_all():
    """ 完全終了処理 """
    global running, exit_flag
    running = False
    exit_flag = True
    pipeline.stop()
    cv2.destroyAllWindows()
    root.quit()
    root.destroy()
    print("Program exited.")

# ボタン
btn_start = Button(root, text="Start", command=start_capture, height=2, width=10)
btn_start.pack(pady=10)

btn_stop = Button(root, text="Stop", command=stop_capture, height=2, width=10)
btn_stop.pack(pady=10)

btn_exit = Button(root, text="Exit", command=stop_all, height=2, width=10)
btn_exit.pack(pady=10)

# OpenCVのプレビューを開始（別スレッド）
preview_thread = threading.Thread(target=update_preview, daemon=True)
preview_thread.start()

# GUIループ
root.mainloop()


# %%



