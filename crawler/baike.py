# coding=utf-8

from .base import Base


class Baike(Base):
    def __init__(self, debug=False):
        super(Baike, self).__init__('baike', debug)

    def get_url(self, word):
        return 'http://so.baike.com/doc/{}'.format(word)

    def find(self, soup):
        return soup.find('div', 'ser-guo')


if __name__ == '__main__':
    print(Baike().search('刘邦').nums())
