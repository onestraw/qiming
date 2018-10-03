# coding=utf-8

import os
import re
import locale
from bs4 import BeautifulSoup

from crawler import Helper


class Base(object):
    def __init__(self, name='default', debug=False):
        locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
        self.num = 0
        self.engine_name = name
        self.debug = debug
        self.tmpdir = 'tmp'
        if not os.path.exists(self.tmpdir):
            os.makedirs(dirs)

    def get_filename(self, word):
        filename = '{}-{}.html'.format(self.engine_name, word)
        return os.path.join(self.tmpdir, filename)

    def get_url(self, word):
        raise NotImplementedError('get_url')

    def find(self, soup):
        raise NotImplementedError('find')

    def get(self, soup):
        if not soup:
            return ''
        v = soup.get_text()
        return v.strip()

    def parse_num(self, text):
        m = re.search('[\d|,|.]+', text)
        if not m:
            return
        nums = m.group()
        self.num = locale.atof(nums)
        return self.num

    def search(self, word):
        filename = self.get_filename(word)
        if self.debug and os.path.exists(filename):
            data = Helper.fetch_raw_data(filename)
            soup = BeautifulSoup(data, 'html.parser')
        else:
            url = self.get_url(word)
            soup = Helper.simple_download(url, tofile=filename)

        v = self.find(soup)
        self.parse_num(self.get(v))
        return self

    def nums(self):
        return self.num
