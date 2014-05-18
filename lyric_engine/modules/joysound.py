# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import common
from lyric_base import LyricBase

site_class = 'JoySound'
site_index = 'joysound'
site_keyword = 'joysound'
site_url = 'http://joysound.com/'
test_url = 'http://joysound.com/ex/search/karaoke/_selSongNo_28721_songwords.htm'
test_expect_length = 1551

class JoySound(LyricBase):
    def read_config(self):
        try:
            import config
            cfg = config.Config()
            self.id = cfg.get('joysound', 'id')
            self.password = cfg.get('joysound', 'password')
        except:
            self.id = ''
            self.password = ''
            logging.info('no config for joysound account')

    def parse_page(self):
        url = self.url

        self.read_config()

        # get necessary cookie by login
        if not self.do_login():
            logging.info('Failed to login to joysound')
            return False

        # convert url if not lyric page
        converted_url = self.convert_url(url)
        if not url:
            logging.info('Failed to get converted url from [%s]' % (url))
            return False
        
        # retrieve lyric page
        sdata = self.get_sdata(converted_url)
        if not sdata:
            logging.info('Failed to get sdata of url [%s]' % (url))
            return False

        # retrieve real lyric content through AMF protocol
        raw_lyric = self.get_raw_lyric(sdata)
        if not raw_lyric:
            logging.info('Failed to get raw data of url [%s]' % (url))
            return False

        if not self.parse_lyric(raw_lyric):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.parse_song_info(raw_lyric):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def send_request(self, url, data=None, headers=None):
        obj = common.URL(url, data, headers)
        return obj

    def do_login(self):
        """
        Login Joysound.com, 
        get 2 important Cookie values and save it in self.cookie
        """
        url = 'http://joysound.com/ex/utasuki/forwardLogin.htm'
        data = 'loginId=%s&loginPass=%s' % (self.id, self.password, )
        headers = {}

        handle = self.send_request(url, data, headers)
        if not handle:
            # something error
            logging.info('damn, login failed')
            return False
            
        headers = handle.get_info()

        self.cookie = self.get_cookie(headers)

        logging.debug('headers=%s' % (str(headers)))
        logging.debug('self.cookie=%s' % (self.cookie))

        return True

    def get_cookie(self, headers):
        cookie = ''

        if 'set-cookie' in headers:
            cookie = headers['set-cookie']
        else:
            raise

        return cookie

    def convert_url(self, url):
        # convert URL if not lyric page
        # http://joysound.com/ex/search/song.htm?gakkyokuId=344513
        # http://joysound.com/ex/search/karaoke/_selSongNo_124645_songwords.htm

        lyric_page_pattern = '(/ex/search/karaoke/_selSongNo_[0-9]+_songwords.htm)'

        song_page_pattern = '/ex/search/song.htm\?gakkyokuId=([0-9]+)'
        id = common.get_first_group_by_pattern(url, song_page_pattern)
        if id:
            # song page pattern, get this page and parse id
            html = common.get_url_content(url)

            relative_url = common.get_first_group_by_pattern(html, lyric_page_pattern)
           
            return urlparse.urljoin(url, relative_url)
            
        return url
    
    def get_sdata(self, url):
        """
        Load the Lyric Page
        find the sdata for this lyric
        """
        data = None
        headers = {
            'Cookie': self.cookie,
        }

        handle = self.send_request(url, data, headers)
        logging.debug('sent request with cookie: %s' % (self.cookie.encode('utf8')))
        
        html = handle.get_content()

        # do parsing
        sdata = None
        pattern = 'viewLyrics\.swf\?sd=([^"]+)'
        sdata = common.get_first_group_by_pattern(html, pattern)

        logging.debug('sdata=%s' % (str(sdata)))

        return sdata

    def get_raw_lyric(self, sdata):
        """
        With sdata, load the lyric
        Action Message Format
        """
        if sdata == None:
            return None

        prefix = '\0\0\0\0\0\1\0\x1a'
        url = 'http://www.lyriget.jp/flashservices/gateway'
        data = '%s%s\0\2/1\0\0\0\x33\x0a\0\0\0\1\3\0\5sData\2\0 %s\0\0\x09' % (
            prefix, 'xing_cfc.songdata.get_data', sdata
        )
        headers = {
            'Content-Type': 'application/x-amf',
        }

        handle = self.send_request(url, data, headers)

        return handle.get_content()
    
    def parse_raw_lyric(self, raw_lyric):
        if raw_lyric == None:
            return None

        # song info
        lyric = self.get_song_info('KAS', raw_lyric)

        lines = []

        lines.append(u'%s\n' % (title))
        lines.append(u'%s：%s' % (u'歌手', artist))
        lines.append(u'%s：%s' % (u'作詞', lyricist))
        lines.append(u'%s：%s' % (u'作曲', music))
        lines.append('\n\n')

        song_info = '\n'.join(lines)

        lyric = song_info + lyric.strip()

        return lyric

    def parse_lyric(self, raw_lyric):
        lyric = self.get_song_info('KAS', raw_lyric)

        self.lyric = lyric.strip()

        return True

    def parse_song_info(self, raw_lyric):
        ret = True

        patterns = {
            'title': 'MNM',
            'artist': 'KNM',
            'lyricist': 'SINM',
            'composer': 'SKNM',
        }

        for key in patterns:
            pattern = patterns[key]

            value = self.get_song_info(pattern, raw_lyric)

            if value:
                setattr(self, key, value)
            else:
                logging.warning('Failed to get %s', key)
                ret = False

        return ret

    def get_song_info(self, prefix, raw_lyric):
        start = raw_lyric.find(prefix) + len(prefix) + 3
        end = raw_lyric.find('\0', start)
        result = raw_lyric[start:end].decode('utf8')

        return result

def get_lyric(url):
    obj = JoySound(url)

    return obj.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Cannot get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))

