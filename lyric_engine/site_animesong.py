# -*- coding: utf8 -*-
import logging
import re
import common

site_index = 'animesong'
site_keyword = 'animesong'
site_url = 'http://www.jtw.zaq.ne.jp/animesong/'
test_url = 'http://www.jtw.zaq.ne.jp/animesong/ra/rahxephontagen/tune.html'
test_expect_length = 1609

def get_lyric(url):
    data = common.get_url_content(url)
    data = unicode(data, 'sjis')

    pattern = '<PRE>(.*)</PRE>'

    bool = re.compile(pattern, re.DOTALL).search(data)
    if bool:
        lyric = bool.group(1)
        return lyric.encode('utf-8')

    return None

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
