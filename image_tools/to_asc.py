"""
to_asc - 将ico图标保存为二进制数据，保存在icon.py中

Author: hanayo
Date： 2023/6/26
"""

import base64

icon_path = input("输入图标完整路径：")
open_icon = open(icon_path, "rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = "img = %s" % b64str
f = open("icon.py", "w+")
f.write(write_data)
f.close()
