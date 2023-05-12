"""
repeated_file - 查找重复文件

Author: JiangHai江海
Date： 2023/5/12
"""
from pathlib import Path
from filecmp import cmp


def rp_file():
    while True:
        folder = input("请输入文件夹的路径：\n")
        folder = Path(folder.strip())
        if folder.exists() and folder.is_dir():
            break
        else:
            print("输入的路径有误，请重新输入--->")
    src_path = folder
    save_path = Path(f"{src_path}/重复文件")
    if not save_path.exists():
        save_path.mkdir(parents=True)

    file_list = []
    result = list(src_path.rglob("*"))

    for file in result:
        if file.is_file():
            file_list.append(file)

    for file in file_list:
        for file_c in file_list:
            if file != file_c and file.exists() and file_c.exists():
                if cmp(file, file_c):
                    file_c.replace(save_path / file_c.name)
    print("已将重复文件移动到【重复文件】，请确认后删除")


if __name__ == '__main__':
    rp_file()
