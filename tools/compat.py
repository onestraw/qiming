# coding=utf-8
import sys


if sys.version_info[0] == 2:
    raw_unicode = unicode


def unicode(s, en):
    if sys.version_info[0] == 3:
        return s
    return raw_unicode(s, en)
