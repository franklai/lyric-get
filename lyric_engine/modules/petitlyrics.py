# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import base64
import json
import logging
import urlparse
import common

from lyric_base import LyricBase

try:
    import requests_toolbelt.adapters.appengine
    # Use the App Engine Requests adapter. This makes sure that Requests uses
    # URLFetch.
    requests_toolbelt.adapters.appengine.monkeypatch()
except:
    pass

site_class = 'PetitLyrics'
site_index = 'petitlyrics'
site_keyword = 'petitlyrics'
site_url = 'https://petitlyrics.com/'
test_url = 'https://petitlyrics.com/lyrics/914675'
test_expect_length = 1275

'''
    Request URL
        http://petitlyrics.com/com/get_lyrics.ajax
    Method
        POST
    Data
        lyrics_id=914675

    Response
'''
class PetitLyrics(LyricBase):
    def parse_page(self):
        url = self.url

        if not self.get_from_azure(url):
            logging.info('Failed to get from azure, url [%s]', url)
            return False

        return True

    def parse_page_local(self):
        url = self.url

        # 1. get song id from url
        id = self.get_song_id(url)
        if not id:
            logging.error('Failed to get id of url [%s]', url)
            return False

        # 2. get html
        html = self.get_content_by_url(url)

        if not html:
            logging.info('Failed to get html of url [%s]' % (url))
            return False

        # 3. get CSRF token
        token = self.get_csrf_token(html)
        if not token:
            logging.info('Failed to get CSRF token of url [%s]' % (url))
            return False
        logging.debug('CSRF token is %s' % (token, ))

        # 5. get lyric
        lyric = self.get_lyric(id, token)
        if not lyric:
            logging.info('Failed to get lyric of url [%s]' % (url))
            return False

        self.lyric = common.htmlspecialchars_decode(lyric.strip())

        self.parse_artist_title(html)
        self.parse_lyricist(html)
        self.parse_composer(html)

        return True

    def get_song_id(self, url):
        if not url:
            return None

        pattern = '/lyrics/([0-9]+)'
        id = common.get_first_group_by_pattern(url, pattern)
        if not id:
            pattern = '/kashi/([0-9]+)'
            id = common.get_first_group_by_pattern(url, pattern)

        return id

    def get_csrf_token(self, html):
        pattern = '(/lib/pl-lib.js[^"]+)'

        pl_lib_js = common.get_first_group_by_pattern(html, pattern)
        if not pl_lib_js:
            return None

        url = urlparse.urljoin(site_url, pl_lib_js)

        content = self.get_content_by_url(url)

        pattern = "'X-CSRF-Token', '(.*?)'"
        token = common.get_first_group_by_pattern(content, pattern)

        return token

    def get_lyric_raw_json(self, id, token):
        if not id:
            return None

        actionUrl = 'https://petitlyrics.com/com/get_lyrics.ajax'
        headers = {
            'X-CSRF-Token': token,
            'X-Requested-With': 'XMLHttpRequest'
        }
        payload = {
            'lyrics_id': id,
        }

        content = self.get_content_by_url(actionUrl, payload, headers)
        try:
            obj = json.loads(content)
        except:
            return None

        return obj

    def get_lyric(self, id, token):
        if not id:
            return None

        obj = self.get_lyric_raw_json(id, token)
        if not obj:
            return None

        lyric_list = []
        for item in obj:
            lyric_list.append(base64.b64decode(item['lyrics']))

        return '\n'.join(lyric_list).decode('utf8', 'ignore')

    def parse_artist_title(self, html):
        startStr = '"description" content="'
        endStr = u'の歌詞ページです'

        infoStr = common.get_string_by_start_end_string(startStr, endStr, html)
        if not infoStr:
            return None

        infoStr = infoStr.replace(startStr, '')
        infoStr = infoStr.replace(endStr, '')
        infoStr = infoStr.strip()

        items = infoStr.split(' / ')

        if len(items) == 2:
            self.title = common.unicode2string(items[0])
            self.artist = common.unicode2string(items[1])

    def parse_lyricist(self, html):
        prefix = '<b>&#20316;&#35422;&#65306;</b>'
        suffix = '\t'

        logging.debug('find me LYRICIST')

        raw_string = common.find_string_by_prefix_suffix(html, prefix, suffix, False)
        if not raw_string:
            logging.debug('Failed to find lyricist')
            return False

        self.lyricist = common.htmlspecialchars_decode(common.unicode2string(raw_string)).strip()

    def parse_composer(self, html):
        prefix = '<b>&#20316;&#26354;&#65306;</b>'
        suffix = '\t'

        raw_string = common.find_string_by_prefix_suffix(html, prefix, suffix, False)
        if not raw_string:
            logging.debug('Failed to find composer')
            return False

        self.composer = common.htmlspecialchars_decode(common.unicode2string(raw_string)).strip()

    def get_content_by_url(self, url, payload=None, headers=None):
        return self.get_content_by_url_by_requests(url, payload, headers)
        #return self.get_content_by_url_by_urllib3(url, payload, headers)

    def get_content_by_url_by_requests(self, url, payload=None, headers=None):
        r = self.request_by_url_requests(url, payload, headers)
        if not r:
            return False
        return r.text

    def get_content_by_url_by_urllib3(self, url, payload=None, headers=None):
        r = self.request_by_url_urllib3(url, payload, headers)
        if not r:
            return False
        return r.data.decode('utf-8', 'ignore')

    def request_by_url_requests(self, url, payload=None, headers=None):
        import urllib3
        urllib3.disable_warnings()
        import requests

        proxies = {
            #'http': '192.168.1.34:8001',
            #'https': '192.168.1.34:8001'
        }

        if not hasattr(self, 'session'):
            self.session = requests.Session()

        if payload:
            r = self.session.post(url, data = payload, headers = headers, proxies=proxies, verify=False)
        else:
            r = self.session.get(url, proxies=proxies, verify=False)

        return r

    def request_by_url_urllib3(self, url, payload=None, headers=None):
        import urllib3
        urllib3.disable_warnings()

        if not hasattr(self, 'http'):
            self.http = urllib3.PoolManager()
            #self.http = urllib3.ProxyManager('http://192.168.1.34:8001')

        if hasattr(self, 'cookie'):
            if not headers:
                headers = {'Cookie': self.cookie}
                logging.debug('no headers in params, set cookie to %s' % (self.cookie))
            elif not hasattr(headers, 'Cookie'):
                headers['Cookie'] = self.cookie
                logging.debug('has headers params, set cookie to %s' % (self.cookie))
            else:
                logging.debug('## cookie in request headers')
        else:
            logging.debug('## no saved cookie')

        if payload:
            r = self.http.request_encode_body('POST', url, payload, headers, encode_multipart=False)
        else:
            r = self.http.request_encode_url('GET', url, payload, headers)

        logging.debug('== == == == ==')
        logging.debug('== request to url [%s]' % (url))

        cookie = r.getheader('Set-Cookie')
        if cookie:
            self.cookie = cookie
            logging.debug('Got Set-Cookie: %s from request to %s' % (cookie, url))

        return r

def get_lyric(url):
    obj = PetitLyrics(url)

    return obj.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url
    url = 'https://petitlyrics.com/lyrics/1175487'
    url = 'https://petitlyrics.com/lyrics/1015689'
    url = 'https://petitlyrics.com/lyrics/34690'

    full = get_lyric(url)
    if not full:
        print('Cannot get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
