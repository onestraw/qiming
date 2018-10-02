#!/usr/bin/env python
# coding=utf-8

import time
import codecs
import datetime
import requests
from bs4 import BeautifulSoup


class Helper(object):
    @classmethod
    def store_raw_data(cls, content, filename):
        fp = codecs.open(filename, encoding='utf-8', mode='w+')
        fp.write(content)
        fp.close()

    @classmethod
    def fetch_raw_data(cls, filename):
        fp = codecs.open(filename, encoding='utf-8', mode='r')
        text = fp.read()
        fp.close()
        return text

    @classmethod
    def simple_download(cls, url, tofile=None):
        d = Downloader(url, 3, 3)
        res = d.get()
        if not tofile:
            tofile = url.split('/')[-1]
        soup = BeautifulSoup(res.text, 'html.parser')
        cls.store_raw_data(soup.prettify(), tofile)
        return soup


class Downloader(object):
    def __init__(self, baseURI, timeout, max_retries):
        self.uri = baseURI
        self.timeout = timeout
        self.max_retries = max_retries
        self.params = None
        self.proxies = None
        self.headers = None

    def setExtPath(self, extPath):
        if extPath:
            self.uri += str(extPath)

    def setParams(self, params):
        self.params = params

    def setProxies(self, proxies):
        self.proxies = proxies

    def setHeaders(self, headers):
        self.headers = headers

    def request(self):
        res = None
        retries = 0
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'}
        for k, v in self.headers.items():
            headers[k] = v

        print headers
        while retries < self.max_retries:
            try:
                retries += 1
                res = requests.get(self.uri, proxies=self.proxies, params=self.params, timeout=self.timeout, headers=headers)
                break
            except Exception as e:
                time.sleep(3)
                print str(e)

        self.log(res)
        if res and res.status_code != 200:
            res = None
        return res

    def log(self, res):
        uri = self.uri
        if isinstance(self.params, dict):
            kv = []
            for k,v in self.params.iteritems():
                kv.append(k + '=' + v)
            uri = uri + '?' + '&'.join(kv)

        if res:
            status_code = res.status_code
            #print res.headers
        else:
            status_code = -1

        print('{} -- GET {} {}'.format(datetime.datetime.now().isoformat(), uri, status_code))

    def get(self, extPath=None, params=None, headers={}):
        self.setExtPath(extPath)
        self.setParams(params)
        self.setHeaders(headers)
        return self.request()
