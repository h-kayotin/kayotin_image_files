"""
jpg_png - 

Author: JiangHai江海
Date： 2023/5/11
"""

from pathlib import Path
from PIL import Image


def to_png():
    src_folder = input("请输入图片文件夹：")
    dest_folder = "./已转换格式"

    src_folder = Path(src_folder)
    dest_folder = Path(dest_folder)

    if not dest_folder.exists():
        dest_folder.mkdir(parents=True)

    file_list = list(src_folder.glob("*.jpg"))

    for file in file_list:
        dest_file = dest_folder / file.name
        dest_file = dest_file.with_suffix(".png")
        Image.open(file).save(dest_file)
        print(f"{file.name}转换完成")
