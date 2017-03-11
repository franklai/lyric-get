# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import common
from lyric_base import LyricBase

site_class = 'UtaNet'
site_index = 'uta_net'
site_keyword = 'uta-net'
site_url = 'http://www.uta-net.com/'
test_url = 'http://www.uta-net.com/song/138139/'
test_expect_length = 1089

# current url format
# 'http://www.uta-net.com/song/138139/'
#
# former url
# 'http://www.uta-net.com/user/phplib/view_0.php?ID=17248'

class UtaNet(LyricBase):
    def parse_page(self):
        url = self.url

        if not self.find_lyric(url):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(url):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def find_lyric(self, url):
        pattern = '/[a-z]+/([0-9]+)/'

        song_id = common.get_first_group_by_pattern(url, pattern)
        if not song_id:
            # try old pattern
            # http://www.uta-net.com/user/phplib/view_0.php?ID=17248
            pattern = 'ID=([0-9]+)'
            song_id = common.get_first_group_by_pattern(url, pattern)

        if not song_id:
            logging.info('Failed to get id of url [%s]', url)
            return False

        # http://www.uta-net.com/user/phplib/svg/showkasi.php?ID=17248&WIDTH=560&HEIGHT=756&FONTSIZE=15&t=1489258939
        showkasi_pattern = 'http://www.uta-net.com/user/phplib/svg/showkasi.php?ID=%s'
        song_url = showkasi_pattern % (song_id, )
        data = common.get_url_content(song_url)
        if not data:
            logging.info('Failed to get content of url [%s]', song_url)
            return False

        prefix = '<svg '
        suffix = '</svg>'
        lyric = common.find_string_by_prefix_suffix(data, prefix, suffix, True)

        if not lyric:
            logging.error('Failed to get lyric of url [%s]', url)
            return False

        lyric = unicode(lyric, 'utf8')
        lyric = lyric.replace('</text>', '\n')
        lyric = common.strip_tags(lyric)
        lyric = lyric.strip()

        # test for half to full
        lyric = common.half2full(lyric)

        self.lyric = lyric

        return True

    def find_song_info(self, url):
        ret = True
        html = common.get_url_content(url)

        encoding = 'utf8'
        html = html.decode(encoding, 'ignore')

        patterns = {
            'title': u'<h2[^>]*>([^<]+)</h2>',
            'artist': u'歌手：<h3.*?><a href="/artist/[0-9]+/".*?>(.+?)</a></h3>',
            'lyricist': u'作詞：<h4.*?>([^<]+)</h4>',
            'composer': u'作曲：<h4.*?>([^<]+)</h4>'
        }

        for key in patterns:
            pattern = patterns[key]

            value = common.get_first_group_by_pattern(html, pattern)

            if not value:
                logging.info('Failed to get %s of url [%s]', key, url)
                ret = False
            else:
                value = common.unicode2string(common.strip_tags(value))
                setattr(self, key, value)

        return ret

def get_lyric(url):
    obj = UtaNet(url)

    return obj.get()

def download_search_result():
    url = 'http://www.uta-net.com/search/?Aselect=1&Bselect=3&Keyword=KOKIA&sort=6'
    output = 'uta_net.search.txt'

    html = common.get_url_content(url)
    if not html:
        logging.error('Failed to download url [%s]' % (url, ))
        return False

    pattern = '<td class="side td1"><a href="([^"]+)">'

    import re
    import urlparse
    songs = re.findall(pattern, html)

    out = open(output, 'wb')
    for song in songs:
        print song
        song_url = urlparse.urljoin(site_url, song)
        full = get_lyric(song_url)

        out.write(full.encode('utf-8'))
        out.write('\n\n=====\n')

    out.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

#     download_search_result()
#     exit()

#     url = 'http://www.uta-net.com/song/181206/'
    url = test_url

    full = get_lyric(url)
    if not full:
        print('damn !')
        exit()
    print(full.encode('utf-8', 'ignore'))
