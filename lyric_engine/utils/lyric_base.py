#/usr/bin/env python3
from utils import common

class LyricBase:
    def __init__(self, url):
        self.url = url
        self.title = None
        self.artist = None
        self.lyricist = None
        self.composer = None
        self.arranger = None
        self.lyric = None

    def get(self, url=None):
        if url:
            self.url = url

        if not self.parse_page():
            return None

        return self.get_full()

    def get_full(self):
        # template of full information
        template = []

        if self.title:
            template.append(self.title)
            template.append('')

        if self.artist:
            template.append('歌手：%s' % (self.artist))
        if self.lyricist:
            template.append('作詞：%s' % (self.lyricist))
        if self.composer:
            template.append('作曲：%s' % (self.composer))
        if self.arranger:
            template.append('編曲：%s' % (self.arranger))

        if len(template) > 2:
            template.append('')
            template.append('')
        template.append(self.lyric)

        return '\n'.join(template)

    def parse(self, url=None):
        # fetch self.url, and parse
        if url:
            self.url = url

        return self.parse_page()

    def parse_page(self):
        return True

    def set_attr(self, patterns, text):
        for key in patterns:
            pattern = patterns[key]
            value = common.get_first_group_by_pattern(text, pattern)

            if not value:
                ret = False
            else:
                value = common.htmlspecialchars_decode(value).strip()
                value = common.strip_tags(value)
                setattr(self, key, value)

    def get_from_azure(self, url):
        import requests
        import urllib.request, urllib.parse, urllib.error

        azure_url = 'https://franks543-lyric-get.azurewebsites.net/json?url=%s' % (
            urllib.parse.quote(url))
        r = requests.get(azure_url)

        obj = r.json()

        patterns = {
            'title': 'title',
            'artist': 'artist',
            'lyricist': 'lyricist',
            'composer': 'composer',
            'arranger': 'arranger',
            'lyric': 'lyric',
        }

        for pattern in patterns:
            if pattern not in obj:
                return False

            setattr(self, pattern, obj[pattern])

        return True
