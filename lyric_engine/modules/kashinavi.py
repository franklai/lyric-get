import logging
from utils import common
from utils.lyric_base import LyricBase

site_class = 'KashiNavi'
site_index = 'kashinavi'
site_keyword = 'kashinavi'
site_url = 'http://kashinavi.com/'
test_url = 'http://kashinavi.com/song_view.html?65545'


class KashiNavi(LyricBase):
    def parse_page(self):
        url = self.url

        html = self.get_html(url)
        if not html:
            logging.info('Failed to get html of url [%s]', url)
            return False

        if not self.find_lyric(url, html):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(url, html):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def get_html(self, url):
        html = common.get_url_content(url, encoding="shift_jis")

        return html

    def find_lyric(self, url, html):
        prefix = '<p oncopy="return false;" unselectable="on;">'
        suffix = '</p>'

        lyric = common.find_string_by_prefix_suffix(
            html, prefix, suffix, False)
        lyric = lyric.replace('<br>', '\n')
        lyric = common.strip_tags(lyric)
        lyric = lyric.strip()

        self.lyric = lyric

        return True

    def find_song_info(self, url, html):
        ret = True

        prefix = '<table border=0 cellpadding=0 cellspacing=5>'
        suffix = '</td></table>'
        infoString = common.get_string_by_start_end_string(
            prefix, suffix, html)

        self.title = common.strip_tags(
            common.get_string_by_start_end_string('<td>', '</td>', infoString)
        )

        self.artist = common.strip_tags(
            common.get_string_by_start_end_string(
                '<td><h3><a href=', '</a></h3></td>', infoString)
        )

        prefix = '<table border=0 cellpadding=0 cellspacing=0>'
        suffix = '</td></table>'
        lyricAndMusic = common.get_string_by_start_end_string(
            prefix, suffix, infoString)

        pattern = '作詞　：　(.*)<br>'
        self.lyricist = common.get_first_group_by_pattern(
            lyricAndMusic, pattern)

        pattern = '作曲　：　(.*)</td>'
        self.composer = common.get_first_group_by_pattern(
            lyricAndMusic, pattern)

        return ret


def get_lyric(url):
    obj = KashiNavi(url)

    return obj.get()


def test_case_1():
    url = 'http://kashinavi.com/song_view.html?65545'
    obj = KashiNavi(url)
    obj.parse()

    assert obj.title == '猫背'

    assert obj.title == '猫背'
    assert obj.artist == '坂本真綾'
    assert obj.lyricist == '岩里祐穂'
    assert obj.composer == '菅野よう子'
    assert len(obj.lyric) == 358


def test_case_2():
    url = 'http://kashinavi.com/song_view.html?77597'
    obj = KashiNavi(url)
    obj.parse()

    assert obj.title == "We Don't Stop"
    assert obj.artist == '西野カナ'
    assert obj.lyricist == 'Kana Nishino・GIORGIO 13'
    assert obj.composer == 'Giorgio Cancemi'
    assert len(obj.lyric) == 1247


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full)
