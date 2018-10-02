# coding=utf-8

from word_count import WordCount
from lookup import lookup


FLAG_LAST_WORD = 1
FLAG_MIDDLE_WORD = 2

wc = WordCount()


def word_topk(k, flag):
    if flag == FLAG_LAST_WORD:
        return wc.last_word_topk(k)
    if flag == FLAG_MIDDLE_WORD:
        return wc.middle_word_topk(k)
    return []


def word_freq(word, flag):
    """返回常见系数、级别"""
    if flag == FLAG_LAST_WORD:
        ret = wc.last_word_freq(word)
    else:
        ret = wc.middle_word_freq(word)

    freq, rank, total = ret
    # 1/4 -- 2/4 -- 3/4 -- 1
    if rank <= total/4:
        comment = u'大众名'
    elif rank <= total/2:
        comment = u'普通名'
    elif rank <= (total*3)/4:
        comment = u'稀有名'
    else:
        comment = u'罕见名'
    # print(ret, comment)
    return [freq, comment]
