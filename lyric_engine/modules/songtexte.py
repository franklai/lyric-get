import logging
from utils import common
from utils.lyric_base import LyricBase

site_class = 'SongTexte'
site_index = 'songtexte'
site_keyword = 'songtexte'
site_url = 'http://www.songtexte.com/'
test_url = 'http://www.songtexte.com/songtext/taylor-swift/begin-again-63a6de47.html'


class SongTexte(LyricBase):
    def parse_page(self):
        url = self.url

        html = self.get_lyric_html(url)
        if not html:
            logging.info('Failed to get lyric html of url [%s]', url)
            return False

        if not self.find_lyric(html):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(html):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def get_lyric_html(self, url):
        return common.get_url_content(url)

    def find_lyric(self, html):
        prefix = '<div id="lyrics">'
        suffix = '<div class="brightLink translation hidden-print">'
        rawLyric = common.get_string_by_start_end_string(prefix, suffix, html)

        if not rawLyric:
            # fall back to old finding </div>
            suffix = '</div>'
            rawLyric = common.get_string_by_start_end_string(
                prefix, suffix, html)

        rawLyric = rawLyric.replace(
            '<div id="71M_inreadads"></div>\n<br />\n', '')
        rawLyric = common.unicode2string(rawLyric)
        rawLyric = common.htmlspecialchars_decode(rawLyric)
        rawLyric = common.strip_tags(rawLyric).strip()

        self.lyric = rawLyric

        return True

    def sanitize(self, src):
        return common.unicode2string(common.htmlspecialchars_decode(src))

    def find_song_info(self, html):
        ret = True

        pattern = 'og:title" content="(.*) - (.*) Songtext"'

        regex = common.get_matches_by_pattern(html, pattern)
        if regex:
            self.artist = self.sanitize(regex.group(1))
            self.title = self.sanitize(regex.group(2))

        return ret


def get_lyric(url):
    obj = SongTexte(url)

    return obj.get()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full)
