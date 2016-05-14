# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import json
import logging
import urllib
import common
from lyric_base import LyricBase

site_class = 'MusixMatch'
site_index = 'musixmatch'
site_keyword = 'musixmatch'
site_url = 'https://www.musixmatch.com/'
test_url = 'https://www.musixmatch.com/lyrics/坂本真綾/猫背'

class MusixMatch(LyricBase):
    def parse_page(self):
        url = self.url

        html = self.get_html(url)
        if not html:
            logging.error('Failed to get html of url [%s]', url)
            return False

        logging.info(html)

        obj = self.find_json(html)
        if not obj:
            msg = self.find_msg(html)
            if not msg:
                logging.error('Failed to get json in html of url [%s]', url)
                return False
            else:
                # robot detect...
                self.lyric = msg
                return True

        if not self.find_lyric(obj):
            logging.error('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(obj):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def get_html(self, url):
        url = urllib.quote(url, ':/')
        data = common.get_url_content(url)
        if not data:
            logging.info('Failed to get content of url [%s]', url)
            return False

        html = data.decode('utf-8', 'ignore')

        return html

    def find_msg(self, html):
        prefix = '<h1 class="mxm-verify-headline">'
        suffix = '</form>'

        raw = common.find_string_by_prefix_suffix(html, prefix, suffix, True)
        if not raw:
            return False

        return raw

    def find_json(self, html):
        prefix = 'var __mxmState = '
        suffix = ';</script>'

        raw = common.find_string_by_prefix_suffix(html, prefix, suffix, False)
        if not raw:
            return False
        
        obj = json.loads(raw)
        if not obj:
            return False

        return obj

    def find_lyric(self, obj):
        try:
            body = obj['page']['lyrics']['lyrics']['body']
        except KeyError:
            logging.error('json does not have lyrics body')
            return False

        self.lyric = body
        return True

    def find_song_info(self, obj):
        try:
            track = obj['page']['track']
            self.title = track['name']
            self.artist = track['artistName']
        except KeyError:
            return False

        return True

def get_lyric(url):
    obj = MusixMatch(url)

    return obj.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url
    url = 'https://www.musixmatch.com/lyrics/artist-274325/Cry-Fight'

    full = get_lyric(url)
    if not full:
        print('Cannot get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
