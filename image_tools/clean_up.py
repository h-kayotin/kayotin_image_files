"""
clean_up - 查找重复文件的界面化

Author: JiangHai江海
Date： 2023/5/23
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pathlib
from tkinter.filedialog import askdirectory
import kayotin_main
from filecmp import cmp


class FileCleanTool(ttk.Frame):

    def __init__(self, master: ttk.Window, canvas=None):
        super().__init__(master, padding=15)
        self.pack(fill=BOTH, expand=YES)
        if canvas:
            canvas.destroy()
        master.title("文件清理工具")

        _path = pathlib.Path().absolute().as_posix()
        self.path_var = ttk.StringVar(value=_path)

        option_text = "请选择或输入文件夹路径，然后点击按钮开始整理重复文件"
        self.option_lf = ttk.Labelframe(self, text=option_text, padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)

        output_text = "运行结果如下所示"
        self.output = ttk.Labelframe(self, text=output_text, padding=15)
        self.output.pack(fill=X, expand=YES, anchor=N, pady=10)

        self.create_path_row()  # 创建路径选择那一行
        self.create_btn_row()  # 创建开始按钮那一行
        self.output_text = ttk.StringVar()
        self.create_output()  # 创建结果那一行

    def create_path_row(self):
        """在labelframe中加入文件路径选择那一行"""
        path_row = ttk.Frame(self.option_lf)
        path_row.pack(fill=X, expand=YES)
        path_lbl = ttk.Label(path_row, text="文件夹路径", width=10)
        path_lbl.pack(side=LEFT, padx=(15, 0))
        path_ent = ttk.Entry(path_row, textvariable=self.path_var, width=50)
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
        """创建按钮这一行"""
        btn_row = ttk.Frame(self.option_lf)
        btn_row.pack(fill=X, expand=YES, pady=15)
        # 这个label用来占位，主要是为了后面按钮的对齐
        path_lbl = ttk.Label(btn_row, text="", width=10)
        path_lbl.pack(side=LEFT, padx=(15, 0))
        # 第一个按钮
        back_button = ttk.Button(
            master=btn_row,
            text="返回首页",
            command=self.back_2_main,
            style="success solid toolbutton",
            width=8
        )
        back_button.pack(side=LEFT, padx=5)

        # 这个label用来站位，主要是为了后面按钮的对齐
        path_lbl2 = ttk.Label(btn_row, text="", width=50)
        path_lbl2.pack(side=LEFT, padx=(15, 0))
        # 第二个按钮
        st_button = ttk.Button(
            master=btn_row,
            text="开始整理",
            command=self.do_work,
            style=OUTLINE,
            width=8
        )
        st_button.pack(side=LEFT, padx=5)

    def back_2_main(self):
        for child in self.master.winfo_children():
            child.destroy()
        kayotin_main.main(self.master)

    def create_output(self):
        """新建结果那一行"""
        output_lb0 = ttk.Label(self.output, text="", width=10)
        output_lb0.pack(side=LEFT, padx=(15, 0))
        output_lb = ttk.Label(self.output,
                              textvariable=self.output_text,
                              width=50, style=INFO
                              )
        output_lb.pack(side=LEFT, padx=5)

    def do_work(self):
        str_path = self.path_var.get()
        src_path = pathlib.Path(str_path)
        # 整理后放在new_path下，如果没有该文件夹就新建一个
        new_path = pathlib.Path(f"{src_path}/重复文件")
        if not new_path.exists():
            pathlib.Path.mkdir(new_path)
        file_num = 0

        file_list = []
        result = list(src_path.rglob("*"))
        for file in result:
            if file.is_file():
                file_list.append(file)

        for file in file_list:
            for file_c in file_list:
                if file != file_c and file.exists() and file_c.exists():
                    if cmp(file, file_c):
                        file_c.replace(new_path / file_c.name)
                        file_num += 1

        self.output_text.set(f"整理完毕，一共发现了{file_num}个重复文件,"
                             f"\n放在所选路径的【重复文件】下，请确认后进行删除。")


if __name__ == '__main__':
    root = ttk.Window("文件分类工具", "journal")
    FileCleanTool(root)
    root.mainloop()
