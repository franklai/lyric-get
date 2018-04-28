import logging
from utils import common
from utils.lyric_base import LyricBase

site_class = 'JLyric'
site_index = 'j_lyric'
site_keyword = 'j-lyric.net'
site_url = 'http://j-lyric.net/'
test_url = 'http://j-lyric.net/artist/a05d1a7/l041d93.html'


class JLyric(LyricBase):
    def parse_page(self):
        url = self.url

        content = common.get_url_content(url)
        if not content:
            logging.info('Failed to get content of url [%s]', url)
            return False

        if not self.find_lyric(content):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(content):
            logging.info('Failed to get song info of url [%s]', url)
            return False

        return True

    def find_lyric(self, content):
        prefix = '<p id="Lyric">'
        suffix = "</p>"
        lyric = common.find_string_by_prefix_suffix(
            content, prefix, suffix, False)

        if not lyric:
            return False

        lyric = lyric.replace('<br>', '\n')
        lyric = common.htmlspecialchars_decode(common.unicode2string(lyric))
        lyric = lyric.strip()

        self.lyric = lyric

        return True

    def find_song_info(self, content):
        prefix = '<div class="cap">'
        suffix = '<p id="Lyric">'
        info_block = common.find_string_by_prefix_suffix(
            content, prefix, suffix, False)

        patterns = {
            'title': '<h2>(.*?)歌詞</h2>',
            'artist': '>歌：(.*?)</p>',
            'lyricist': '>作詞：(.*?)</p>',
            'composer': '>作曲：(.*?)</p>'
        }

        self.set_attr(patterns, info_block)

        return True


def get_lyric(url):
    obj = JLyric(url)

    return obj.get()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url
    url = 'http://j-lyric.net/artist/a000673/l000bea.html'

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full)
