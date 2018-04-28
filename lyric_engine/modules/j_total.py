import logging
import re
from utils import common
from utils.lyric_base import LyricBase

site_class = 'JTotal'
site_index = 'j_total'
site_keyword = 'j-total'
site_url = 'http://music.j-total.net/'
test_url = 'http://music.j-total.net/data/026ha/053_Perfume/038.html'


class JTotal(LyricBase):
    def parse_page(self):
        url = self.url

        html = self.get_lyric_html(url)
        if not html:
            logging.error('Failed to get lyric html of url [%s]', url)
            return False

        if not self.find_lyric(html):
            logging.error('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(html):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def get_lyric_html(self, url):
        html = common.get_url_content(url, encoding="shift_jis")
        if not html :
            logging.error('Failed to get content of url [%s]', url)
            return False

        return html

    def find_lyric(self, html):
        prefix = '<!--HPSTART-->'
        suffix = '<!--HPEND-->'

        body = common.find_string_by_prefix_suffix(html, prefix, suffix)
        body = re.sub('     +', '', body)
        body = body.replace('\r', '')
        body = body.replace('\n', '')
        body = body.replace('<br>', '\n')
        body = common.strip_tags(body).strip()

        self.lyric = body

        return True

    def find_song_info(self, html):
        ret = True

        prefix = '<font size="4" color="#FFFFFF"><b>'
        suffix = '</b></font>'
        value = common.find_string_by_prefix_suffix(html, prefix, suffix)
        if value:
            title = common.strip_tags(value).strip()
            self.title = title

        prefix = '<font size="3" color="#FFFFFF">'
        suffix = '</font>'
        info = common.find_string_by_prefix_suffix(html, prefix, suffix)
        info = re.sub('     +', '', info)
        info = info.replace('\r', '').replace('\n', '')

        patterns = {
            'artist': '歌：(.*?)/',
            'lyricist': '詞：(.*?)/',
            'composer': '曲：(.*?)<',
        }

        self.set_attr(patterns, info)

        return ret


def get_lyric(url):
    obj = JTotal(url)

    return obj.get()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Cannot get lyric')
        exit()
    print(full)
