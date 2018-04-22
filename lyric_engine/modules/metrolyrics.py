# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import common
from lyric_base import LyricBase

site_class = 'MetroLyrics'
site_index = 'metrolyrics'
site_keyword = 'metrolyrics'
site_url = 'http://www.metrolyrics.com/'
test_url = 'http://www.metrolyrics.com/we-belong-together-lyrics-mariah-carey.html'


class MetroLyrics(LyricBase):
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
        raw = common.get_url_content(url)

        html = raw.decode('utf-8', 'ignore')

        return html

    def find_lyric(self, html):
        prefix = '<!-- First Section -->'
        suffix = '</sd-lyricbody>'
        rawLyric = common.get_string_by_start_end_string(prefix, suffix, html)
        if not rawLyric:
            return None

        rawLyric = self.remove_noise(rawLyric)

        rawLyric = rawLyric.replace('<br />', '\n')
        rawLyric = rawLyric.replace("<p class='verse'>", '\n\n')
        rawLyric = common.strip_tags(rawLyric).strip()

        self.lyric = rawLyric

        return True

    def remove_noise(self, rawLyric):
        items = [{
            'prefix': '<div id="mid-song-discussion"',
            'suffix': '<span class="label">See all</span>\n</a>\n</div>'
        }, {
            'prefix': '\n<!--WIDGET - RELATED-->',
            'suffix': '<!-- Second Section -->\n'
        }, {
            'prefix': '\n<!--WIDGET - PHOTOS-->',
            'suffix': '<!-- Third Section -->\n'
        }, {
            'prefix': '<p class="writers">',
            'suffix': '</sd-lyricbody>'
        }]

        for item in items:
            prefix = item['prefix']
            suffix = item['suffix']
            noise = common.get_string_by_start_end_string(
                prefix, suffix, rawLyric)
            if noise:
                rawLyric = rawLyric.replace(noise, '')

        return rawLyric

    def find_song_info(self, html):
        ret = True

        patterns = {
            'title': '"musicSongTitle":"(.*?)"',
            'artist': '"musicArtistName":"(.*?)"'
        }

        for key in patterns:
            pattern = patterns[key]

            value = common.get_first_group_by_pattern(html, pattern)
            if value:
                setattr(self, key, value)

        return ret


def get_lyric(url):
    obj = MetroLyrics(url)

    return obj.get()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url
    url = 'http://www.metrolyrics.com/red-lyrics-taylor-swift.html'

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
