"""
png_ico - PNG格式转ICO

Author: JiangHai
Date： 2023/5/11
"""

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Canvas
from tkinter import filedialog
from PIL import Image
from tkinter import messagebox
from pathlib import Path
import kayotin_main

# 初始化图片路径
img = ""
img_name = ""


def get_png():
    """
    获取图片位置然后用pillow打开
    :return:无
    """
    global img
    global img_name
    import_file_path = tk.filedialog.askopenfilename(filetypes=[("PNG File", '.png')])
    source_path = Path(import_file_path)
    if source_path.is_file():
        img = Image.open(source_path)
        img_name = source_path.name.split(".")[0]


def convert_to_ico():
    """
    将图片转换成ico格式并保存到用户指定位置
    :return:无
    """
    global img
    if img == "":
        tk.messagebox.showerror("Error", "请先选择文件")
    else:
        # initial file参数指定了保存的默认文件名
        export_file_path = tk.filedialog.asksaveasfilename(
            defaultextension='.ico', filetypes=[("ICO", ".ico")],
            initialfile=img_name
        )
        if export_file_path == "":
            return
        img.save(export_file_path)
        # 此处的警告是因为系统以为img还是一个空字符串
        tk.messagebox.showinfo("Success", "图片已转换并保存")


def back_main(root, canvas):
    canvas.destroy()
    kayotin_main.main(root)


def ico_main(src_root=None, src_canvas: Canvas = None):

    # 如果不存在root，那么新建一个
    if src_root:
        root = src_root
    else:
        root = ttk.Window()

    if src_canvas:
        src_canvas.destroy()

    width = 15
    root.title('PNG转换ICO')

    canvas_ico = ttk.Canvas(root, width=500, height=350, bg='white')
    canvas_ico.pack()
    # 窗口中的标题文字
    label1 = ttk.Label(root, text='PNG转ICO')
    label1.config(font=('helvetica', 20))
    canvas_ico.create_window(250, 100, window=label1)

    # 选择图片的按钮，注意button的第一个参数，指定他的parent，这里不指定的话会报错
    browse_button = ttk.Button(root, text="选择图片",
                               command=get_png, width=width, style="success outline button")
    canvas_ico.create_window(250, 150, window=browse_button)
    # 保存图片的按钮
    save_as_button = ttk.Button(root, text='开始转换',
                                command=convert_to_ico, width=width, style="success outline button")
    canvas_ico.create_window(250, 200, window=save_as_button)
    # 回到首页的按钮
    back_button = ttk.Button(root, text='返回首页',
                             command=lambda: back_main(root, canvas_ico),
                             width=width, style="success solid toolbutton")
    canvas_ico.create_window(250, 250, window=back_button)

    root.mainloop()


if __name__ == '__main__':
    ico_main()
