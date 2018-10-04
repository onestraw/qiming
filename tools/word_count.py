# coding=utf-8

import os
import json
import codecs
import operator


class WordCount(object):
    NameCorpusTxt = 'data/chinese_names_corpus.txt'
    NameLastTxt = 'data/last.txt'
    NameLastJson = 'data/last_json.json'
    NameMiddleTxt = 'data/middle.txt'
    NameMiddleJson = 'data/middle_json.json'

    def __init__(self):
        if not os.path.exists(self.NameLastTxt) or\
           not os.path.exists(self.NameMiddleTxt) or\
           not os.path.exists(self.NameLastJson) or \
           not os.path.exists(self.NameMiddleJson):
            self.count()

    def inc(self, hmap, key):
        if key not in hmap:
            hmap[key] = 0
        hmap[key] += 1

    def output(self, hmap, tofile):
        sorted_hmap = sorted(hmap.items(), key=operator.itemgetter(1),
                             reverse=True)
        try:
            f = codecs.open(tofile, 'w+', 'utf-8')
            for k, v in sorted_hmap:
                f.write(u'{}: {}\n'.format(k, v))
            f.close()
        except Exception as e:
            print(e.message)
            for k, v in sorted_hmap:
                print(u'{}: {}'.format(k, v))
        return sorted_hmap

    def output_json(self, hmap, tofile):
        total = 0
        for _, v in hmap.iteritems():
            total += v[0]
        f = codecs.open(tofile, 'w+', 'utf-8')
        hmap['total'] = total
        f.write(json.dumps(hmap))
        f.close()

    def save(self, hmap, toTxt, toJson):
        sorted_hmap = self.output(hmap, toTxt)
        for i, v in enumerate(sorted_hmap):
            word, count = v
            # 保存频次、名次
            hmap[word] = [count, i]
        self.output_json(hmap, toJson)

    def count(self):
        f = open(self.NameCorpusTxt)
        rows = f.readlines()
        f.close()
        # 最后一个字的次数
        last = {}
        # 如果名字长度>=3，倒数第二个字的次数，不考虑复姓长度3
        middle = {}
        for text in rows:
            name = unicode(text.strip(), 'utf-8')
            if len(name) >= 2:
                self.inc(last, name[-1])

            if len(name) >= 3:
                self.inc(middle, name[-2])

        self.save(last, self.NameLastTxt, self.NameLastJson)
        self.save(middle, self.NameMiddleTxt, self.NameMiddleJson)

    def topk(self, sorted_file, k):
        f = open(sorted_file)
        rows = f.readlines()
        f.close()
        return [r.strip() for r in rows[0:k]]

    def last_word_topk(self, k):
        return self.topk(self.NameLastTxt, k)

    def middle_word_topk(self, k):
        return self.topk(self.NameMiddleTxt, k)

    def word_freq(self, json_file, word):
        f = open(json_file)
        hmap = json.loads(f.read())
        f.close()
        if word not in hmap:
            return [0] * 3
        v = hmap[word]
        f = round(v[0] / float(hmap['total']), 4)
        # 频率、名次、总数
        return [f, v[1], len(hmap)]

    def last_word_freq(self, word):
        return self.word_freq(self.NameLastJson, word)

    def middle_word_freq(self, word):
        return self.word_freq(self.NameMiddleJson, word)


def test():
    wc = WordCount()
    k = 16
    print(u'==========中间字-top{}=========='.format(k))
    for i, r in enumerate(wc.middle_word_topk(k)):
        print('{}. {}'.format(i + 1, r))
    print(u'==========末尾字-top{}=========='.format(k))
    for i, r in enumerate(wc.last_word_topk(k)):
        print('{}. {}'.format(i + 1, r))

    print(u'==========字的频率==========')
    ws = [u'植', u'华', u'晓', u'启', u'羽', u'伟']
    for word in ws:
        print(u'{}: {}, {}'.format(word, wc.middle_word_freq(word),
              wc.last_word_freq(word)))


if __name__ == '__main__':
    test()
