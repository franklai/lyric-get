# -*- coding: utf8 -*-
import logging
import re
import common

site_index = 'j_total'
site_keyword = 'j-total'
site_url = 'http://music.j-total.net/'
test_url = 'http://music.j-total.net/data/026ha/012_BUMP_OF_CHICKEN/014.html'
test_expect_length = 3592

def get_lyric(url):
    bytes = common.get_url_content(url)

    encoding = 'sjis'
    html = bytes.decode('sjis', 'ignore')

    prefix_func = 'hp_d00("'
    prefix_escaped = '\\x3C\\x21\\x2D\\x2D'
    prefix = prefix_func + prefix_escaped
    suffix = '");//--></SCRIPT>'

    start = html.find(prefix)
    if start == -1:
        # failed to find prefix
        return None

    start += len(prefix_func)

    end = html.find(suffix, start)
    if end == -1:
        # failed to find suffix
        return None

    escaped_string = html[start: end]

    def unescape(matchobj):
        if matchobj.group(1):
            return chr(int(matchobj.group(1), 16))
    pattern = r'\\x([0-9A-F]+)'
    lyric_with_tag = re.sub(pattern, unescape, escaped_string)

    # remove <a href>, </a>, <!-- -->
    pattern = '<[/a!][^>]+>'
    lyric_with_tag = re.compile(pattern).sub('', lyric_with_tag)

    # remove front spaces
    pattern = '(  +)'
    lyric_with_tag = re.compile(pattern).sub('', lyric_with_tag)

    # remove CR, LF
    lyric_with_tag = lyric_with_tag.replace(' \r\n', ' ')

    # replace <br> with new line
    lyric = lyric_with_tag.replace('<br>\r\n', '\n')

    def get_song_info(html):
        pattern = u'<font color="#FFFFFF"><b>　([^<]+)</b>'
        regex = re.compile(pattern).search(html)
        if regex:
            title = regex.group(1)
            return title

        return ''

    song_info = get_song_info(html) 
    if song_info:
        lyric = song_info + '\n\n\n' + lyric

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
