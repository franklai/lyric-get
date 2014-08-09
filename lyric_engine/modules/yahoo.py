# -*- coding: utf8 -*-
import os
import sys
from urllib import unquote
from xml.dom.minidom import parseString
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import common
from lyric_base import LyricBase

site_class = 'Yahoo'
site_index = 'yahoo'
site_keyword = 'yahoo'
site_url = 'http://lyrics.gyao.yahoo.co.jp/'
test_url = 'http://lyrics.gyao.yahoo.co.jp/ly/Y152097/'

class Yahoo(LyricBase):
    def parse_page(self):
        url = self.url

        query = self.get_xml_parameters(url)
        if not query:
            logging.info('Failed to get query of url [%s]', url)
            return False

        logging.debug('XML parameters, query[%s]', query)

        # 3. get xml
        xml_str = self.get_xml(query)
        if not xml_str:
            logging.info('Failed to get xml of url [%s]', url)
            return False

        # 4. parse xml
        if not self.parse_xml(xml_str):
            logging.info('Failed to parse xml of url [%s]', url)
            return False

        return True

    def get_xml_parameters(self, url):
        bytes = common.get_url_content(url)

        pattern = "query +: +'([^']+)'"
        query = common.get_first_group_by_pattern(bytes, pattern)

        return query

    def get_xml(self, query):
        # http://rio.yahooapis.jp/RioWebService/V2/getLyrics?appid=7vOgnk6xg64IDggn6YEl3IQxmbj1qqkQzTpAx5nGwl9HnfPX3tZksE.oYhEw3zA-&lyrics_id=Y152097&results=1&multi_htmlspecialchars_flag=1
        xmlpath = 'http://rio.yahooapis.jp/RioWebService/V2/getLyrics?appid=%s&%s' % (
            '7vOgnk6xg64IDggn6YEl3IQxmbj1qqkQzTpAx5nGwl9HnfPX3tZksE.oYhEw3zA-', unquote(query)
        )
        
        bytes = common.get_url_content(xmlpath)

        logging.debug(bytes)

        return bytes

    def xml_get_name_attribute(self, doc, tagname):
        ret = None
        elements = doc.getElementsByTagName(tagname)
        if elements.length == 1:
            ret = elements.item(0).getAttribute('name')
        return ret

    def xml_get_first_child(self, doc, tagname):
        ret = None
        elements = doc.getElementsByTagName(tagname)
        if elements.length == 1:
            ret = elements.item(0).firstChild.nodeValue
        return ret

    def parse_xml(self, xml_str):
        doc = parseString(xml_str)

        def get_lyric(doc):
            lyric = self.xml_get_first_child(doc, 'Lyrics')
            lyric = unicode(lyric) 
            lyric = lyric.replace('<br>', '\r\n')

            return lyric


        self.lyric = get_lyric(doc)
        self.find_song_info(doc)

        return True

    def find_song_info(self, doc):
        ret = True

        patterns = {
            'title': 'Title',
            'artist': 'ArtistName',
            'lyricist': 'WriterName',
            'composer': 'ComposerName',
        }

        for key in patterns:
            tag = patterns[key]

            value = self.xml_get_first_child(doc, tag)

            if not value:
                logging.info('Failed to get %s of url [%s]', key, url)
                ret = False
            else:
                value = common.htmlspecialchars_decode(value).strip()
                setattr(self, key, value)

        return ret
            

def get_lyric(url):
    obj = Yahoo(url)

    return obj.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
