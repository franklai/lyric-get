import logging
import urllib.request, urllib.parse
import requests
from utils import common
from utils.lyric_base import LyricBase

site_class = 'MusicJp'
site_index = 'music_jp'
site_keyword = 'music-book.jp'
site_url = 'http://music-book.jp/music/'
test_url = 'http://music-book.jp/music/Kashi/aaa0k3wa?artistname=%25e5%25ae%2589%25e5%25ae%25a4%25e5%25a5%2588%25e7%25be%258e%25e6%2581%25b5&title=Love%2520Story&packageName=Sit!%2520Stay!%2520Wait!%2520Down!%252fLove%2520Story'


class MusicJp(LyricBase):
    def parse_page(self):
        url = self.url

        content = common.get_url_content(url)
        if not content:
            logging.info('Failed to get content of url [%s]', url)
            return False

        json = self.get_lyric_json(content)
        if not json:
            logging.info('Failed to get json of url [%s]', url)
            return False

        if not self.find_lyric(json):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(json, url):
            logging.info('Failed to get song info of url [%s]', url)
            return False

        return True

    def convert_js_to_url(self, js):
        js = js.replace('var data = "', '')
        js = js.replace('encodeURIComponent(', '').replace(')',
                                                           '').replace(';', '')
        js = js.replace('"', '').replace(
            '+', '').replace(' ', '').replace("'", '')

        return js

    def get_lyric_json(self, content):
        line = content.replace('\r\n', '')

        prefix = 'function showLyric'
        suffix = '$.ajax'
        line = common.find_string_by_prefix_suffix(line, prefix, suffix)
        if not line:
            logging.error('Failed to find string in ')
            return False

        prefix = 'var data ='
        suffix = ';'
        line = common.find_string_by_prefix_suffix(line, prefix, suffix)
        if not line:
            logging.error('Failed to find string in ')
            return False

        post_data = self.convert_js_to_url(line)
        logging.debug('post data: %s' % (post_data, ))

        lyric_url = 'http://music-book.jp/music/MusicDetail/GetLyric'
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        r = requests.post(lyric_url, data=post_data, headers=headers)
        return  r.json()

    def find_lyric(self, json):
        lyric = json['Lyrics'].replace('<br />', '\n')

        self.lyric = lyric.strip()

        return True

    def find_song_info(self, json, url):
        result = urllib.parse.urlparse(url)
        logging.debug(result)
        if not result.query:
            logging.warn('Failed to get query of url [%s]' % (url, ))
            return False

        queries = urllib.parse.parse_qs(result.query)
        logging.debug(queries)
        if 'artistname' not in queries:
            logging.warn('Failed to get artist from url [%s]' % (url, ))
            return False

        if 'title' not in queries:
            logging.warn('Failed to get artist from url [%s]' % (url, ))
            return False

        self.title = urllib.parse.unquote(
            queries['title'][0])
        self.artist = urllib.parse.unquote(
            queries['artistname'][0])
        self.lyricist = json['Writer']
        self.composer = json['Composer']
        return True


def get_lyric(url):
    obj = MusicJp(url)

    return obj.get()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url
    url = 'http://music-book.jp/music/Kashi/aaa2s0bv?artistname=%25e3%2582%25bd%25e3%2583%258a%25e3%2583%25bc%25e3%2583%259d%25e3%2582%25b1%25e3%2583%2583%25e3%2583%2588&title=%25e6%259c%2580%25e7%25b5%2582%25e9%259b%25bb%25e8%25bb%258a%2520%25ef%25bd%259emissing%2520you%25ef%25bd%259e&packageName=%25e6%259c%2580%25e7%25b5%2582%25e9%259b%25bb%25e8%25bb%258a%2520%25ef%25bd%259emissing%2520you%25ef%25bd%259e'

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full)
