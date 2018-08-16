# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '..', 'include')
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
