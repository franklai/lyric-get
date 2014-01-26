# -*- coding: utf8 -*-
import logging
import re
import common

site_index = 'animap'
site_keyword = 'animap'
site_url = 'http://www.animap.jp/'
test_url = 'http://www.animap.jp/kasi/showkasi.php?surl=dk101202_50'
test_expect_length = 1660

def get_lyric(url):
    prefix = 'http://www.animap.jp/kasi/phpflash/flashphp.php?unum='
    pattern = 'surl=([^&=]+)'

    id = common.get_first_group_by_pattern(url, pattern)
    if id:
        full_url = prefix + id
        
        # get data
        data = common.get_url_content(full_url)

        front_str = 'test2='
        start = data.find(front_str) + len(front_str)
        lyric = data[start:]
        lyric = lyric.decode('sjis', 'ignore')
        lyric = lyric.strip()

        # test for half to full
        lyric = common.half2full(lyric)

        song_info = _get_song_info(url)
        lyric = song_info + lyric

        return lyric.encode('utf-8')

    return None

def get_info_value_by_key(html, key):
    valuePrefix = '#ffffff>&nbsp;'
    valueSuffix = '</TD>'
    lenPrefix = len(valuePrefix)
    posKey = html.find(key)
    logging.debug('key position: %d' % (posKey))

    posStart = html.find(valuePrefix, posKey) + lenPrefix
    posEnd = html.find(valueSuffix, posStart)
    logging.debug('position [%d:%d]' % (posStart, posEnd))

    value = html[posStart:posEnd]
    
    return value

def _get_song_info(url):
    html = common.get_url_content(url)

    encoding = 'euc_jp'
    html = html.decode(encoding, 'ignore')

    artist = get_info_value_by_key(html, u'歌手</TD>')
    sakusi = get_info_value_by_key(html, u'作詞</TD>')
    title  = get_info_value_by_key(html, u'曲名</TD>')
    sakyoku= get_info_value_by_key(html, u'作曲</TD>')

    lines = []
    lines.append(u'%s\n' % (title))
    lines.append(u'歌手：%s' % (artist))
    lines.append(u'作詞：%s' % (sakusi))
    lines.append(u'作曲：%s' % (sakyoku))

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
