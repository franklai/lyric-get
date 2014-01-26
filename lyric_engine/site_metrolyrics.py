# -*- coding: utf8 -*-
import logging
import re
import common

site_index = 'metrolyrics'
site_keyword = 'metrolyrics'
site_url = 'http://www.metrolyrics.com/'
test_url = 'http://www.metrolyrics.com/we-belong-together-lyrics-mariah-carey.html'
test_expect_length = 2186

def get_lyric(url):
    encoding = 'utf8'

    logging.debug('url [%s]' % (url, ))

    bytes = common.get_url_content(url)
    html = bytes.decode(encoding, 'ignore')

    pattern = 'rm_artist = "(.*)"'
    artist = common.get_first_group_by_pattern(html, pattern)

    pattern = 'rm_songtitle = "(.*)"'
    title = common.get_first_group_by_pattern(html, pattern)

    logging.debug('artist [%s], title [%s]' % (artist, title, ))

    prefix = '<div id="lyrics-body">'
    suffix = '</div>'
    rawLyric = common.get_string_by_start_end_string(prefix, suffix, html)

    rawLyric = rawLyric.replace('<br />', '\n')
    rawLyric = common.strip_tags(rawLyric).strip()

    pattern = '(\[ From: http://www.metrolyrics.com/.*.html \])'
    extra = common.get_first_group_by_pattern(rawLyric, pattern)
    if extra:
        rawLyric = rawLyric.replace(extra, '')

#     lyric = u'%s\n\nArtist: %s\n\n\n%s' % (title, artist, rawLyric)
    lyric = u'%s\n\n\n%s' % (title, rawLyric)

    lyric = common.unicode2string(lyric)

    return lyric.encode('utf-8')

def find_all_song(url):
    html = common.get_url_content(url)
    
    # http://www.uta-net.com/song/113654/
#     pattern = 'href="(/song/[0-9]+/)"'
    pattern = 'href="(.*)" title=".* Lyrics"><span'
    song_ids = re.findall(pattern, html)

    url_prefix = 'http://www.metrolyrics.com'
    song_urls = [url_prefix + id for id in song_ids]

    return song_urls

def _output_album(album_url):
    song_urls = find_all_song(album_url)
    print(song_urls) 

    index = 1
    out = open('metro_lyrics.result.txt', 'wb')
    for item in song_urls:
        print('getting song of %s' % (item))
        lyric = get_lyric(item)

        out.write('%d. ' % (index))
        out.write(lyric.encode('utf8'))
        out.write('\n')
        out.write('\n')
        out.write('=====\n')

        index += 1

    out.close()

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

#     album_url = 'http://www.metrolyrics.com/21-album-adele.html'
#     _output_album(album_url)

#     print(repr(result))

# vim: expandtab
