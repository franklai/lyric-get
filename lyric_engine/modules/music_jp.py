# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import json
import logging
import urllib
import urlparse
import common
from lyric_base import LyricBase

site_class = 'MusicJp'
site_index = 'music_jp'
site_keyword = 'music-book.jp'
site_url = 'http://music-book.jp/music/'
test_url = 'http://music-book.jp/music/Kashi/aaa0k3wa?artistname=%25e5%25ae%2589%25e5%25ae%25a4%25e5%25a5%2588%25e7%25be%258e%25e6%2581%25b5&title=Love%2520Story&packageName=Sit!%2520Stay!%2520Wait!%2520Down!%252fLove%2520Story'

class MusicJp(LyricBase):
    def parse_page(self):
        url = self.url

        content = self.get_url_content(url)
        if not content:
            logging.info('Failed to get content of url [%s]', url)
            return False

        json = self.get_lyric_json(content)
        if not json:
            logging.info('Failed to get json of url [%s]', url)
            return False

        if not self.find_lyric(json):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(json, url):
            logging.info('Failed to get song info of url [%s]', url)
            return False 

        return True

    def get_url_content(self, url):
        handle = common.URL('http://music-book.jp/music/')
        cookie = self.get_cookie(handle)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2141.0 Safari/537.36',
            'Cookie': cookie
        }
        html = common.get_url_content(url, data=None, headers=headers)
        if not html:
            logging.error('Failed to get html of url [%s]' % (url, ))
            return False

        return html.decode('utf-8', 'ignore')

    def get_cookie(self, handle):
        info = handle.get_info()
        logging.debug('info: %s' % (info))

        set_cookie = handle.get_header('set-cookie')
        logging.debug('set_cookie: %s' % (set_cookie))

        if isinstance(set_cookie, list):
            # google url fetch service for set-cookie will return list
            logging.info('set_cookie: %s' % (set_cookie))
            for item in set_cookie:
                pattern = '(ASP.NET_SessionId=[0-9a-z]+;)'
                cookie = common.get_first_group_by_pattern(item, pattern)
                if cookie:
                    return cookie

        if 'set-cookie' in info:
            pattern = '(ASP.NET_SessionId=[0-9a-z]+;)'
            cookie = common.get_first_group_by_pattern(info['set-cookie'], pattern)
            if not cookie:
                logging.error('Failed to get session id from cookie [%s]' % (info['set-cookie']))
                return ''
            return cookie

        return ''

    def convert_js_to_url(self, js):
        js = js.replace('var data = "', '')
        js = js.replace('encodeURIComponent(', '').replace(')', '').replace(';', '')
        js = js.replace('"', '').replace('+', '').replace(' ', '').replace("'", '')

        return js

    def get_lyric_json(self, content):
        line = content.replace('\r\n', '')

        prefix = 'function showLyric'
        suffix = '$.ajax'
        line = common.find_string_by_prefix_suffix(line, prefix, suffix)
        if not line:
            logging.error('Failed to find string in ')
            return False

        prefix = 'var data ='
        suffix = ';'
        line = common.find_string_by_prefix_suffix(line, prefix, suffix)
        if not line:
            logging.error('Failed to find string in ')
            return False

        post_data = self.convert_js_to_url(line)

        lyric_url = 'http://music-book.jp/music/MusicDetail/GetLyric'
        raw_json = common.get_url_content(lyric_url, data=post_data)
        if not raw_json:
            logging.error('Failed to get json of url [%s]' % (lyric_url, ))
            return False

        return json.loads(raw_json)

    def find_lyric(self, json):
        lyric = json['Lyrics'].replace('<br />', '\n')

        self.lyric = lyric.strip()

        return True

    def find_song_info(self, json, url):
        # so lazy do not parse song info, left it in lyric

        result = urlparse.urlparse(url)
        logging.debug(result)
        if not result.query:
            logging.warn('Failed to get query of url [%s]' % (url, ))
            return False

        queries = urlparse.parse_qs(result.query)
        logging.debug(queries)
        if 'artistname' not in queries:
            logging.warn('Failed to get artist from url [%s]' % (url, ))
            return False

        if 'title' not in queries:
            logging.warn('Failed to get artist from url [%s]' % (url, ))
            return False

        self.title = urllib.unquote(queries['title'][0]).decode('utf-8', 'ignore')
        self.artist = urllib.unquote(queries['artistname'][0]).decode('utf-8', 'ignore')
        self.lyricist = json['Writer']
        self.composer = json['Composer']
        return True

def get_lyric(url):
    obj = MusicJp(url)

    return obj.get()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url
    url = 'http://music-book.jp/music/Kashi/aaa2s0bv?artistname=%25e3%2582%25bd%25e3%2583%258a%25e3%2583%25bc%25e3%2583%259d%25e3%2582%25b1%25e3%2583%2583%25e3%2583%2588&title=%25e6%259c%2580%25e7%25b5%2582%25e9%259b%25bb%25e8%25bb%258a%2520%25ef%25bd%259emissing%2520you%25ef%25bd%259e&packageName=%25e6%259c%2580%25e7%25b5%2582%25e9%259b%25bb%25e8%25bb%258a%2520%25ef%25bd%259emissing%2520you%25ef%25bd%259e'

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
