# -*- coding: utf8 -*-
import logging
import re
import common

site_index = 'petitlyrics'
site_keyword = 'petitlyrics'
site_url = 'http://petitlyrics.com/'
test_url = 'http://petitlyrics.com/kashi/34690/'
test_url = 'http://petitlyrics.com/kashi/914583/'
test_expect_length = 1275

'''
    Request URL
        http://petitlyrics.com/kashi/action
    Method
        POST
    Data
        id=34690

    Response

    &#x305d;&#x308c;&#x3067;&#x3082;&#x3082;&#x3046;&#x5927;&#x4e08;&#x592b;&#x0020;&#x6e80;&#x305f;&#x3055;&#x308c;&#x305f;&#x304b;&#x3089;&#x000d;<br />
    &#x000d;<br />
'''
class PetitLyrics:
    def __init__(self):
        self.artist = ''
        self.title = ''
        self.composer = ''
        self.lyricist = ''

    def get_lyric(self, url):
        # 1. get song id from url
        id = self.get_song_id(url)

        # 2. get 1st part lyric from html and song_info
        html = self.get_html(url)
        lyric_1st = self.get_lyric_1st_part(html)
        song_info = self.get_song_info(html)

        # 2. get second part lyric
        lyric_2nd = self.get_lyric_2nd_part(id, url)

        result = song_info + lyric_1st + lyric_2nd

        # handle special char
        result = common.htmlspecialchars_decode(result)

        return result

    def get_html(self, url):
        return common.get_url_content(url).decode('utf-8', 'ignore')

    def format_lyric_from_raw(self, html):

        return lyric

    def get_lyric_1st_part(self, html):
        prefix = '<pre id="lyrics" class="viwe_lyrics">'
        suffix = '</pre>'

        rawLyric = common.get_string_by_start_end_string(prefix, suffix, html)
        encodedLyric = common.strip_tags(rawLyric)
        lyric_1st = common.unicode2string(encodedLyric)

        return lyric_1st

    def get_song_id(self, url):
        if not url:
            return None

        pattern = '/kashi/([0-9]+)'
        id = common.get_first_group_by_pattern(url, pattern)

        return id

    def get_lyric_2nd_part(self, id, url):
        if not id:
            return None

        actionUrl = 'http://petitlyrics.com/kashi/action'
        postData = 'id=%s' % (id, )
        headers = {
            'Referer': url
        }
        html = common.get_url_content(actionUrl, data=postData, headers=headers)

        rawLyric = common.unicode2string(html)

        lyricWithBr = re.sub('[\r\n]', '', rawLyric)

        lyric = lyricWithBr.replace('<br />', '\n')
        lyric = lyric.strip()

        return lyric

    def get_song_info(self, html):
        # get artist and title from original url
        # parse lyricist and composer from lyricHtml

        self.get_artist_title(html)

        self.get_lyricist_composer(html)

        lines = []

        lines.append(u'%s\n' % (self.title))
        lines.append(u'%s：%s' % (u'歌手', self.artist))
        if self.lyricist:
            lines.append(u'%s：%s' % (u'作詞', self.lyricist))
        if self.composer:
            lines.append(u'%s：%s' % (u'作曲', self.composer))
        lines.append('\n\n')

        songInfo = '\n'.join(lines)
        logging.debug('song info: %s' % (songInfo, ))

        return songInfo

    def get_artist_title(self, html):
        startStr = '<div id="main_title">'
        endStr = '</div>'

        infoStr = common.get_string_by_start_end_string(startStr, endStr, html)

        infoStr = infoStr.replace(startStr, '')
        infoStr = infoStr.replace(endStr, '')
        infoStr = infoStr.strip()

        items = infoStr.split('&nbsp;/&nbsp;')

        if len(items) == 2:
            self.title = items[0]
            self.artist = items[1]
        else:
            self.title = ''
            self.artist = ''

        return self.artist, self.title

    def get_lyricist_composer(self, lyricHtml):
        startStr = '<td width="340" align="right" colspan="2">'
        endStr = '</td>'

        infoAreaStr = common.get_string_by_start_end_string(startStr, endStr, lyricHtml)
        if not infoAreaStr:
            logging.debug('Failed to find lyricist/composer area')
            return None

        infoAreaStr = infoAreaStr.strip()
        logging.debug('lyricist/composer area str: %s' % (infoAreaStr, ))

        pattern = u'作詞：([^<]+)&nbsp;&nbsp;作曲：([^<]+)'
        regex = re.compile(pattern).search(infoAreaStr)
        if regex:
            self.lyricist = regex.group(1)
            self.composer = regex.group(2)
            logging.debug('Matched lyricist: %s, composer: %s' % (self.lyricist, self.composer))
        else:
            logging.debug('Failed to match lyricist/composer area pattern')
            return None

        return self.lyricist, self.composer

def get_lyric(url):
    obj = PetitLyrics()

    lyric = obj.get_lyric(url)

    return lyric.encode('utf-8')

def test_site():
    result = {}
    success = False

    lyric = get_lyric(test_url)
    logging.debug('test url return length: %d, expect: %d' % (len(lyric), test_expect_length))
    if len(lyric) == test_expect_length:
        success = True

    result['name'] = site_index
    result['url'] = test_url
    result['lyric'] = lyric
    result['success'] = success

    return result

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    result = test_site()

    status = 'Failed'
    if result and result['success']:
        status = 'OK'

    string = '%s: test [%s]' % (status, site_index)
    print(string)

#     print(repr(result))
