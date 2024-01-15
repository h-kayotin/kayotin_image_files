"""
pku_sub_words - https://github.com/fuqiuai/wordCloud/blob/master/chnSegment.py
停用词，一般的做法是，读取停用词，然后分词后做处理

Author: hanayo
Date： 2024/1/11
"""
from collections import Counter
from os import path
import jieba
import word_cloud

# 导入用户自定义词典
jieba.load_userdict(path.join(path.dirname(__file__), 'resource/user_dict.txt'))
test_text = "我今天很开心，使用了可悠然产品。"


def word_test(text):
    words = jieba.cut(text, cut_all=False)
    for word in words:
        print(word)
    word_list = jieba.lcut(text)
    print(word_list)


def word_segment(text):
    """
    通过jieba进行分词并通过空格分隔,返回分词后的结果
    """

    # 计算每个词出现的频率，并存入txt文件
    words_list = jieba.lcut(text, cut_all=False)
    # cut_all是分词模式，True是全模式，False是精准模式，默认False
    data_dict = Counter(words_list)
    with open('doc//词频统计.txt', 'w') as fw:
        for k, v in data_dict.items():
            fw.write("%s,%d\n" % (k, v))

    # 返回分词后的结果，用空格分隔
    jieba_word = jieba.cut(text, cut_all=False)
    seg_list = ' '.join(jieba_word)
    return seg_list


if __name__ == '__main__':
    word_test(test_text)

    # 读取文件
    d = path.dirname(__file__)
    text = open(path.join(d, 'doc//十九大报告全文.txt'), encoding="utf-8").read()
    # text = open(path.join(d, 'doc//alice.txt')).read()

    # 若是中文文本，则先进行分词操作
    text = word_segment(text)

    # 生成词云
    word_cloud.generate_wordcloud(text)
