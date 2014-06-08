# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import time
try:
    import zlib
except:
    pass
import common
from lyric_base import LyricBase

site_class = 'KashiNavi'
site_index = 'kashinavi'
site_keyword = 'kashinavi'
site_url = 'http://www.kashinavi.com/'
test_url = 'http://kashinavi.com/song_view.html?65545'

class KashiNavi(LyricBase):
    def parse_page(self):
        url = self.url

        if not self.find_lyric(url):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(url):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def find_lyric(self, url):
        pattern = '\?([0-9]+)'

        song_id = common.get_first_group_by_pattern(url, pattern)
        if not song_id:
            logging.error('Failed to get id of url [%s]', url)
            return False

        params = self.get_hidden_params()

        query = '%s%s&time=%s' % (params['query_prefix'], song_id, time.localtime(), )
        logging.debug('query:%s' % (query, ))

        post_url = 'http://www.kashinavi.com/cgi-bin/kashi.cgi'
        resp = common.get_url_content(post_url, query)
        if not resp:
            logging.error('Failed to get content of url [%s], query [%s]', post_url, query)
            return False

        raw_lyric = resp.decode('utf-8', 'ignore')

        # if parsing rule changed, return debug info
        if raw_lyric.find(u'歌詞ナビTOPページより') > 0:
            self.lyric = '''
Site rule changed!
Please contact franklai
LoadVars::%s::myLoadVars
''' % (params['middle_value'])
            return True
        
        # else remove the useless part and return lyric
        front_str = 'kashi='
        start = raw_lyric.find(front_str) + len(front_str)
        lyric = raw_lyric[start:]
        lyric = lyric.strip()

        self.lyric = lyric

        return True

    def get_hidden_params(self):
        """ get new hidden parameters of kashinavi. need zlib support. """ 
        url = 'http://www.kashinavi.com/song_view.swf'

        # add random value to avoid Google cache old value
        url = '%s?time=%.0f' % (url, time.time())
        logging.debug('url:%s' % (url, ))

        data = common.get_url_content(url)

        if data[0:3] == 'CWS':
            # compressed swf
            compressed_str = data[8:]
            uncompressed_str = zlib.decompress(compressed_str)
        elif data[0:3] == 'FWS':
            # uncompressed swf
            uncompressed_str = data
        else:
            # not valid swf, just return
            return

        prefix = '\0LoadVars\0'
        suffix = '\0myLoadVars'

        u = uncompressed_str 
        m = u[u.find(prefix)+len(prefix): u.find(suffix)]
        items = m.split('\0')

        para_name = 'something'
        para_value = 'is'
        # wrong

        if len(items) == 3:
            target_name = items[1]
            target_value = items[2]
            
        middle_value = m.replace('\0', ' ')

        query_prefix = '%s=%s&file_no=' % (target_name, target_value,)

        para = {
            'query_prefix': query_prefix,
            'middle_value': middle_value,
        }

        logging.debug('query_prefix:%s' % (query_prefix, ))

        return para

    def find_song_info(self, url):
        ret = True
        resp = common.get_url_content(url)

        encoding = 'sjis'
        html = resp.decode(encoding, 'ignore')

        prefix = '<table border=0 cellpadding=0 cellspacing=5>'
        suffix = '</td></table>'
        infoString = common.get_string_by_start_end_string(prefix, suffix, html)

        self.title = common.strip_tags(
            common.get_string_by_start_end_string('<td>', '</td>', infoString)
        )

        self.artist = common.strip_tags(
            common.get_string_by_start_end_string('<td><a href=', '</a></td>', infoString)
        )

        prefix = '<table border=0 cellpadding=0 cellspacing=0>'
        suffix = '</td></table>'
        lyricAndMusic = common.get_string_by_start_end_string(prefix, suffix, infoString)

        pattern = u'作詞　：　(.*)<br>'
        self.lyricist = common.get_first_group_by_pattern(lyricAndMusic, pattern)

        pattern = u'作曲　：　(.*)</td>'
        self.composer = common.get_first_group_by_pattern(lyricAndMusic, pattern)

        return ret

def get_lyric(url):
    obj = KashiNavi(url)

    return obj.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
