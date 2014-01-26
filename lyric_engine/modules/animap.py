# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import common
from lyric_base import LyricBase

site_class = 'AniMap'
site_index = 'animap'
site_keyword = 'animap'
site_url = 'http://www.animap.jp/'
test_url = 'http://www.animap.jp/kasi/showkasi.php?surl=dk101202_50'

class AniMap(LyricBase):
    def parse_page(self):
        url = self.url

        if not self.find_lyric(url):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(url):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def find_lyric(self, url):
        pattern = 'surl=([^&=]+)'

        song_id = common.get_first_group_by_pattern(url, pattern)

        if not song_id:
            logging.error('Failed to get id of url [%s]', url)
            return False

        song_url = 'http://www.animap.jp/kasi/phpflash/flashphp.php?unum=' + song_id
        data = common.get_url_content(song_url)
        if not data:
            logging.error('Failed to get content of url [%s]', song_url)
            return False

        prefix = 'test2='
        pos = data.find(prefix)
        if pos == -1:
            logging.error('Failed to find lyric position of url [%s]', url)
            return False

        lyric = data[pos + len(prefix):]
        lyric = lyric.decode('sjis').strip()

        # test for half to full
        lyric = common.half2full(lyric)

        self.lyric = lyric

        return True

    def find_song_info(self, url):
        ret = True
        html = common.get_url_content(url)

        encoding = 'euc_jp'
        html = html.decode(encoding, 'ignore')

        prefix = '<TABLE cellspacing="1"'
        suffix = '</TABLE>'
        info_table = common.find_string_by_prefix_suffix(html, prefix, suffix)

        def get_info_value_by_key(html, key):
            valuePrefix = '#ffffff>&nbsp;'
            valueSuffix = '</TD>'
            lenPrefix = len(valuePrefix)
            posKey = html.find(key)
            logging.debug('key position: %d' % (posKey))

            posStart = html.find(valuePrefix, posKey) + lenPrefix
            posEnd = html.find(valueSuffix, posStart)
            logging.debug('position [%d:%d]' % (posStart, posEnd))

            value = html[posStart:posEnd]
            return value

        patterns = {
            'title': u'曲名</TD>',
            'artist': u'歌手</TD>',
            'lyricist': u'作詞</TD>',
            'composer': u'作曲</TD>',
        }

        for key in patterns:
            pattern = patterns[key]
            value = get_info_value_by_key(info_table, pattern)

            if not value:
                logging.info('Failed to get %s of url [%s]', key, url)
                ret = False
            else:
                value = common.htmlspecialchars_decode(value).strip()
                setattr(self, key, value)

        return ret

def get_lyric(url):
    obj = AniMap(url)

    return obj.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = 'http://www.animap.jp/kasi/showkasi.php?surl=dk130730_30'

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
