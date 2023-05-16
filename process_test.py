"""
process_test - 

Author: JiangHai江海
Date： 2023/5/12
"""

from tkinter import *

windows = Tk()
windows.geometry("200x200")


def b():
    windows.destroy() #关掉之前的窗口
    root = Tk()
    Label(root,text="这是新的窗口").pack()
    root.focus_force() #新窗口获得焦点
    root.mainloop()


Button(windows, text="打开一个新窗口", command=b).pack(pady=50)
windows.mainloop()
