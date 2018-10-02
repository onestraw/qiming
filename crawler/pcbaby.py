# coding=utf-8

import urllib
import random
import json

from base import Base


class PCbaby(Base):
    def __init__(self, debug=False):
        super(PCbaby, self).__init__('pcbaby', debug)
        self.score = 0

    def get_url(self, name):
        family_name = urllib.quote(name[:3])
        first_name = urllib.quote(name[3:])
        # 0 girl, 1 boy
        gender = 1
        rt = random.randint(10**4, 10**7)
        return "http://my.pcbaby.com.cn/intf/forCMS/getIntitleScoreJson.jsp?\
                sex='{gender}'&xing='{xing}'&callback=testName&name='{ming}'\
                &time='{randtime}'&req_enc=utf-8".format(
                        xing=family_name, ming=first_name, gender=gender, randtime=rt)

    def parse_num(self, text):
        pass

    def find(self, soup):
        # response format:
        # testName({"ids":100,"scores":[{"id":13,"content":"xxxx","score":"66"}]})
        try:
            body = soup.string.strip()[9:-1]
            d = json.loads(body)
            self.score = int(d['scores'][0]['score'])
        except Exception as e:
            print('raw body: {}, find score err: {}'.format(soup.string, e.message))

        return soup

    def nums(self):
        return self.score


if __name__=='__main__':
    print(PCbaby().search('何中天').nums())
