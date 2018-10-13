# -*- coding: utf8 -*-
import os
import sys
from urllib import unquote
from xml.dom.minidom import parseString
include_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import requests
import common
from lyric_base import LyricBase

site_class = 'Yahoo'
site_index = 'yahoo'
site_keyword = 'yahoo'
site_url = 'https://gyao.yahoo.co.jp/lyrics/'
test_url = 'https://gyao.yahoo.co.jp/lyrics/Y152097'


class Yahoo(LyricBase):
    def parse_page(self):
        url = self.url

        html = self.get_html(url)
        if not html:
            logging.info('Failed to get html of url [%s]', url)
            return False

        if not self.find_lyric(url, html):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(url, html):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def get_html(self, url):
        resp = common.get_url_content(url)

        encoding = 'utf-8'
        html = resp.decode(encoding, 'ignore')

        return html

    def find_lyric(self, url, html):
        pattern = '<div class="lyrics-texts">(.+?)</div>'

        lyric = common.get_first_group_by_pattern(html, pattern)
        lyric = lyric.replace('<br>', '\n')
        lyric = lyric.replace('</p>', '\n')
        lyric = common.strip_tags(lyric)
        lyric = lyric.strip()

        self.lyric = lyric

        return True

    def find_song_info(self, url, html):
        ret = True

        prefix = '<h1'
        suffix = '</dl>'

        info = common.get_string_by_start_end_string(prefix, suffix, html)

        patterns = {
            'title': '<h1 class="lyrics-title">(.+)</h1>',
            'artist': '>([^>]+)</a></h2>',
            'lyricist': u'作詞</dt><dd[^>]*>(.+?)</dd>',
            'composer': u'作曲</dt><dd.*?>(.+?)</dd>',
        }

        for key, pattern in patterns.iteritems():
            value = common.get_first_group_by_pattern(info, pattern)
            
            if value:
                setattr(self, key, value)
            else:
                logging.info('Failed to get %s of url [%s]', key, url)
                ret = False

        return ret


def get_lyric(url):
    obj = Yahoo(url)

    return obj.get()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
