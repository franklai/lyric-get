# -*- coding: utf8 -*-
import logging
import re
import common

site_index = 'utamap'
site_keyword = 'utamap'
site_url = 'http://www.utamap.com/'
test_url = 'http://www.utamap.com/showkasi.php?surl=70380'
test_expect_length = 1581

def get_lyric(url):
    prefix = 'http://www.utamap.com/phpflash/flashfalsephp.php?unum='
    pattern = 'surl=([^&=]+)'

    bool = re.compile(pattern).search(url)

    if bool:
        id = bool.group(1)
        full_url = prefix + id
        
        # get data
        data = common.get_url_content(full_url)
        logging.debug('url: %s' % (full_url, ))

        lyric = data.decode('utf-8', 'ignore')

        front_str = 'test2='
        if lyric.find(front_str) == -1:
            logging.debug('Failed to parse lyric')
            return ''

        start = lyric.find(front_str) + len(front_str)
        lyric = lyric[start:]
        lyric = lyric.strip()

        # test for half to full
        lyric = common.half2full(lyric)

        song_info = _get_song_info(url)
        lyric = song_info + lyric

        return lyric.encode('utf-8')

    return None

def _get_song_info(url):
    data = common.get_url_content(url)

    # web page has sjis in html, but actually is euc_jp...
    encoding = 'euc_jp'
    html = data.decode(encoding, 'ignore')

    def getValue(key, content):
        pattern = u'<INPUT type="hidden" name=%s value="([^"]*)">' % (key, )
        value = common.get_first_group_by_pattern(content, pattern)
        return value

    title = getValue('title', html)
    artist = getValue('artist', html)
    sakusi = getValue('sakusi', html)
    sakyoku = getValue('sakyoku', html)

    lines = []

    lines.append(u'%s' % (title))
    lines.append(u'')
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
