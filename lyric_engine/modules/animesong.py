# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import common
from lyric_base import LyricBase

site_class = 'AnimeSong'
site_index = 'animesong'
site_keyword = 'animesong'
site_url = 'http://www.jtw.zaq.ne.jp/animesong/'
test_url = 'http://www.jtw.zaq.ne.jp/animesong/ra/rahxephontagen/tune.html'

class AnimeSong(LyricBase):
    def parse_page(self):
        url = self.url

        html = self.get_html(url)
        if not html:
            logging.info('Failed to get html of url [%s]', url)
            return False

        if not self.parse_lyric(html):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        return True

    def get_html(self, url):
        html = common.get_url_content(url)
        if not html:
            return False

        html = html.decode('sjis', 'ignore')

        return html

    def parse_lyric(self, html):
        prefix = '<PRE>'
        suffix = '</PRE>'
        raw_lyric = common.find_string_by_prefix_suffix(html, prefix, suffix, False)
        if not raw_lyric:
            logging.info('Failed to parse lyric from html [%s]', html)
            return False

        raw_lyric = raw_lyric.strip()

        pos = raw_lyric.find('\n\n')
        if pos < 0:
            logging.info('Failed to find two consecutive newlines')
            return False

        self.title = raw_lyric[0:pos]

        raw_lyric = raw_lyric[pos+2:]

        pos = raw_lyric.find('\n\n')
        if pos < 0:
            logging.info('Failed to find two consecutive newlines')
            return False

        info = raw_lyric[0:pos]
        self.lyric = raw_lyric[pos+2:]

        patterns = {
            'artist': u'歌：(.+)',
            'lyricist': u'作詞：(.+?)／',
            'composer': u'作曲：(.+?)／',
            'arranger': u'編曲：(.+?)／',
        }

        for key in patterns:
            pattern  = patterns[key]

            value = common.get_first_group_by_pattern(info, pattern)

            if not value:
                logging.info('Failed to get %s of url [%s]', key, url)
            else:
                value = common.htmlspecialchars_decode(value).strip()
                setattr(self, key, value)

        return True

def get_lyric(url):
    klass = globals()[site_class]
    obj = klass(url)

    return obj.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
