"""
kayotin_main - 主程序

Author: JiangHai江海
Date： 2023/5/11
"""

import image_tools
import tkinter
from tkinter import filedialog
from tkinter import messagebox

do_somethings = {
    "1": "转换图片，done",
    "2": "查询文件",
    "3": "清理C盘",
    "4": "转ICO，done"

}


def main():
    # 创建TK对象
    root_main = tkinter.Tk()
    font = ('helvetica', 12, 'bold')
    bg = 'grey'
    fg = 'white'
    width = 15

    # 用画布创建窗口对象
    root_main.title("工具箱")
    canvas_main = tkinter.Canvas(root_main, width=500, height=350, bg='white')
    canvas_main.pack()
    label1 = tkinter.Label(root_main, text='工具箱', bg='white')
    label1.config(font=('helvetica', 20))
    canvas_main.create_window(250, 100, window=label1)

    # 第一个功能：转换成ICO
    func1_button = tkinter.Button(root_main, text="PNG转ICO", command=image_tools.png_ico.ico_main,
                                  bg=bg, fg=fg, font=font, width=width)
    canvas_main.create_window(250, 150, window=func1_button)

    # 第二个功能：jpg转png
    func2_button = tkinter.Button(root_main, text="JPG转png", command=image_tools.jpg_png.to_png,
                                  bg=bg, fg=fg, font=font, width=width)
    canvas_main.create_window(250, 200, window=func2_button)

    root_main.mainloop()


if __name__ == '__main__':
    main()

