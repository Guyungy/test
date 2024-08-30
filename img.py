import os
import shutil
from transformers import pipeline
from PIL import Image
from tkinter import Tk
from tkinter import filedialog

# 使用pipeline进行高层次的图片分类
def classify_image_pipeline(image_path, pipe):
    # 打开本地图片
    image = Image.open(image_path)
    
    # 进行分类
    results = pipe(image)
    
    # 返回预测的标签
    return results[0]['label']

# 处理图片并将其分类归类
def process_images_in_folder(folder_path):
    # 初始化pipeline
    pipe = pipeline("image-classification", model="MichalMlodawski/nsfw-image-detection-large")
    
    # 遍历文件夹中的所有图片文件
    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        
        # 检查是否为图片文件
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            continue
        
        # 分类图片
        label = classify_image_pipeline(image_path, pipe)
        
        # 创建目标文件夹路径
        target_folder = os.path.join(folder_path, label)
        
        # 如果目标文件夹不存在，创建它
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        
        # 移动图片到相应的分类文件夹
        target_path = os.path.join(target_folder, filename)
        shutil.move(image_path, target_path)
        print(f"Moved {filename} to {target_folder}")

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
        process_images_in_folder(folder_path)
    else:
        print("No folder selected.")
