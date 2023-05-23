"""
file_sort - 界面化文件分类

Author: JiangHai江海
Date： 2023/5/23
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pathlib
from tkinter.filedialog import askdirectory


class FileSortTool(ttk.Frame):

    def __init__(self, master: ttk.Window, canvas=None):
        super().__init__(master, padding=15)
        self.pack(fill=BOTH, expand=YES)
        if canvas:
            canvas.destroy()
        master.title("文件整理工具")

        _path = pathlib.Path().absolute().as_posix()
        self.path_var = ttk.StringVar(value=_path)

        option_text = "请选择或输入文件夹路径，然后点击按钮开始整理"
        self.option_lf = ttk.Labelframe(self, text=option_text, padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)

        self.create_path_row()  # 创建路径选择那一行
        self.create_btn_row()  # 创建开始按钮那一行

    def create_path_row(self):
        """在labelframe中加入文件路径选择那一行"""
        path_row = ttk.Frame(self.option_lf)
        path_row.pack(fill=X, expand=YES)
        path_lbl = ttk.Label(path_row, text="文件夹路径", width=10)
        path_lbl.pack(side=LEFT, padx=(15, 0))
        path_ent = ttk.Entry(path_row, textvariable=self.path_var)
        path_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)
        browse_btn = ttk.Button(
            master=path_row,
            text="浏览",
            command=self.choose_path,
            width=8
        )
        browse_btn.pack(side=LEFT, padx=5)

    def choose_path(self):
        """选择文件路径"""
        path = askdirectory(title="选择文件路径")
        if path:
            self.path_var.set(path)

    def create_btn_row(self):
        type_row = ttk.Frame(self.option_lf)
        type_row.pack(fill=X, expand=YES, pady=5)
        back_button = ttk.Button(
            master=type_row,
            text="返回首页",
            command="",
            style="success solid toolbutton",
            width=8
        )
        back_button.pack(side=LEFT, padx=6)



if __name__ == '__main__':
    root = ttk.Window("文件分类工具", "journal")
    FileSortTool(root)
    root.mainloop()
