# coding=utf-8

import os
from bs4 import BeautifulSoup

from crawler import Downloader, Helper
from base import Base


class Httpcn(Base):
    def __init__(self, debug=False):
        super(Httpcn, self).__init__('httpcn', debug)
        self.score = 0

    def search(self, word):
        filename = self.get_filename(word)
        if self.debug and os.path.exists(filename):
            data = Helper.fetch_raw_data(filename)
            soup = BeautifulSoup(data, 'html.parser')
        else:
            url = 'http://m.life.httpcn.com/m/xingming/'
            uname = unicode(word, 'utf-8')
            data = {
                'act': 'submit',
                'xing': uname[0],
                'ming': uname[1:],
                'sex': 1,
                'isbz': 0,
            }
            Helper.simple_download(url, filename)
            res = Downloader(url, 3, 3).post(data=data)
            soup = BeautifulSoup(res.text, 'html.parser')
            Helper.store_raw_data(soup.prettify(), filename)

        soup = soup.find('div', 'progress-bar')
        self.score = self.parse_num(self.get(soup))
        return self

    def nums(self):
        return self.score


if __name__ == '__main__':
    print(Httpcn().search('何中天').nums())
