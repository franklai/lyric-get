# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import common
from lyric_base import LyricBase

site_class = 'JpLyrics'
site_index = 'jplyrics'
site_keyword = 'jplyrics'
site_url = 'http://jplyrics.com/'
test_url = 'http://jplyrics.com/j-pop-lyrics/9mm-parabellum-bullet-mad-pierrot.html'


class JpLyrics(LyricBase):
    def parse_page(self):
        url = self.url

        html = common.get_url_content(url)

        if not html:
            logging.info('Failed to get html of url [%s]', url)
            return False

        html = html.decode('utf-8')

        if not self.find_lyric(url, html):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(url, html):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def find_lyric(self, url, html):
        prefix = '<div class="divcss5-b">'
        suffix = '</div>'

        lyric = common.find_string_by_prefix_suffix(
            html, prefix, suffix, False)
        if not lyric:
            logging.info('Failed to get lyric div of url [%s]', url)
            return False

        lyric = lyric.replace('<br />', '')
        lyric = lyric.replace('<p>', '')
        lyric = lyric.replace('</p>', '\n')
        lyric = common.unicode2string(lyric)
        lyric = lyric.strip()
        lyric = common.strip_tags(lyric)

        self.lyric = lyric

        return True

    def find_song_info(self, url, html):
        ret = False
        pattern = '<h2 align="center" class="title">(.*?)</h2>'

        value = common.get_first_group_by_pattern(html, pattern)
        if value:
            self.title = common.unicode2string(common.strip_tags(value))
            ret = True

        return ret


def get_lyric(url):
    obj = JpLyrics(url)

    return obj.get()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('failed to get full lyric!')
        exit()
    print(full.encode('utf-8', 'ignore'))
