# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import json
import logging
import common
from lyric_base import LyricBase

site_class = 'KashiSearch'
site_index = 'kashisearch'
site_keyword = 'kashisearch.jp'
site_url = 'http://kashisearch.jp/'
test_url = 'http://kashisearch.jp/lyrics/188242'

class KashiSearch(LyricBase):
    def parse_page(self):
        url = self.url

        lyric_content = self.get_lyric_content(url)
        if not lyric_content:
            return False

        if not self.find_lyric(lyric_content):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        page_content = self.get_page_content(url)
        if not page_content:
            return False

        if not self.find_song_info(page_content):
            logging.info('Failed to get song info of url [%s]', url)
            return False 

        return True

    def get_lyric_content(self, url):
        lyric_api_url = 'http://kashisearch.jp/api/lyrics'

        lyric_id = self.get_lyric_id(url)
        if not lyric_id:
            return False

        post_data = 'id=%s' % (lyric_id, )
        headers = {
            'X-Requested-With': 'XMLHttpRequest' 
        }
        raw_lyric = common.get_url_content(lyric_api_url, post_data, headers)
        if not raw_lyric:
            logging.error('Failed to get lyric content, url [%s]', url)
            return False

        raw_lyric = raw_lyric.decode('utf-8', 'ignore')

        return raw_lyric

    def get_lyric_id(self, url):
        pattern = 'lyrics/([0-9]+)'

        lyric_id = common.get_first_group_by_pattern(url, pattern)
        if not lyric_id:
            logging.error('Failed to parse id of lyric from url')
            return False

        return lyric_id

    def get_page_content(self, url):
        content = common.get_url_content(url)
        if not content:
            logging.info('Failed to get content of url [%s]', url)
            return False

        content = content.decode('utf-8', 'ignore')

        return content

    def find_lyric(self, content):
        data = json.loads(content)
        if 'words' not in data:
            logging.error('Cannot find words in lyric json content')
            return False

        words = data['words']
        lyric = words.strip();

        self.lyric = lyric

        return True

    def find_song_info(self, content):
        pattern = 'og:description" content="(.*)"'
        og_desc = common.get_first_group_by_pattern(content, pattern)
        if og_desc:
            pattern = u'(.*?)「(.*?)」'
            matches = common.get_matches_by_pattern(og_desc, pattern)
            if matches:
                artist = matches.group(1)
                artist = artist.replace(u'歌詞サーチ ', '')
                self.artist = artist
                self.title  = matches.group(2)
            else:
                logging.debug('og desc: %s' % (og_desc))

        prefix = '="lyrics_info_text"'
        suffix = '</div>'
        info_text = common.find_string_by_prefix_suffix(content, prefix, suffix, False)
        if not info_text:
            logging.info('Failed to find lyrics info text')
        one_line = info_text.replace('\n', '')

        patterns = {
            'lyricist': u'>作詞</p><p class="info_detail">(.*?)</p>',
            'composer': u'>作曲</p><p class="info_detail">(.*?)</p>',
        }

        for key in patterns:
            pattern = patterns[key]

            value = common.get_first_group_by_pattern(one_line, pattern)
            if value:
                value = common.strip_tags(common.htmlspecialchars_decode(value)).strip()
                setattr(self, key, value)
            else:
                logging.debug('Failed to get %s, pattern: %s' % (key, pattern, ))

        return True

def get_lyric(url):
    obj = KashiSearch(url)

    return obj.get()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
