import logging
from utils import common
from utils.lyric_base import LyricBase

site_class = 'KGet'
site_index = 'kget'
site_keyword = 'kget'
site_url = 'http://www.kget.jp/'
test_url = 'http://www.kget.jp/lyric/11066/'
test_expect_length = 1513


class KGet(LyricBase):
    def parse_page(self):
        url = self.url

        html = self.get_html(url)
        if not html:
            return False

        if not self.parse_lyric(url, html):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.parse_song_info(url, html):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def get_html(self, url):
        html = common.get_url_content(url, encoding="utf-8")
        if not html:
            logging.error('Failed to get content of url [%s]', url)
            return False

        return html

    def parse_lyric(self, url, html):
        prefix = '<div id="lyric-trunk">'
        suffix = '</div>'
        lyric = common.get_string_by_start_end_string(prefix, suffix, html)
        if not lyric:
            logging.error('Failed to parse lyric')
            return False

        lyric = common.strip_tags(lyric)

        lyric = common.unicode2string(lyric).strip()

        self.lyric = lyric
        return True

    def parse_song_info(self, url, html):
        ret = True

        pattern = '<h1.*?>(.*)</h1>'
        title = common.get_first_group_by_pattern(html, pattern)
        if title:
            title = common.htmlspecialchars_decode(
                common.strip_tags(title)).strip()
            self.title = title
        else:
            logging.warning('Failed to parse title of url [%s]', url)
            ret = False

        prefix = '<table class="lyric-data">'
        suffix = '</table>'
        info_table = common.find_string_by_prefix_suffix(html, prefix, suffix)
        info_table = info_table.replace('\n', '')

        patterns = {
            'artist': '">([^<]*)</a></span></td></tr>',
            'lyricist': 'td>([^<]*)<br></td></tr><tr>',
            'composer': 'td>([^<]*)<br></td></tr></table>',
        }

        self.set_attr(patterns, info_table)

        return ret


def get_lyric(url):
    obj = KGet(url)

    return obj.get()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = 'http://www.kget.jp/lyric/188989/'

    full = get_lyric(url)
    if not full:
        print('Cannot get lyric')
        exit()
    print(full)
