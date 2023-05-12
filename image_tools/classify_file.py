"""
classify_file - 文件根据后缀分类

Author: JiangHai江海
Date： 2023/5/12
"""
import os
import shutil
import glob
from pathlib import Path


def classify_file():
    while True:
        folder = input("请输入文件夹的路径：\n")
        folder = Path(folder.strip())
        if folder.exists() and folder.is_dir():
            break
        else:
            print("输入的路径有误，请重新输入--->")

    src_path = folder
    new_path = f"{folder}/分类文件夹"

    if not os.path.exists(new_path):
        os.mkdir(new_path)

    file_num = 0
    dir_num = 0

    for file in glob.glob(f"{src_path}/**/*", recursive=True):
        if os.path.isfile(file):
            filename = os.path.basename(file)
            if "." in filename:
                suffix = filename.split(".")[-1]
            else:
                suffix = "others"

            if not os.path.exists(f"{new_path}/{suffix}"):
                os.mkdir(f"{new_path}/{suffix}")
                dir_num += 1

            shutil.copy(file, f"{new_path}/{suffix}")
            file_num += 1
    print(f"整理完毕，一共整理了{file_num}个文件,共有{dir_num}种类型的文件，\n整理结果放在所选路径的【分类文件夹】下。")


if __name__ == '__main__':
    classify_file()