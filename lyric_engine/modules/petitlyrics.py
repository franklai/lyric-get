# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import base64
import json
import logging
import urlparse
import common
import requests
from lyric_base import LyricBase

site_class = 'PetitLyrics'
site_index = 'petitlyrics'
site_keyword = 'petitlyrics'
site_url = 'http://petitlyrics.com/'
test_url = 'http://petitlyrics.com/lyrics/914675'
test_expect_length = 1275

'''
    Request URL
        http://petitlyrics.com/com/get_lyrics.ajax
    Method
        POST
    Data
        lyrics_id=914675

    Response
'''
class PetitLyrics(LyricBase):
    def parse_page(self):
        url = self.url

        s = requests.Session()
        self.s = s

        # 1. get song id from url
        id = self.get_song_id(url)
        if not id:
            logging.error('Failed to get id of url [%s]', url)
            return False

        r = s.get(url)

        # 2. get 1st part lyric from html and song_info
        html = r.text
        if not html:
            logging.info('Failed to get html of url [%s]' % (url))
            return False
        lyric_1st = self.get_lyric_1st_part(html)

        # 2. get CSRF token
        token = self.get_csrf_token(html)
        if not token:
            logging.info('Failed to get CSRF token of url [%s]' % (url))
            return False
        logging.debug('CSRF token is %s' % (token, ))

        # 2. get second part lyric
        lyric_2nd = self.get_lyric_2nd_part(id, token)
        self.lyric = common.htmlspecialchars_decode(lyric_1st + lyric_2nd)

        self.parse_artist_title(html)
        self.parse_lyricist(html)
        self.parse_composer(html)

        return True

    def get_lyric_1st_part(self, html):
        prefix = '<canvas id="lyrics" '
        suffix = '</canvas>'

        rawLyric = common.get_string_by_start_end_string(prefix, suffix, html)
        if not rawLyric:
            logging.info('Failed to get lyric string')
            return None
        encodedLyric = common.strip_tags(rawLyric)
        lyric_1st = common.unicode2string(encodedLyric)

        return lyric_1st

    def get_song_id(self, url):
        if not url:
            return None

        pattern = '/lyrics/([0-9]+)'
        id = common.get_first_group_by_pattern(url, pattern)
        if not id:
            pattern = '/kashi/([0-9]+)'
            id = common.get_first_group_by_pattern(url, pattern)

        return id

    def get_csrf_token(self, html):
        pattern = '(/lib/pl-lib.js[^"]+)'

        pl_lib_js = common.get_first_group_by_pattern(html, pattern)
        if not pl_lib_js:
            return None

        url = urlparse.urljoin(site_url, pl_lib_js)

        r = self.s.get(url)

        pattern = "'X-CSRF-Token', '(.*?)'"
        token = common.get_first_group_by_pattern(r.text, pattern)

        return token

    def get_lyric_2nd_part(self, id, token):
        if not id:
            return None

        actionUrl = 'http://petitlyrics.com/com/get_lyrics.ajax'
        postData = {'lyrics_id': id}
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'X-Dummy': 'Dummy\r\nX-CSRF-Token: %s' % (token,)
        }

        r = self.s.post(actionUrl, data=postData, headers=headers)
        obj = r.json()

        lyric_list = []
        for item in obj:
            lyric_list.append(base64.b64decode(item['lyrics']))

        return '\n'.join(lyric_list).decode('utf8', 'ignore')

    def parse_artist_title(self, html):
        startStr = '"description" content="'
        endStr = u'の歌詞ページです'

        infoStr = common.get_string_by_start_end_string(startStr, endStr, html)
        if not infoStr:
            return None

        infoStr = infoStr.replace(startStr, '')
        infoStr = infoStr.replace(endStr, '')
        infoStr = infoStr.strip()

        items = infoStr.split(' / ')

        if len(items) == 2:
            self.title = common.unicode2string(items[0])
            self.artist = common.unicode2string(items[1])

    def parse_lyricist(self, html):
        prefix = '<b>&#20316;&#35422;&#65306;</b>'
        suffix = '\t'

        logging.debug('find me LYRICIST')

        raw_string = common.find_string_by_prefix_suffix(html, prefix, suffix, False)
        if not raw_string:
            logging.debug('Failed to find lyricist')
            return False

        self.lyricist = common.htmlspecialchars_decode(common.unicode2string(raw_string)).strip()

    def parse_composer(self, html):
        prefix = '<b>&#20316;&#26354;&#65306;</b>'
        suffix = '\t'

        raw_string = common.find_string_by_prefix_suffix(html, prefix, suffix, False)
        if not raw_string:
            logging.debug('Failed to find composer')
            return False

        self.composer = common.htmlspecialchars_decode(common.unicode2string(raw_string)).strip()

def get_lyric(url):
    obj = PetitLyrics(url)

    return obj.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Cannot get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
