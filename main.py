# This is a sample Python script.
"""
软工个人作业——论文相似度重复率计算程序
"""
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import jieba
import re


# 分词
def re_jieba_han(str):
    openStr = open(str, 'r', encoding='utf-8')
    line = openStr.readline()
    outStr = []
    while line:
        line = line.strip()  # 去除空格
        seg_list = jieba.cut(line,cut_all=False)
        midStr = []
        for word in seg_list:
            midStr.append(word)
        #print(midStr)
        for tag in midStr:
            if re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]", tag):
                outStr.append(tag)
            else:
                pass
        line = openStr.readline()
    return outStr

#统计关键词和词频
def count(words):
    t = {}
    for word in words:
        if word !="" and t.__contains__(word):
            num = t[word]
            t[word] = num+1
        elif word != "":
            t[word] = 1
    dic = sorted(t.items(),key=lambda t:t[1],reverse=True)
    return dic

def mergeWord(T1,T2):
    mergeWord = []
    duplicateWord = 0
    for ch in range(len(T1)):
        mergeWord.append(T1[ch][0])
    for ch in range(len(T2)):
        if T2[ch][0] in mergeWord:
            duplicateWord = duplicateWord + 1
        else:
            mergeWord.append(T2[ch][0])
    return mergeWord

#文档转化向量
def change(T1,mergeWord):
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


#计算相似度
import numpy as np
def cosine_similarity(x, y, norm=False):
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
    mergeword = mergeWord(rfile,ffile)
    #向量化
    r_vector = change(rfile,mergeword)
    f_vector = change(ffile,mergeword)
    result = cosine_similarity(r_vector,f_vector)
    result = np.float(result)
    result = round(result,3)
    file3 = open(sys.argv[3],"w")
    file3.write(str(result))
    file3.close()