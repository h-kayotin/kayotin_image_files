"""
shopping_cart_analysis - 购物车关联分析

参考该链接：https://blog.csdn.net/weixin_46277779/article/details/128500463

Support（支持度）：表示某个项集出现的频率，也就是包含该项集的交易数与总交易数的比例。例如P(A)表示项集A的比例，P(A∩B)表示项集A和项集B同时出现的比例。
Confidence（置信度）：表示当A项出现时B项同时出现的频率，记作{A→B}。换言之，置信度指同时包含A项和B项的交易数与包含A项的交易数之比。公式表达：{A→B}的置信度=P(B∣A)=P(A∩B)/P(A)
Lift（提升度）：指A项和B项一同出现的频率，但同时要考虑这两项各自出现的频率。公式表达：{A→B}的提升度={A→B}的置信度/P(B)=P(B∣A)/P(B)=P(A∩B)/(P(A)∗P(B))
提升度反映了关联规则中的A与B的相关性，提升度>1且越高表明正相关性越高，提升度<1且越低表明负相关性越高，提升度=1表明没有相关性。负值，商品之间具有相互排斥的作用。


Author: hanayo
Date： 2024/1/10
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from apyori import apriori
import openpyxl

# 参数设置
pd.options.display.float_format = '{:,.4f}'.format
np.set_printoptions(precision=4)
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
test_file = "resource/400_data.xlsx"
data = pd.read_excel(test_file)

data['分词内容'] = data['分词内容'].apply(lambda x: x[1:].split(','))
data_list = list(data['分词内容'])


results = apriori(data_list, min_support=0.03, min_confidence=0.4)
workbook = openpyxl.Workbook()
worksheet = workbook.active
worksheet.title = "关联性"
worksheet.append(('相关类别', '支持度', '置信度', '提升度'))
for res in results:
    support = round(res.support, 3)
    for rule in res.ordered_statistics:
        head_set = list(rule.items_base)
        tail_set = list(rule.items_add)
        # 跳过前件为空的数据
        if not head_set:
            continue
        related_content = str(head_set) + '→' + str(tail_set)
        # 提取置信度，并保留3位小数
        confidence = round(rule.confidence, 3)
        # 提取提升度，并保留3位小数
        lift = round(rule.lift, 3)
        worksheet.append((related_content, support, confidence, lift))
workbook.save("output/关联性分析.xlsx")






