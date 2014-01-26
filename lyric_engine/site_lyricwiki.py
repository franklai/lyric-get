# -*- coding: utf8 -*-
import logging
import re
import common

site_index = 'lyricwiki'
site_keyword = 'lyrics.wikia'
site_url = 'http://lyrics.wikia.com/'
# test_url = u'http://lyrics.wikia.com/ナイトメア_(Nightmare):レゾンデートル'.encode('utf8')
test_url = 'http://lyrics.wikia.com/Ronan_Keating:When_You_Say_Nothing_At_All'
test_expect_length = 1386

class LyricWiki:
    def __init__(self):
        self.lyric = None
        self.song_info = None

    def get_lyric(self, url):
        html = self.get_html(url)

        lyric = self.parse_lyric(html)

        info = self.parse_info(html)

        lyric = '%s\n\n\n%s' % (info, lyric)

        return lyric

    def get_html(self, url):
        encoding = 'utf8'

        bytes = common.get_url_content(url)
        html = bytes.decode(encoding, 'ignore')
        return html

    def parse_lyric(self, html):
        pattern = '</div>(&#.*)<!--'
        items = re.findall(pattern, html)
        logging.debug(repr(items))

        lyrics = []
        for item in items:
            string = item.replace('<br />', '\n')

            string += '\n'
            lyrics.append(string)
        lyric = '\n'.join(lyrics)

        lyric = common.unicode2string(lyric).strip()
        return lyric

    def parse_info(self, html):
        pattern = '<meta property="og:title" content="([^"]+)" />'
        ogTitle = common.get_first_group_by_pattern(html, pattern)

        artist, title = ogTitle.split(':')

        info = '%s\n\nArtist: %s' % (title, artist)
        return info
        
# 
# def get_lyric(url):
# 
#     pattern = 'wgTitle="([^"]+)"'
#     wgTitle = common.get_first_group_by_pattern(html, pattern)
#     logging.debug(repr(wgTitle))
# 
#     artist = ''
#     title = ''
#     infos = wgTitle.split(':')
#     if len(infos) >= 2:
#         artist = infos[0]
#         title = infos[1]
# 
# 
#     lines.append('\n\n')
#     lines.append('%s' % (lyric, ))
# 
#     lyric = '\n'.join(lines)
#     lyric = u'%s\n\nArtist: %s\n\n\n%s' % (title, artist, '\n\n'.join(lyrics))
# 
#     # convert &#115; to unicode character
#     def code_point_to_char(matchobj):
#         if matchobj.group(1):
#             return unichr(int(matchobj.group(1)))
#     pattern = '&#([0-9]+);'
#     lyric = re.sub(pattern, code_point_to_char, lyric)
# 
#     return lyric

def get_lyric(url):
    obj = LyricWiki()

    lyric = obj.get_lyric(url)

    return lyric.encode('utf-8')

def _get_song_info(url):
    pass

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
