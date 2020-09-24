# This is a sample Python script.
"""
软工个人作业——论文相似度重复率计算程序
"""
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import re
import jieba
import numpy as np

def re_jieba_han(sel):
    """
    对目标文档进行读取
    采取结巴算法进行分词
    使用re函数筛除标点符号
    最后输出文档文字列表
    :param sel:
    :return:
    """
    open_sel = open(sel, 'r', encoding='utf-8')
    line = open_sel.readline()
    out_sel = []
    while line:
        line = line.strip()  # 去除空格
        seg_list = jieba.cut(line,cut_all=False)
        mid_sel = []
        for word in seg_list:
            mid_sel.append(word)
        for tag in mid_sel:
            if re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]", tag):
                out_sel.append(tag)
            else:
                pass
        line = open_sel.readline()
    return out_sel

def count(words):
    """
    统计关键词和词频
    对所得文档列表转化为字典
    :param words:
    :return:
    """
    t = {}
    for word in words:
        if word !="" and t.__contains__(word):
            num = t[word]
            t[word] = num+1
        elif word != "":
            t[word] = 1
    dic = sorted(t.items(),key=lambda t:t[1],reverse=True)
    return dic

def merge_word(T1,T2):
    """
    对两个文档字典进行关键词合并
    :param T1:
    :param T2:
    :return:
    """
    mergeWord = []
    duplicate_word = 0
    for ch in range(len(T1)):
        mergeWord.append(T1[ch][0])
    for ch in range(len(T2)):
        if T2[ch][0] in mergeWord:
            duplicate_word = duplicate_word + 1
        else:
            mergeWord.append(T2[ch][0])
    return mergeWord

def change(T1,mergeWord):
    """
    字典转化为向量
    :param T1:
    :param mergeWord:
    :return:
    """
    TF1 = [0] * len(mergeWord)
    for ch in range(len(T1)):
        TF = T1[ch][1]
        word = T1[ch][0]
        i = 0
        while i < len(mergeWord):
            if word == mergeWord[i]:
                TF1[i] = TF
                break
            else:
                i = i + 1
    return TF1

def cosine_similarity(x, y, norm=False):
    """
    计算余弦相似度
    :param x:
    :param y:
    :param norm:
    :return:
    """
    assert len(x) == len(y), "len(x) != len(y)"
    zero_list = [0] * len(x)
    if x == zero_list or y == zero_list:
        return float(1) if x == y else float(0)

    res = np.array([[x[i] * y[i], x[i] * x[i], y[i] * y[i]] for i in range(len(x))])
    cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))

    return 0.5 * cos + 0.5 if norm else cos

if __name__ == '__main__':
    #拆分句子
    rfile = count(re_jieba_han(sys.argv[1]))
    ffile = count(re_jieba_han(sys.argv[2]))
    mergeword = merge_word(rfile,ffile)
    #向量化
    r_vector = change(rfile,mergeword)
    f_vector = change(ffile,mergeword)
    result = cosine_similarity(r_vector,f_vector)
    result = np.float(result)
    result = round(result,2)
    file3 = open(sys.argv[3],"w")
    file3.write(str(result))
    file3.close()