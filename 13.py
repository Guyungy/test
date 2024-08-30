import os
import cv2
from tkinter import Tk
from tkinter import filedialog

# 从视频中按间隔提取图片
def extract_frames_from_video(video_path, output_folder, interval=5):
    try:
        # 打开视频文件
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Failed to open video file: {video_path}")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)  # 获取视频帧率
        frame_interval = int(fps * interval)  # 计算间隔帧数

        count = 0
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 打印调试信息
            print(f"Processing frame {frame_count}, saving every {frame_interval} frames.")

            if frame_count % frame_interval == 0:
                # 使用简单路径进行测试
                simple_output_folder = "C:/temp"
                if not os.path.exists(simple_output_folder):
                    os.makedirs(simple_output_folder)

                frame_filename = f"frame_{count}.jpg"
                frame_filepath = os.path.join(simple_output_folder, frame_filename)

                # 保存提取的帧为图片
                success = cv2.imwrite(frame_filepath, frame)
                if success:
                    print(f"Saved frame: {frame_filepath}")
                else:
                    print(f"Failed to save frame: {frame_filepath}")

                count += 1

            frame_count += 1

        cap.release()

    except Exception as e:
        print(f"An error occurred: {e}")

# 处理文件夹中的所有视频
def process_videos_in_folder(folder_path, interval=5):
    try:
        # 遍历文件夹中的所有视频文件
        for filename in os.listdir(folder_path):
            video_path = os.path.join(folder_path, filename)
            
            # 检查是否为视频文件
            if not filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv')):
                continue
            
            # 提取视频中的帧
            extract_frames_from_video(video_path, folder_path, interval)

    except Exception as e:
        print(f"An error occurred during folder processing: {e}")

# 弹出文件夹选择窗口
def select_folder():
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    folder_path = filedialog.askdirectory()  # 打开文件夹选择对话框
    return folder_path

# 主函数
if __name__ == "__main__":
    folder_path = select_folder()  # 选择文件夹
    if folder_path:  # 如果选择了文件夹
        process_videos_in_folder(folder_path, interval=5)
    else:
        print("No folder selected.")
