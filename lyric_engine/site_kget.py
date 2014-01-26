# -*- coding: utf8 -*-
import logging
import re
import common

site_index = 'kget'
site_keyword = 'kget'
site_url = 'http://www.kget.jp/'
test_url = 'http://www.kget.jp/lyric/11066/'
test_expect_length = 1513

def get_lyric(url):
    # get lyric page first
    html = common.get_url_content(url)
    if not html:
        return None

    html = html.decode('utf-8', 'ignore')

    prefix = '<div id="lyric-trunk">'
    suffix = '</div>'
    rawLyric = common.get_string_by_start_end_string(prefix, suffix, html)
    lyric = common.strip_tags(rawLyric)

    lyric = common.unicode2string(lyric).strip()

    songInfo = _get_song_info_by_content(html)
    lyric = songInfo + lyric

    return lyric.encode('utf-8')

def _get_song_info_by_content(html):
    prefix = '<table class="lyric-data">'
    suffix = '</table>'
    infoTable = common.get_string_by_start_end_string(prefix, suffix, html)
    infoTable = infoTable.replace('\n', '')

    pattern = '">([^<]*)</a></td></tr>'
    artist = common.get_first_group_by_pattern(infoTable, pattern)

    pattern = 'td>([^<]*)<br></td></tr><tr>'
    lyric = common.get_first_group_by_pattern(infoTable, pattern)

    pattern = 'td>([^<]*)<br></td></tr></table>'
    music = common.get_first_group_by_pattern(infoTable, pattern)

    prefix = '<div id="status-heading">'
    suffix = '</div>'
    titleDiv = common.get_string_by_start_end_string(prefix, suffix, html)
    pattern = '<h1>(.*)</h1>'
    title = common.get_first_group_by_pattern(titleDiv, pattern)

    lines = []
    lines.append(u'%s' % (title))
    lines.append(u'')
    lines.append(u'歌手：%s' % (artist))
    lines.append(u'作詞：%s' % (lyric))
    lines.append(u'作曲：%s' % (music))

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
    else:
        print(repr(result))

    string = '%s: test [%s]' % (status, site_index)
    print(string)

