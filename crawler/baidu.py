# coding=utf-8

from .base import Base


class Baidu(Base):
    def __init__(self, debug=False):
        super(Baidu, self).__init__('baidu', debug)

    def get_url(self, word):
        return 'http://www.baidu.com/s?wd={}'.format(word)

    def find(self, soup):
        return soup.find('span', 'nums_text')


if __name__ == '__main__':
    print(Baidu().search('onestraw').nums())
