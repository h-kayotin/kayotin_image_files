"""
jpg_png - 图片转换主程序

Author: JiangHai江海
Date： 2023/5/11
"""

from pathlib import Path
from PIL import Image
import ttkbootstrap as ttk
import tkinter
from tkinter import filedialog, messagebox
from ttkbootstrap import Canvas
from image_tools.png_ico import back_main

file_path = ""


def get_dir():
    global file_path
    file_path = tkinter.filedialog.askdirectory()


def to_png():
    global file_path
    src_folder = file_path
    save_folder = "./已转换格式"
    if file_path == "":
        tkinter.messagebox.showerror("Error", "请先选择源文件夹")
        return

    src_folder = Path(src_folder)
    save_folder = Path(save_folder)

    if not save_folder.exists():
        save_folder.mkdir(parents=True)

    file_list = list(src_folder.glob("*.jpg"))

    for file in file_list:
        done_file = save_folder / file.name
        done_file = done_file.with_suffix(".png")
        Image.open(file).save(done_file)
    tkinter.messagebox.showinfo("Success", "图片已转换并保存")


def init_interface(src_root=None, src_canvas: Canvas = None):
    # 如果不存在root，那么新建一个
    if src_root:
        root = src_root
    else:
        root = ttk.Window()
    # 如果是从首页跳转来的，清除原先的画布
    if src_canvas:
        src_canvas.destroy()

    # 按钮宽度
    width = 15
    root.title('jpg转png')
    # 新建一个画布
    canvas_png = ttk.Canvas(root, width=500, height=350, bg='white')
    canvas_png.pack()
    # 标题label
    label1 = ttk.Label(root, text='JPG转PNG')
    label1.config(font=('微软雅黑', 20))
    canvas_png.create_window(250, 100, window=label1)

    # 选择文件路径的按钮
    browse_button = ttk.Button(root, text="选择图片路径",
                               command=get_dir, width=width, style="success outline")
    browse_button.bind("")
    canvas_png.create_window(250, 150, window=browse_button)

    # 开始转换的按钮
    browse_button = ttk.Button(root, text="开始转换",
                               command=to_png, width=width, style="success-outline")
    canvas_png.create_window(250, 200, window=browse_button)

    # 返回首页的按钮
    browse_button = ttk.Button(root, text="返回首页",
                               command=lambda: back_main(root, canvas_png),
                               width=width, style="success-solid-toolbutton")
    canvas_png.create_window(250, 250, window=browse_button)

    root.mainloop()


if __name__ == '__main__':
    init_interface()
