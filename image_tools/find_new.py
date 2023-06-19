import datetime
import pathlib
import os
from queue import Queue
from threading import Thread
from tkinter.filedialog import askdirectory
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import utility
import kayotin_main


class FileSearchEngine(ttk.Frame):

    queue = Queue()
    searching = False

    def __init__(self, master: ttk.Window, canvas=None):
        # super用来调用父类的方法，如果需要新增属性，就要用super来继承原有的属性
        super().__init__(master, padding=15)
        self.result_view = None
        self.pack(fill=BOTH, expand=YES)
        if canvas:
            canvas.destroy()
        master.title("文件查找工具")

        # 这里是绝对路径，/分隔，默认是当前路径
        _path = pathlib.Path().absolute().as_posix()
        self.path_var = ttk.StringVar(value=_path)  # 默认路径填写在文件夹路径中
        self.term_var = ttk.StringVar(value='')  # 默认关键字，为空
        self.type_var = ttk.StringVar(value='contains')  # 默认搜索模式，contains

        # 创建顶部的Labelframe块
        option_text = "请选择或输入文件夹路径，输入关键词开始搜索"
        self.option_lf = ttk.Labelframe(self, text=option_text, padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)

        self.create_path_row()  # 创建路径那一行
        self.create_term_row()  # 创建选择关键字那一行
        self.create_type_row()  # 创建选择搜索类型那一行
        self.create_results_view()  # 创建搜索结果显示的块

        # 创建进度条
        self.progressbar = ttk.Progressbar(
            master=self, 
            mode=INDETERMINATE, 
            style="striped-success"
        )
        self.progressbar.pack(fill=X, expand=YES)

    def create_path_row(self):
        """在labelframe中加入文件路径选择那一行"""
        path_row = ttk.Frame(self.option_lf)
        path_row.pack(fill=X, expand=YES)
        path_lbl = ttk.Label(path_row, text="文件夹路径", width=10)  # label 文件夹路径
        path_lbl.pack(side=LEFT, padx=(15, 0))
        path_ent = ttk.Entry(path_row, textvariable=self.path_var)  # 输入框
        path_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)
        browse_btn = ttk.Button(      # 浏览按钮
            master=path_row, 
            text="浏览",
            command=self.on_browse,   # 绑定方法，获取路径
            width=8
        )
        browse_btn.pack(side=LEFT, padx=5)

    def create_term_row(self):
        """在labelframe中加入关键字行"""
        term_row = ttk.Frame(self.option_lf)
        term_row.pack(fill=X, expand=YES, pady=15)
        term_lbl = ttk.Label(term_row, text="关键字", width=10)
        term_lbl.pack(side=LEFT, padx=(15, 0))
        term_ent = ttk.Entry(term_row, textvariable=self.term_var)
        term_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)
        search_btn = ttk.Button(
            master=term_row, 
            text="开始搜索",
            command=self.on_search, 
            style=OUTLINE,
            width=8
        )
        search_btn.pack(side=LEFT, padx=5)

    def create_type_row(self):
        """在labelframe创建类型选择行"""
        type_row = ttk.Frame(self.option_lf)
        type_row.pack(fill=X, expand=YES)
        type_lbl = ttk.Label(type_row, text="搜索类型", width=10)
        type_lbl.pack(side=LEFT, padx=(15, 0))

        contains_opt = ttk.Radiobutton(
            master=type_row, 
            text="包含",
            variable=self.type_var, 
            value="contains"
        )
        contains_opt.pack(side=LEFT)
        contains_opt.invoke()

        endswith_opt = ttk.Radiobutton(
            master=type_row, 
            text="后缀名",
            variable=self.type_var, 
            value="endswith"
        )
        endswith_opt.pack(side=LEFT, padx=15)

        back_button = ttk.Button(
            master=type_row,
            text="返回首页",
            command=self.back_2_main,
            style="success solid toolbutton",
            width=8
        )
        back_button.pack(side=RIGHT, padx=6)

    def create_results_view(self):
        """初始化搜索结果界面"""
        self.result_view = ttk.Treeview(
            master=self,
            style="info",
            columns=["#0", "#1", "#2", "#3", "#4"],  # 列表长度代表列数
            show=HEADINGS
        )
        self.result_view.pack(fill=BOTH, expand=YES, pady=10)

        # setup columns and use `scale_size` to adjust for resolution
        # 初始化列标题，用scale_size去调整列宽
        self.result_view.heading(0, text='文件名', anchor=W)
        self.result_view.heading(1, text='最后修改时间', anchor=W)
        self.result_view.heading(2, text='文件类型', anchor=E)
        self.result_view.heading(3, text='大小', anchor=E)
        self.result_view.heading(4, text='路径', anchor=W)
        self.result_view.column(
            column=0, 
            anchor=W, 
            width=utility.scale_size(self, 125), 
            stretch=True
        )
        self.result_view.column(
            column=1, 
            anchor=W, 
            width=utility.scale_size(self, 140), 
            stretch=False
        )
        self.result_view.column(
            column=2, 
            anchor=E, 
            width=utility.scale_size(self, 70),
            stretch=False
        )
        self.result_view.column(
            column=3, 
            anchor=E, 
            width=utility.scale_size(self, 50), 
            stretch=False
        )
        self.result_view.column(
            column=4, 
            anchor=W, 
            width=utility.scale_size(self, 300)
        )

    def on_browse(self):
        """选择文件路径"""
        path = askdirectory(title="选择文件路径")
        if path:
            self.path_var.set(path)

    def on_search(self):
        """根据文件类型进行搜索"""
        # 下次搜索前，先清除之前的结果
        items = self.result_view.get_children()
        for item in items:
            self.result_view.delete(item)

        search_term = self.term_var.get()  # 关键字
        search_path = self.path_var.get()  # 路径
        search_type = self.type_var.get()  # 搜索类型

        if search_term == '':  # 如果关键字为空
            return

        # start search in another thread to prevent UI from locking
        # 新建一个线程来进行搜索
        Thread(
            target=FileSearchEngine.file_search, 
            args=(search_term, search_path, search_type), 
            daemon=True
        ).start()
        self.progressbar.start(10)  # 进度条滚动

        iid = self.result_view.insert(
            # 插入在根进节点，插入在最后
            parent='',
            index=END, 
        )
        self.result_view.item(iid, open=True)
        # 100ms后执行检查队列
        self.after(100, lambda: self.check_queue(iid))

    def back_2_main(self):
        for child in self.master.winfo_children():
            child.destroy()
        kayotin_main.main(self.master)

    def check_queue(self, iid):  # 这个方法还要研究下
        """检查队列，然后进行显示"""
        if all([
            FileSearchEngine.searching,  # 在搜索中
            not FileSearchEngine.queue.empty()  # 并且队列不为空
        ]):
            filename = FileSearchEngine.queue.get()
            self.insert_row(filename, iid)
            self.update_idletasks()
            self.after(100, lambda: self.check_queue(iid))
        elif all([
            not FileSearchEngine.searching,  # 搜索已结束
            not FileSearchEngine.queue.empty()  # 但队列不为空
        ]):
            # 当队列不为空，就反复的插入新的行
            while not FileSearchEngine.queue.empty():
                filename = FileSearchEngine.queue.get()
                self.insert_row(filename, iid)
            self.update_idletasks()  # 该方法是为了避免tk在处理一个长时间任务时可能出现的卡顿
            self.progressbar.stop()
        elif all([
            FileSearchEngine.searching,  # 在搜索中，且队列为空
            FileSearchEngine.queue.empty()
        ]):
            # 这种情况下，稍等0.1s再来检查队列
            self.after(100, lambda: self.check_queue(iid))
        else:
            self.progressbar.stop()

    def insert_row(self, file, iid):
        """在搜索结果中插入一行"""
        try:
            _stats = file.stat()  # 文件状态信息
            _name = file.stem   #
            # st_mtime实际上是最后访问时间
            _timestamp = datetime.datetime.fromtimestamp(_stats.st_mtime)
            _modified = _timestamp.strftime(r'%Y/%m/%d %H:%M')
            _type = file.suffix.lower()  # 文件类型
            if file.is_dir():
                _type = "dir"
                _name = "文件夹"
            _size = FileSearchEngine.convert_size(_stats.st_size)
            _path = file.as_posix()
            iid = self.result_view.insert(
                parent='', 
                index=END, 
                values=(_name, _modified, _type, _size, _path)
            )
            self.result_view.selection_set(iid)  # 选择这一行，这样每次都选择最后一行
            self.result_view.see(iid)  # see方法用来滚动使所选的行可见
        except OSError:
            return

    @staticmethod  # 静态方法表示不和类相关的方法
    def file_search(term, search_path, search_type):
        """根据搜索类型分别调用方法进行搜索"""
        FileSearchEngine.set_searching(True)  # 这个参数表示搜索在进行中
        if search_type == 'contains':
            FileSearchEngine.find_contains(term, search_path)  # 执行搜索的主方法
        elif search_type == 'endswith':
            FileSearchEngine.find_endswith(term, search_path)

    @staticmethod
    def find_contains(term, search_path):
        """关键字搜索"""
        src_path = pathlib.Path(search_path)
        result = list(src_path.rglob(f"*{term}*"))
        for file in result:
            FileSearchEngine.queue.put(file)  # 将搜索结果放到队列中
        FileSearchEngine.set_searching(False)  # 将状态设置为结束

    @staticmethod
    def find_endswith(term, search_path):
        """根据后缀名搜索"""
        for path, _, files in os.walk(search_path):
            if files:
                for file in files:
                    if file.endswith(term):
                        record = pathlib.Path(path) / file
                        FileSearchEngine.queue.put(record)
        FileSearchEngine.set_searching(False)

    @staticmethod
    def set_searching(state=False):
        """设定搜索的状态"""
        FileSearchEngine.searching = state

    @staticmethod
    def convert_size(size):
        """Convert bytes to mb or kb depending on scale"""
        kb = size // 1000
        mb = round(kb / 1000, 1)
        if kb > 1000:
            return f'{mb:,.1f} MB'
        else:
            return f'{kb:,d} KB'        


if __name__ == '__main__':

    app = ttk.Window("文件搜索工具", "journal")
    FileSearchEngine(app)
    app.mainloop()
