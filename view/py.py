# coding=utf-8
import pinyin
import unicodedata


BJXFile = 'data/bjx.data'
BJX = {}


def initOnce():
    def load(f, d):
        lines = open(f).readlines()
        for row in lines:
            cols = [e.strip() for e in row.split(':')]
            if len(cols) == 2:
                d[cols[0]] = unicode(cols[1], 'utf-8').strip()

    if len(BJX) == 0:
        load(BJXFile, BJX)


def tone2ID(s):
    # s = 'Lǐ Zhōu Wú'
    return unicodedata.normalize('NFKD', s).encode('ascii','ignore')


def splitName(name):
    # 2种可能：单姓、复姓
    name = unicode(name, 'utf-8')
    xing = name[0]
    ming = name[1:]
    if len(name) > 2 and name[:2] in BJX:
        xing = name[:2]
        ming = name[2:]
    return xing.encode('utf-8'), ming.encode('utf-8')


def toID(text):
    initOnce()
    xing, ming = splitName(text)
    if xing not in BJX:
        return pinyin.get(text, format='strip')
    return ''.join([tone2ID(BJX.get(xing)), pinyin.get(ming, format='strip')])


def toPY(text):
    initOnce()
    xing, ming = splitName(text)
    if xing not in BJX:
        return pinyin.get(text, delimiter=' ')
    return ' '.join([BJX.get(xing), pinyin.get(ming, delimiter=' ')])


if __name__ == '__main__':
    text = '中华'
    print(u'ID: {}\nPinyin: {}'.format(toID(text), toPY(text)))
