# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import common
from lyric_base import LyricBase

site_class = 'KasiTime'
site_index = 'kasi_time'
site_keyword = 'kasi-time'
site_url = 'http://www.kasi-time.com/'
test_url = 'http://www.kasi-time.com/item-262.html'
test_expect_length = 1581

# current url format
# http://www.kasi-time.com/item-67546.html

class KasiTime(LyricBase):
    def parse_page(self):
        url = self.url

        if not self.find_lyric(url):
            logging.error('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(url):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def find_lyric(self, url):
        pattern = 'item-([0-9]+)\.html'

        song_id = common.get_first_group_by_pattern(url, pattern)

        if not song_id:
            logging.info('Failed to get id of url [%s]', url)
            return False

        song_url = 'http://www.kasi-time.com/item_js.php?no=' + song_id
        data = common.get_url_content(song_url)
        if not data:
            logging.info('Failed to get content of url [%s]', song_url)
            return False

        lyric = data.decode('utf-8', 'ignore')
        lyric = lyric.replace("document.write('", "")
        lyric = lyric.replace("');", "")
        lyric = lyric.replace("<br>", "\n")
        lyric = lyric.replace("&nbsp;", " ")
        lyric = common.htmlspecialchars_decode(lyric)
        lyric = common.unicode2string(lyric)
        lyric = common.strip_slash(lyric)
        lyric = lyric.strip()

        # test for half to full
        lyric = common.half2full(lyric)

        self.lyric = lyric

        return True

    def find_song_info(self, url):
        ret = True
        html = common.get_url_content(url)

        encoding = 'utf-8'
        html = html.decode(encoding, 'ignore')

        pattern = '<h1>(.*)</h1>'
        value = common.get_first_group_by_pattern(html, pattern).strip()
        if value:
            self.title = value
        else:
            logging.error('Failed to find title of url [%s]', url)
            ret = False

        prefix = '<div id="song_info_table">'
        suffix = '</div>'
        info_table = common.find_string_by_prefix_suffix(html, prefix, suffix)

        patterns = {
            'artist': u'歌手',
            'lyricist': u'作詞',
            'composer': u'作曲',
            'arranger': u'編曲',
        }

        for key in patterns:
            pattern = patterns[key]

            prefix = u'<td class="td1">%s</td>' % (pattern)
            suffix = '</a></td>'

            value = common.find_string_by_prefix_suffix(info_table, prefix, suffix, False)
            if not value:
                continue
            value = common.strip_tags(value).strip()
            if value:
                setattr(self, key, value)

        return ret

def get_lyric(url):
    obj = KasiTime(url)

    return obj.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

#     url = 'http://www.kasi-time.com/item-67546.html'
    url = test_url
    url = 'http://www.kasi-time.com/item-65831.html'

    full = get_lyric(url)
    if not full:
        print('Cannot get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
