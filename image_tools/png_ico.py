"""
png_ico - PNG格式转ICO

Author: JiangHai
Date： 2023/5/11
"""

import tkinter as tk
from tkinter import filedialog
from PIL import Image
from tkinter import messagebox
from pathlib import Path

# 初始化图片路径
img = ""


def get_png():
    """
    获取图片位置然后用pillow打开
    :return:无
    """
    global img
    import_file_path = tk.filedialog.askopenfilename(filetypes=[("PNG File", '.png')])
    source_path = Path(import_file_path)
    if source_path.is_file():
        img = Image.open(source_path)


def convert_to_ico():
    """
    将图片转换成ico格式并保存到用户指定位置
    :return:无
    """
    global img
    if img == "":
        tk.messagebox.showerror("Error", "请先选择文件")
    else:
        export_file_path = tk.filedialog.asksaveasfilename(defaultextension='.ico', filetypes=[("ICO", ".ico")])
        if export_file_path == "":
            return
        img.save(export_file_path)
        # 此处的警告是因为系统以为img还是一个空字符串
        tk.messagebox.showinfo("Success", "图片已转换并保存")


def ico_main():
    # 新建一个窗口
    root = tk.Tk()

    # 初始化按钮的字体，背景颜色和宽度
    font = ('helvetica', 12, 'bold')
    bg = 'blue'
    fg = 'white'
    width = 15

    # 窗口标题
    root.title('PNG转换ICO')
    canvas1 = tk.Canvas(root, width=500, height=350, bg='lightblue')
    canvas1.pack()
    # 窗口中的标题文字
    label1 = tk.Label(root, text='PNG转ICO', bg='lightblue')
    label1.config(font=('helvetica', 20))
    canvas1.create_window(250, 100, window=label1)
    # 选择图片的按钮，注意button的第一个参数，指定他的parent，这里不指定的话会报错
    browse_button = tk.Button(root, text="选择图片", command=get_png, bg=bg, fg=fg, font=font, width=width)
    canvas1.create_window(250, 150, window=browse_button)
    # 保存图片的按钮
    save_as_button = tk.Button(root, text='开始转换', command=convert_to_ico, bg=bg, fg=fg, font=font, width=width)
    canvas1.create_window(250, 200, window=save_as_button)
    root.mainloop()


if __name__ == '__main__':
    ico_main()
