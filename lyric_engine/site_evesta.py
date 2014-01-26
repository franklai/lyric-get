# -*- coding: utf8 -*-
import logging
import re
import common

site_index = 'evesta'
site_keyword = 'evesta'
site_url = 'http://www.evesta.jp/lyric/'
test_url = 'http://www.evesta.jp/lyric/artists/a10019/lyrics/l7811.html'
test_expect_length = 1385

def get_lyric(url):
    data = common.get_url_content(url)
    data = data.decode('utf-8', 'ignore')

    pattern = "<div class='body'>(\r\n)+<p>(.*?)</p>"

    bool = re.compile(pattern, re.DOTALL).search(data)
    if bool:
        lyric = bool.group(2)
        lyric = lyric.replace('<br />', '')
        lyric = lyric.strip()
        lyric = common.unicode2string(lyric)

        # test for half to full
        lyric = common.half2full(lyric)

        song_info = _get_song_info_by_data(data)
        lyric = song_info + lyric

        return lyric.encode('utf-8')
    else:
        logging.debug('html pattern failed.')

    return None

def _get_song_info_by_data(data):
    title = ''
    artist = ''
    lyricist = ''
    music = ''

    pattern = u'<title>(.+?) 歌詞 / .*</title>'
    bool = re.compile(pattern).search(data) 
    if bool:
        title = bool.group(1)
    pattern = u"<div class='artists'>歌：(.*)　作詞：(.*)　作曲：(.*)</div>"
    bool = re.compile(pattern).search(data) 
    artist  = ''
    sakusi = ''
    sakyoku = ''
    if bool:
        artist = bool.group(1)
        sakusi = bool.group(2)
        sakyoku = bool.group(3)

    lines = []
    lines.append(u'%s\n' % (title))
    lines.append(u'作詞：%s' % (sakusi))
    lines.append(u'作曲：%s' % (sakyoku))
    lines.append(u'唄：%s' % (artist))

    lines.append('\n\n')

    string = '\n'.join(lines)

    return string

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
