"""
kayotin_main - 主程序

Author: JiangHai江海
Date： 2023/5/11
"""

import image_tools
import ttkbootstrap as ttk


def main():
    root_main = ttk.Window(themename="lumen")
    width = 15
    root_main.title("工具箱")

    # 新建画布
    canvas_main = ttk.Canvas(root_main, width=500, height=450, bg='white')
    canvas_main.pack()
    label1 = ttk.Label(root_main, text='工具箱')
    label1.config(font=('helvetica', 20))
    canvas_main.create_window(250, 100, window=label1)

    # 第一个功能：转换成ICO
    func1_button = ttk.Button(root_main, text="PNG转ICO", command=image_tools.png_ico.ico_main,
                              width=width, style="success outline button")
    canvas_main.create_window(250, 150, window=func1_button)

    # 第二个功能：jpg转png
    func2_button = ttk.Button(root_main, text="JPG转png", command=image_tools.jpg_png.to_png,
                              width=width, style="info outline button")
    canvas_main.create_window(250, 200, window=func2_button)

    # 第三个功能：查找文件
    func3_button = ttk.Button(root_main, text="查找文件", command=image_tools.find_file.find_file,
                              width=width, style="success solid toolbutton")
    canvas_main.create_window(250, 250, window=func3_button)

    # 第四个功能：分类文件
    func4_button = ttk.Button(root_main, text="文件分类", command=image_tools.classify_file.classify_file,
                              width=width, style="info outline button")
    canvas_main.create_window(250, 300, window=func4_button)

    # 第五个功能：查找重复文件
    func4_button = ttk.Button(root_main, text="查找重复文件", command=image_tools.repeated_file.rp_file,
                              width=width, style="success outline button")
    canvas_main.create_window(250, 350, window=func4_button)

    root_main.mainloop()


if __name__ == '__main__':
    main()
