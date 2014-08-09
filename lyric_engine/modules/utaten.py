# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import re
import common
from lyric_base import LyricBase

site_class = 'UtaTen'
site_index = 'utaten'
site_keyword = 'utaten'
site_url = 'http://utaten.com/'
test_url = 'http://utaten.com/lyric/jb50903142'

class UtaTen(LyricBase):
    def parse_page(self):
        url = self.url

        content = self.get_lyric_content(url)
        if not content:
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_lyric(content):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(content):
            logging.info('Failed to get song info of url [%s]', url)
            return False 

        return True

    def get_lyric_content(self, url):
        prefix = 'http://utaten.com/lyric/load_text.php?LID='
        pattern = '/lyric/([a-z]{2}[0-9]+)'

        song_id = common.get_first_group_by_pattern(url, pattern)
        if not song_id:
            logging.info('Failed to get song id of url [%s]', url)
            return False

        content_url = prefix + song_id
        content = common.get_url_content(content_url)
        if not content:
            logging.info('Failed to get song content of url [%s]', url)
            return False

        return content

    def find_lyric(self, content):
        value = content.decode('sjis', 'ignore')

        value = re.sub('[ \t]+\n', '\n', value) # remove trailing space
        value = re.sub('\t *(.*)\n', r'\n(\1)\n', value) # move ruby to next line
        value = re.sub('   +', ',', value)
        value = value.strip()

        self.lyric = value
        
        return True

    def find_song_info(self, content):
        # so lazy do not parse song info, left it in lyric
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
    print(full.encode('utf-8', 'ignore'))
