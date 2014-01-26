# -*- coding: utf8 -*-
import logging
import re
import time
import common
from urllib import unquote
from xml.dom.minidom import parseString

site_index = 'yahoo'
site_keyword = 'yahoo'
site_url = 'http://music.yahoo.co.jp/lyrics/'
test_url = 'http://lyrics.gyao.yahoo.co.jp/ly/Y152097/'
test_expect_length = 1133

class YahooMusic:
    def __init__(self):
        self.lyric = None
        self.song_info = None
        self.cookie = None
        self.userAgent = 'lyric_get'
        self.headers = {'User-Agent': self.userAgent}
        
    def get_lyric(self, url):
        if not self.get_cookie(url):
            logging.warning('%s cannot get cookie' % (url, ))

        query = self.get_xml_parameters(url)
        if not query:
            return 'Failed to get XML parameters'
        logging.debug('XML parameters, query[%s]' % (query, ))

        # 3. get xml
        xml_str = self.get_xml(query)
        if not xml_str:
            return 'Cannot get xml'

        # 4. parse xml
        lyric = self.parse_xml(xml_str)

        return lyric

    def get_cookie(self, url):
        req = common.URL(url, data=None, headers=self.headers)
        info = req.get_info()

        if 'Set-Cookie' not in info:
            logging.debug('no Set-Cookie, info:%s' % (repr(info)))
            return None

        self.headers['Cookie'] = info['Set-Cookie']
        logging.debug('Cookie[%s]' % (self.headers['Cookie'], ))
        return self.headers['Cookie']

    def get_xml_parameters(self, url):
        bytes = common.get_url_content(url, headers=self.headers)

        pattern = "query +: +'([^']+)'"
        query = common.get_first_group_by_pattern(bytes, pattern)

        return query

    def get_xml(self, query):
        # http://rio.yahooapis.jp/RioWebService/V2/getLyrics?appid=7vOgnk6xg64IDggn6YEl3IQxmbj1qqkQzTpAx5nGwl9HnfPX3tZksE.oYhEw3zA-&lyrics_id=Y152097&results=1&multi_htmlspecialchars_flag=1
        xmlpath = 'http://rio.yahooapis.jp/RioWebService/V2/getLyrics?appid=%s&%s' % (
            '7vOgnk6xg64IDggn6YEl3IQxmbj1qqkQzTpAx5nGwl9HnfPX3tZksE.oYhEw3zA-', unquote(query)
        )
        
        bytes = common.get_url_content(xmlpath)

        return bytes

    def parse_xml(self, xml_str):
        doc = parseString(xml_str)

        def xml_get_name_attribute(doc, tagname):
            ret = None
            elements = doc.getElementsByTagName(tagname)
            if elements.length == 1:
                ret = elements.item(0).getAttribute('name')
            return ret

        def xml_get_first_child(doc, tagname):
            ret = None
            elements = doc.getElementsByTagName(tagname)
            if elements.length == 1:
                ret = elements.item(0).firstChild.nodeValue
            return ret

        def get_lyric(doc):
            lyric = xml_get_first_child(doc, 'Lyrics')
            lyric = unicode(lyric) 
            lyric = lyric.replace('<br>', '\r\n')

            return lyric

        def get_song_info(doc):
            artist = xml_get_first_child(doc, 'ArtistName')
            title = xml_get_first_child(doc, 'Title')
            lyric = xml_get_first_child(doc, 'WriterName')
            music = xml_get_first_child(doc, 'ComposerName')

            lines = []
            lines.append(u'%s\n' % (title))
            lines.append(u'歌手：%s' % (artist))
            lines.append(u'作詞：%s' % (lyric))
            lines.append(u'作曲：%s' % (music))

            lines.append('\n\n')

            string = '\n'.join(lines)

            logging.debug('info: %s' % (string, ))

            return string

        return get_song_info(doc) + get_lyric(doc)

def get_lyric(url):
    js = YahooMusic()

    lyric = js.get_lyric(url)

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
