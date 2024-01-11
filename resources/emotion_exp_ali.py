"""
emotion_exp - NLP

https://help.aliyun.com/document_detail/179345.html

免费额度：每个模型每天50w次免费额度
免费额度消耗完将按量计费，计费方式：0.0016元/次
限制每秒20次请求

1 分词 https://help.aliyun.com/document_detail/177236.html?spm=a2c4g.176652.0.i0#topic-2139758
2 情感分析 https://help.aliyun.com/document_detail/179345.html?spm=a2c4g.179344.0.i0

需要以下三个库
pip install aliyun-python-sdk-core
pip install aliyun-python-sdk-alinlp==1.0.20
pip install openpyxl

Author: hanayo
Date： 2024/1/8
"""

# 分词模块的actionName：GetWsCustomizedChGeneralRequest
from aliyunsdkalinlp.request.v20200629 import GetWsCustomizedChGeneralRequest
# 情感分析模块
from aliyunsdkalinlp.request.v20200629 import GetSaChGeneralRequest
# 验证模块
from aliyunsdkcore.client import AcsClient
# 处理报错可能用到的模块
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException

from config import access_key_id, access_key_secret
import json
import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
from time import sleep


client = AcsClient(access_key_id, access_key_secret, "cn-hangzhou")
test_messages = "这个可悠然产品很不错，下次还会继续购买"
junk_words = {'，', '。', '：', '、', '（', '）', '是', '的', '在', ' ', '了'}


def split_word(txt):
    request = GetWsCustomizedChGeneralRequest.GetWsCustomizedChGeneralRequest()
    request.set_ServiceCode("alinlp")
    request.set_Text(txt)

    response = client.do_action_with_exception(request)
    resp_obj = json.loads(response)
    data_dict = json.loads(resp_obj['Data'])
    res = ""
    for word in data_dict['result']:
        if word['word'] not in junk_words:
            res += f",{word['word']}"
    return res


def emo_ana(txt):
    request = GetSaChGeneralRequest.GetSaChGeneralRequest()
    request.set_Text(txt)
    request.set_ServiceCode("alinlp")
    response = client.do_action_with_exception(request)
    resp_obj = json.loads(response)
    data_dict = json.loads(resp_obj['Data'])
    # print(data_dict)
    # print(data_dict['result']['sentiment'])
    return data_dict['result']['sentiment']


def read_excel(filename):
    workbook = openpyxl.load_workbook(filename)  # type:Workbook
    worksheet = workbook.worksheets[0]  # type: Worksheet

    for row_idx in range(2, worksheet.max_row + 1):
        if worksheet[f"L{row_idx}"].value:
            cell_val = worksheet[f"L{row_idx}"].value.strip()
            sleep(0.05)
            worksheet[f"R{row_idx}"].value = emo_ana(cell_val)
            worksheet[f"S{row_idx}"].value = split_word(cell_val)
    worksheet[f"R1"].value = "情感分析"
    worksheet[f"S1"].value = "分词内容"
    workbook.save(filename)


if __name__ == '__main__':
    # split_word(test_messages)
    # emo_ana(test_messages)
    read_excel("resource/400_data.xlsx")
