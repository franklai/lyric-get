# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import base64
import logging
import re
import requests
import common
from lyric_base import LyricBase

site_class = 'UtaTen'
site_index = 'utaten'
site_keyword = 'utaten'
site_url = 'https://utaten.com/'
test_url = 'https://utaten.com/lyric/BUMP+OF+CHICKEN/beautiful+glider/'


class UtaTen(LyricBase):
    def parse_page(self):
        url = self.url

        r = requests.get(url)
        if r.status_code != 200:
            logging.info(
                'Cannot get content of url [%s], status code [%d]', url, r.status_code)
            logging.debug('headers: [%s]', r.headers)
            return False

        r.encoding = 'utf-8'
        content = r.text

        if not content:
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        logging.debug('web content length [%d]', len(content))
        if not self.find_lyric(content):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(content):
            logging.info('Failed to get song info of url [%s]', url)
            return False

        return True

    def get_lyric_content(self, url):
        content = common.get_url_content(url)

        return content

    def find_lyric(self, content):
        prefix = '<div class="lyricBody">'
        suffix = '</div>'

        lyric = common.find_string_by_prefix_suffix(content, prefix, suffix)

        pattern = '<span class="rt">(.*?)</span>'
        lyric = re.sub(pattern, r'(\1)', lyric)
        lyric = common.strip_tags(lyric)
        lyric = lyric.strip()

        self.lyric = lyric

        return True

    def find_song_info(self, content):
        #         content = content.decode('utf-8', 'ignore')

        pattern = u'<meta property="og:title" content="(.*?)　歌詞【'
        title = common.get_first_group_by_pattern(content, pattern)
        title = common.htmlspecialchars_decode(title)
        self.title = title

        pattern = u'<meta property="og:description" content="(.*?)が歌う'
        artist = common.get_first_group_by_pattern(content, pattern)
        artist = common.htmlspecialchars_decode(artist)
        self.artist = artist

        prefixes = {
            'lyricist': u'作詞</dt>',
            'composer': u'作曲</dt>',
        }
        suffix = '</dd>'

        for key in prefixes:
            prefix = prefixes[key]
            value = common.find_string_by_prefix_suffix(
                content, prefix, suffix, False)
            if value:
                value = common.strip_tags(value).strip()
                value = common.htmlspecialchars_decode(value)
                setattr(self, key, value)

        return True


def get_lyric(url):
    obj = UtaTen(url)

    return obj.get()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
#     print(full)
    print(full.encode('utf-8', 'ignore'))
