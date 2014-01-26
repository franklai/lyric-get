# -*- coding: utf8 -*-
import logging
import re
import common

site_index = 'kasi_time'
site_keyword = 'kasi-time'
site_url = 'http://www.kasi-time.com/'
test_url = 'http://www.kasi-time.com/item-262.html'
test_expect_length = 1581

def get_lyric(url):
    prefix = 'http://www.kasi-time.com/item_js.php?no='
    pattern = 'item-([0-9]+)\.html'

    bool = re.compile(pattern).search(url)

    if bool:
        id = bool.group(1)
        full_url = prefix + id
        
        # get data
        try:
            data = common.get_url_content(full_url)
        except IOError:
            raise

        lyric = unicode(data, 'utf-8')
        lyric = lyric.replace("document.write('", "")
        lyric = lyric.replace("');", "")
        lyric = lyric.replace("<br>", "\n")
        lyric = lyric.replace("&nbsp;", " ")
        lyric = re.sub(r'\\(.)', r'\1', lyric) # as stripslashes() in PHP
        lyric = lyric.strip()


        # test for half to full
        lyric = common.half2full(lyric)


        song_info = _get_song_info(url)
        lyric = song_info + lyric
            
        return lyric.encode('utf-8')

    return None

def _get_song_info(url):
    data = common.get_url_content(url)

    encoding = 'utf-8'
    html = data.decode(encoding, 'ignore')

    prefix = '<div id="song_info_table">'
    suffix = '</div>'
    infoTable = common.get_string_by_start_end_string(prefix, suffix, html)

    pattern = '<h1>(.*)</h1>'
    title = common.get_first_group_by_pattern(html, pattern).strip()

    def getValue(key, content):
        prefix = u'<td class="td1">%s</td>' % (key)
        suffix = '</a></td>'

        tdValue = common.get_string_by_start_end_string(prefix, suffix, content)
        logging.debug('[%s] td value is [%s]' % (key, tdValue))
        return common.strip_tags(tdValue[len(prefix):]).strip()

    artist = getValue(u'歌手', infoTable)
    lyric = getValue(u'作詞', infoTable)
    music = getValue(u'作曲', infoTable)

    lines = []
    lines.append(u'%s\n' % (title))
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

    string = '%s: test [%s]' % (status, site_index)
    print(string)

    print(repr(result))
