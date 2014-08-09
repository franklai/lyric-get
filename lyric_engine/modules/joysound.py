# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import json
import logging
import common
from lyric_base import LyricBase

site_class = 'JoySound'
site_index = 'joysound'
site_keyword = 'joysound'
site_url = 'http://joysound.com/'
test_url = 'http://joysound.com/ex/search/karaoke/_selSongNo_28721_songwords.htm'
test_expect_length = 1551

class JoySound(LyricBase):
    def parse_page(self):
        url = self.url

        song_id = self.get_song_id(url)
        if not song_id:
            logging.info('Failed to song id from [%s]', url)
            return False

        logging.debug('Song ID is %s', song_id)

        json_obj = self.get_song_json(song_id)
        if not json_obj:
            logging.info('Failed to get song JSON of url [%s]', url)
            return False

        if not self.parse_lyric(json_obj):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.parse_song_info(json_obj):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def get_song_id(self, url):
        pattern = '/ex/search/karaoke/_selSongNo_([0-9]+)_songwords.htm'
        song_id = common.get_first_group_by_pattern(url, pattern)

        return song_id

    def get_referer(self, song_id):
        pattern = 'http://joysound.com/ex/search/karaoke/_selSongNo_%s_songwords.htm'
        return pattern % (song_id, )

    def get_song_json(self, song_id):
        json_url = 'http://joysound.com/ex/api/lyrics/_getLyrics.htm'
        post_data = 'sno=%s' % (song_id, )
        headers = {
            'Referer': self.get_referer(song_id)
        }

        json_str = common.get_url_content(json_url, post_data, headers)
        if not json_str:
            logging.info('Failed to get json from url [%s]', url)
            return False

        obj = json.loads(json_str)

        return obj

    def parse_lyric(self, json_obj):
        if 'kasi' not in json_obj:
            logging.info('No "kasi" in song JSON')
            return False

        value = json_obj['kasi'].replace('<br>', '\r\n')
        value = common.unicode2string(value)
        value = value.strip()

        self.lyric = value

        return True

    def parse_song_info(self, json_obj):
        patterns = {
            'title': 'song_disp_str',
            'artist': 'singer_disp',
            'lyricist': 'songwriter',
            'composer': 'composer',
        }

        for key in patterns:
            json_key = patterns[key]

            if json_key in json_obj:
                value = json_obj[json_key]

                if value:
                    setattr(self, key, value)
        return True

def get_lyric(url):
    obj = JoySound(url)

    return obj.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Cannot get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))

