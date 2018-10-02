#!/usr/bin/env python
# coding=utf-8

import argparse

from prettytable import PrettyTable
from crawler import Baidu, Baike, PCbaby
from view import toID, toPY, s2t, t2s
from tools import lookup, word_topk, word_freq


def RenderName(names):
    debug = True
    t = PrettyTable()
    t.field_names = ["序号", "简体", '繁体', '读音', 'ID', '百度', '百科', '打分', '分析', '释义']
    t.align = 'l'

    for i, n in enumerate(names):
        word = unicode(n, 'utf-8')[-1]
        freq, comment = word_freq(word, 1)
        row = [i, t2s(n), s2t(n), toPY(n), toID(n),
                Baidu(debug=debug).search(n).nums(),
                Baike(debug=debug).search(n).nums(),
                PCbaby(debug=debug).search(n).nums(),
                str(freq) + ' ' + comment,
                lookup(word)[:30].replace('\n', ''),
              ]
        t.add_row(row)

    return t


def test():
    names = ['孙中山', '戴笠', '杨利伟', '曹植', '李小龙']
    print(RenderName(names))


def main():
    ARGS = argparse.ArgumentParser(description=u'起名助手')
    ARGS.add_argument('--names', action='store', help=u'名字列表(","分隔)')
    ARGS.add_argument('--name_file', action='store', help=u'名字文件(每行一个)')
    ARGS.add_argument('--word', action='store', help=u'查询字典')
    ARGS.add_argument('--topk', action='store', type=int,
            default=0, help=u'查看常用名字TopK')
    ARGS.add_argument('--test', action='store_true', dest='test',
            default=True, help=u'run a test (default)')

    args = ARGS.parse_args()
    if args.names:
        names = [name.strip() for name in args.names.split(',')]
        print(RenderName(names))
        return
    if args.name_file:
        f = open(args.name_file)
        names = [name.strip() for name in f.readlines()]
        f.close()
        print(RenderName(names))
        return
    if args.word:
        print(lookup(unicode(args.word, 'utf-8')))
        return
    if args.topk > 0:
        names = word_topk(args.topk, 1)
        for i, r in enumerate(names):
            print('{}. {}'.format(i+1, r))
        return
    if args.test:
        return test()

    print('Use --help for command line help')


if __name__=='__main__':
    main()
