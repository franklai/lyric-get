# -*- coding: utf8 -*-
import logging
import re
import common

site_index = 'utaten'
site_keyword = 'utaten'
site_url = 'http://utaten.com/'
test_url = 'http://utaten.com/lyric/jb50903142'
test_url2 = 'http://utaten.com/lyric/lyric.php?LID=jb10508040'
test_expect_length = 1876

def get_lyric(url):
    prefix = 'http://utaten.com/lyric/load_text.php?LID='
    pattern = '((LID=)|(/lyric/))(?P<lid>[a-z]{2}[0-9]+)'

    bool = re.compile(pattern).search(url)
    if bool:
        id = bool.group('lid')
        full_url = prefix + id

        # get data
        data = common.get_url_content(full_url)

        data = unicode(data, 'sjis')
        lyric = data[1:]

        lyric = re.compile('[ \t]+\n').sub('\n', lyric) # delete trailing
        lyric = re.compile('\t *(.*)\n').sub(r'\n(\1)\n', lyric)
        lyric = re.compile('   +').sub(',', lyric)
        lyric = lyric.strip()

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

    string = '%s: test [%s]' % (status, site_index)
    print(string)
