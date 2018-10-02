# -*- coding: utf-8 -*-
import pinyin


def toID(text):
    return pinyin.get(text, format='strip')


def toPY(text):
    return pinyin.get(text, delimiter=' ')


if __name__=='__main__':
    text = '中华'
    print(u'ID: {}\nPinyin: {}'.format(toID(text), toPY(text)))
