# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import common
from lyric_base import LyricBase

site_class = 'KashiNavi'
site_index = 'kashinavi'
site_keyword = 'kashinavi'
site_url = 'https://kashinavi.com/'
test_url = 'https://kashinavi.com/song_view.html?65545'


class KashiNavi(LyricBase):
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

        encoding = 'sjis'
        html = resp.decode(encoding, 'ignore')

        return html

    def find_lyric(self, url, html):
        pattern = 'unselectable="on;">(.*?)</p>'

        lyric = common.get_first_group_by_pattern(html, pattern)
        lyric = lyric.replace('<br>', '\n')
        lyric = common.strip_tags(lyric)
        lyric = lyric.strip()

        self.lyric = lyric

        return True

    def find_song_info(self, url, html):
        ret = True

        prefix = '<table border=0 cellpadding=0 cellspacing=5>'
        suffix = '</td></table>'
        infoString = common.get_string_by_start_end_string(
            prefix, suffix, html)

        title_pattern = u'<td><h.>(.+?).♪'
        self.title = common.strip_tags(
            common.get_first_group_by_pattern(infoString, title_pattern)
        )

        artist_pattern = u'♪.(.+?)</a>'        
        self.artist = common.strip_tags(
            common.get_first_group_by_pattern(infoString, artist_pattern)
        )

        prefix = '<table border=0 cellpadding=0 cellspacing=0>'
        suffix = '</td></table>'
        lyricAndMusic = common.get_string_by_start_end_string(
            prefix, suffix, infoString)

        pattern = u'作詞　：　(.*)<br>'
        self.lyricist = common.get_first_group_by_pattern(
            lyricAndMusic, pattern)

        pattern = u'作曲　：　(.*)</td>'
        self.composer = common.get_first_group_by_pattern(
            lyricAndMusic, pattern)

        return ret


def get_lyric(url):
    obj = KashiNavi(url)

    return obj.get()


def test_case_1():
    url = 'http://kashinavi.com/song_view.html?65545'
    obj = KashiNavi(url)
    obj.parse()

    assert obj.title == u'猫背'

    assert obj.title == u'猫背'
    assert obj.artist == u'坂本真綾'
    assert obj.lyricist == u'岩里祐穂'
    assert obj.composer == u'菅野よう子'
    assert len(obj.lyric) == 358


def test_case_2():
    url = 'http://kashinavi.com/song_view.html?77597'
    obj = KashiNavi(url)
    obj.parse()

    assert obj.title == u"We Don't Stop"
    assert obj.artist == u'西野カナ'
    assert obj.lyricist == u'Kana Nishino・GIORGIO 13'
    assert obj.composer == u'Giorgio Cancemi'
    assert len(obj.lyric) == 1247


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
