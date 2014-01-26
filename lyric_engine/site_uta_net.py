# coding: utf-8
import logging
import common
from lyric_base import LyricBase

site_class = 'UtaNet'
site_index = 'uta_net'
site_keyword = 'uta-net'
site_url = 'http://www.uta-net.com/'
# test_url = 'http://www.uta-net.com/user/phplib/view_0.php?ID=17248'
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
        pattern = '/song/([0-9]+)/'

        song_id = common.get_first_group_by_pattern(url, pattern)
        if not song_id:
            # try old pattern
            # http://www.uta-net.com/user/phplib/view_0.php?ID=17248
            pattern = 'ID=([0-9]+)'
            song_id = common.get_first_group_by_pattern(url, pattern)

        if not song_id:
            logging.info('Failed to get id of url [%s]', url)
            return False

        showkasi_pattern = 'http://www.uta-net.com/user/phplib/swf/showkasi.php?ID=%s&WIDTH=530&HEIGHT=810'
        song_url = showkasi_pattern % (song_id, )
        data = common.get_url_content(song_url)
        if not data:
            logging.info('Failed to get content of url [%s]', song_url)
            return False

        prefix = '<\0\0'
        suffix = '\0'
        lyric = common.find_string_by_prefix_suffix(data, prefix, suffix, False)

        if not lyric:
            logging.error('Failed to get lyric of url [%s]', url)
            return False

        lyric = unicode(lyric, 'utf8')
        lyric = lyric.strip()

        # test for half to full
        lyric = common.half2full(lyric)

        self.lyric = lyric

        return True

    def find_song_info(self, url):
        ret = True
        html = common.get_url_content(url)

        encoding = 'sjis'
        html = html.decode(encoding, 'ignore')

        patterns = {
            'title': u'<h2[^>]*>([^<]+)</h2>',
            'artist': u'歌手：<h3.*?><a href="/artist/[0-9]+/">([^<]+)</a></h3>',
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
                setattr(self, key, value)

        return ret

def get_lyric(url):
    obj = UtaNet(url)

    return obj.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = 'http://www.uta-net.com/song/138139/'

#     obj = UtaNet(url)
#     full = obj.get()
    full = get_lyric(url)
    if not full:
        print('damn !')
        exit()
    print(full.encode('utf-8', 'ignore'))
