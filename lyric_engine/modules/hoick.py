# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import urllib
import requests
import common
from lyric_base import LyricBase

site_class = 'Hoick'
site_index = 'hoick'
site_keyword = 'hoick'
site_url = 'https://hoick.jp/'
test_url = 'http://hoick.jp/mdb/detail/9920/%E3%81%AB%E3%81%98'


class Hoick(LyricBase):
    def parse_page(self):
        url = self.url

        text = self.get_from_azure(url)
        if not text:
            logging.info('Failed to get from azure, url [%s]', url)
            return False

        if not self.parse_text(text):
            logging.info('Failed to parse text from azure, url [%s]', url)
            return False

        return True

    def parse_text(self, text):
        lines = text.split(u'\n')

        if len(lines) < 5:
            return False

        self.title = lines[0]
        self.lyricist = lines[2].replace(u'作詞：', '')
        self.composer = lines[3].replace(u'作曲：', '')

        self.lyric = '\n'.join(lines[6:])

        return True

    def get_from_azure(self, url):
        azure_url = 'https://lyric-get-node-test1.azurewebsites.net/app?url=%s' % (
            urllib.quote(url))
        r = requests.get(azure_url)

        obj = r.json()

        return obj['lyric']

def get_lyric(url):
    obj = Hoick(url)

    return obj.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Cannot get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
