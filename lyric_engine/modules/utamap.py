import logging
from utils import common
from utils.lyric_base import LyricBase

site_class = 'UtaMap'
site_index = 'utamap'
site_keyword = 'utamap'
site_url = 'http://www.utamap.com/'
test_url = 'http://www.utamap.com/showkasi.php?surl=70380'


class UtaMap(LyricBase):
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

        song_url = 'http://www.utamap.com/phpflash/flashfalsephp.php?unum=' + song_id
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

        # test for half to full
        lyric = common.half2full(lyric)

        self.lyric = lyric

        return True

    def find_song_info(self, url):
        ret = True
        html = common.get_url_content(url, encoding="euc_jp")

        keys = {
            'title': 'title',
            'artist': 'artist',
            'lyricist': 'sakusi',
            'composer': 'sakyoku',
        }

        patterns = {}
        for attr, key in keys.items():
            patterns[attr] = '<INPUT type="hidden" name={} value="([^"]*)">'.format(key)

        self.set_attr(patterns, html)

        return ret


def get_lyric(url):
    obj = UtaMap(url)

    return obj.get()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url
    url = 'http://www.utamap.com/showkasi.php?surl=k-131226-001'

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full)
