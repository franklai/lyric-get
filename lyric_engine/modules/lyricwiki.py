# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import re
import common
from lyric_base import LyricBase

site_class = 'LyricWiki'
site_index = 'lyricwiki'
site_keyword = 'lyrics.wikia'
site_url = 'http://lyrics.wikia.com/'
test_url = 'http://lyrics.wikia.com/Ronan_Keating:When_You_Say_Nothing_At_All'

class LyricWiki(LyricBase):
    def parse_page(self):
        url = self.url

        html = self.get_lyric_html(url)
        if not html:
            logging.info('Failed to get content of url [%s]', url)
            return False
        
        if not self.find_lyric(html):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(html):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def get_lyric_html(self, url):
        encoding = 'utf8'

        raw = common.get_url_content(url)
        html = raw.decode(encoding, 'ignore')
        return html

    def find_lyric(self, html):
        pattern = '</div>(&#.*)<!--'
        items = re.findall(pattern, html)

        lyrics = []
        for item in items:
            string = item.replace('<br />', '\n')

            string += '\n'
            lyrics.append(string)
        lyric = '\n'.join(lyrics)

        lyric = common.unicode2string(lyric).strip()
        lyric = common.strip_tags(lyric)

        self.lyric = lyric
        return True

    def find_song_info(self, html):
        pattern = '<meta property="og:title" content="([^"]+)" />'
        ogTitle = common.get_first_group_by_pattern(html, pattern)

        artist, title = ogTitle.split(':')

        self.title = title
        self.artist = artist

        return True

def get_lyric(url):
    obj = LyricWiki(url)

    return obj.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url
    url = 'http://lyrics.wikia.com/%E5%9D%82%E6%9C%AC%E7%9C%9F%E7%B6%BE_(Maaya_Sakamoto):%E5%83%95%E3%81%9F%E3%81%A1%E3%81%8C%E6%81%8B%E3%82%92%E3%81%99%E3%82%8B%E7%90%86%E7%94%B1'

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
