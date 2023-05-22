"""
find_file - 查找文件,已废弃

Author: JiangHai江海
Date： 2023/5/12
"""

from pathlib import Path


def find_file():
    while True:
        folder = input("请输入搜索文件的路径：\n")
        folder = Path(folder.strip())
        if folder.exists() and folder.is_dir():
            break
        else:
            print("输入的路径有误，请重新输入--->")

    search = input("请输入文件或文件夹名称：")
    result = list(folder.rglob(f"*{search}*"))  # 查找子文件夹
    if not result:
        print(f"在{folder}下没有找到关键字是{search}的文件或文件夹。")
    else:
        result_folder = []
        result_file = []
        for file in result:
            if file.is_dir():
                result_folder.append(file)
            else:
                result_file.append(file)
        if result_folder:
            print(f"查找到包含关键字{search}的文件夹有{len(result_folder)}个：")
            for fd in result_folder:
                print(fd)
        if result_file:
            print(f"查找到包含关键字{search}的相关文件{len(result_file)}个：")
            for file_name in result_file:
                print(file_name)


if __name__ == '__main__':
    find_file()
