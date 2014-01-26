# -*- coding: utf8 -*-
import logging
import re
import urlparse
import common

site_index = 'joysound'
site_keyword = 'joysound'
site_url = 'http://joysound.com/'
test_url = 'http://joysound.com/ex/search/karaoke/_selSongNo_28721_songwords.htm'
test_expect_length = 1551

class Joysound:
    def __init__(self):
        self.lyric = None
        self.song_info = None
        self.cookie = []

        self.read_config()

    def read_config(self):
        try:
            import config
            cfg = config.Config()
            self.id = cfg.get('joysound', 'id')
            self.password = cfg.get('joysound', 'password')
        except:
            self.id = ''
            self.password = ''

    def get_lyric(self, url):
        # 1. get necessary cookie by login
        self.do_login()

        # convert url if not lyric page
        url = self.convert_url(url)
        
        # 2. retrieve lyric page
        sdata = self.get_sdata(url)

        # 3. retrieve real lyric content through AMF protocol
        raw_lyric = self.get_raw_lyric(sdata)

        # 4. parse raw lyric
        lyric = self.parse_raw_lyric(raw_lyric)

        return lyric

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
            

        headers = handle.get_info()

        cookie = self.get_cookie(headers)
        self.cookie = ';'.join(cookie)

        logging.debug('headers=%s' % (str(headers)))
        logging.debug('self.cookie=%s' % (self.cookie))

    def get_cookie(self, headers):
        cookie = []

        if 'set-cookie' in headers:
            raw_cookie = headers['set-cookie']

            pattern = '(JSESSIONID=[^;]+)'
            obj = re.compile(pattern).search(raw_cookie)
            if obj:
                cookie.append(obj.group(1)) 
                
            pattern = '(AlteonP=[^;]+)'
            obj = re.compile(pattern).search(raw_cookie)
            if obj:
                cookie.append(obj.group(1)) 
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
        
        html = handle.get_content()

        # do parsing
        sdata = None
        pattern = 'viewLyrics\.swf\?sd=([^"]+)'
        regex = re.compile(pattern).search(html)
        if regex:
            sdata = regex.group(1)

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
        artist = self.get_song_info('KNM', raw_lyric)
        title = self.get_song_info('MNM', raw_lyric)
        lyricist = self.get_song_info('SINM', raw_lyric)
        music = self.get_song_info('SKNM', raw_lyric)
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

    def get_song_info(self, prefix, raw_lyric):
        start = raw_lyric.find(prefix) + len(prefix) + 3
        end = raw_lyric.find('\0', start)
        result = raw_lyric[start:end].decode('utf8')

        return result

    def send_request(self, url, data=None, headers=None):
        obj = common.URL(url, data, headers)
        return obj

def get_lyric(url):
    js = Joysound()

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

#     print(repr(result))
