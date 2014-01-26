# -*- coding: utf8 -*-
import re
try:
    import zlib
except:
    pass
import time
import logging
import os
import common

site_index = 'kashinavi'
site_keyword = 'kashinavi'
site_url = 'http://www.kashinavi.com/'
test_url = 'http://www.kashinavi.com/song_view.html?12462'
test_expect_length = 1560

def get_lyric(url, count=0):
    post_url = 'http://www.kashinavi.com/cgi-bin/kashi.cgi'

    # get file_no first
    pattern = '\?([0-9]+)'
    bool = re.compile(pattern).search(url)

    # no file_no, invalid url
    if not bool:
        return None

    id = bool.group(1)

    # get parameter from Flash
    para = get_hidden_para()

    # concatenate HTTP POST query
    query = '%s%s&time=%s' % (para['query_prefix'], id, time.localtime(), )

    logging.debug('query:%s' % (query, ))
    
    # get raw data of lyric
    data = common.get_url_content(post_url, query)

    lyric = unicode(data, 'utf8')

    logging.debug('lyric:%s' % (lyric, ))

    # if parsing rule changed, return debug info
    if lyric.find(u'歌詞ナビTOPページより') > 0:
        lyric = '''
Site rule changed!
Please contact franklai
LoadVars::%s::myLoadVars
''' % (para['middle_value'])
    
    # else remove the useless part and return lyric
    front_str = 'kashi='
    start = lyric.find(front_str) + len(front_str)
    lyric = lyric[start:]
    lyric = lyric.strip()

    view_html = common.get_url_content(url)
    song_info = _get_song_info_by_dat(view_html)

    lyric = song_info + lyric

    return lyric.encode('utf-8')

def get_hidden_para():
    """ get new hidden parameters of kashinavi. need zlib support. """ 
    url = 'http://www.kashinavi.com/song_view.swf'

    # add random value to avoid Google cache old value
    url = '%s?time=%.0f' % (url, time.time())
    logging.debug('url:%s' % (url, ))

    data = common.get_url_content(url)

    if data[0:3] == 'CWS':
        # compressed swf
        compressed_str = data[8:]
        uncompressed_str = zlib.decompress(compressed_str)
    elif data[0:3] == 'FWS':
        # uncompressed swf
        uncompressed_str = data
    else:
        # not valid swf, just return
        return

    prefix = '\0LoadVars\0'
    suffix = '\0myLoadVars'

    u = uncompressed_str 
    m = u[u.find(prefix)+len(prefix): u.find(suffix)]
    items = m.split('\0')

    para_name = 'something'
    para_value = 'is'
    # wrong

    if len(items) == 3:
        target_name = items[1]
        target_value = items[2]
        
    middle_value = m.replace('\0', ' ')

    query_prefix = '%s=%s&file_no=' % (target_name, target_value,)

    para = {
        'query_prefix': query_prefix,
        'middle_value': middle_value,
    }

    logging.debug('query_prefix:%s' % (query_prefix, ))

    return para

def _get_song_info_by_dat(data):
    encoding = 'sjis'
    html = data.decode(encoding, 'ignore')

    prefix = '<table border=0 cellpadding=0 cellspacing=5>'
    suffix = '</td></table>'
    infoString = common.get_string_by_start_end_string(prefix, suffix, html)

    title = common.strip_tags(
        common.get_string_by_start_end_string('<td>', '</td>', infoString)
    )

    artist = common.strip_tags(
        common.get_string_by_start_end_string('<td><a href=', '</a></td>', infoString)
    )

    prefix = '<table border=0 cellpadding=0 cellspacing=0>'
    suffix = '</td></table>'
    lyricAndMusic = common.get_string_by_start_end_string(prefix, suffix, infoString)

    pattern = u'作詞　：　(.*)<br>'
    lyric = common.get_first_group_by_pattern(lyricAndMusic, pattern)

    pattern = u'作曲　：　(.*)</td>'
    music = common.get_first_group_by_pattern(lyricAndMusic, pattern)

    lines = []
    lines.append(u'%s\n' % (title))
    lines.append(u'%s：%s' % (u'歌手', artist))
    lines.append(u'%s：%s' % (u'作詞', lyric))
    lines.append(u'%s：%s' % (u'作曲', music))

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
