# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import common
from lyric_base import LyricBase

site_class = 'AnimationSong'
site_index = 'animationsong'
site_keyword = 'animationsong'
site_url = 'http://animationsong.com/'
test_url = 'http://animationsong.com/archives/1800903.html'


class AnimationSong(LyricBase):
    def parse_page(self):
        url = self.url

        html = common.get_url_content(url)

        if not html:
            logging.info('Failed to get html of url [%s]', url)
            return False

        html = html.decode('utf-8')

        if not self.find_lyric(html):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(html):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def find_lyric(self, html):
        prefix = u'<h2>歌詞</h2>'
        suffix = '</div>'

        lyric = common.find_string_by_prefix_suffix(
            html, prefix, suffix, False)

        if not lyric:
            logging.info('Failed to get lyric div of url [%s]', url)
            return False

        lyric = lyric.replace('<br />', '')
        lyric = lyric.replace('<p>', '')
        lyric = lyric.replace('</p>', '\n')
        lyric = common.unicode2string(lyric)
        lyric = lyric.strip()

        # due to sakushi, sakkyoku are not list separately, so merge these information in lyric
        staff = self.find_staff(html)
        if staff:
            lyric = '%s\n\n\n%s' % (staff, lyric)

        self.lyric = lyric

        return True

    def find_staff(self, html):
        result = []
        prefix = '<div class="kashidescription">'
        suffix = '</div>'

        info = common.find_string_by_prefix_suffix(html, prefix, suffix, False)
        if not info:
            logging.info('Failed to get info html piece')
            return None

        info = common.to_one_line(info)

        pattern = u'<th>歌手</th><td>(.*?)</td>'
        value = common.get_first_group_by_pattern(info, pattern)
        if value:
            result.append(u'歌手：%s' %
                          (common.unicode2string(common.strip_tags(value))))

        pattern = u'<th>制作者</th><td>(.*?)</td>'
        value = common.get_first_group_by_pattern(info, pattern)
        if value:
            result.append(u'%s' %
                          (common.unicode2string(common.strip_tags(value))))

        if len(result) > 0:
            return '\n'.join(result)

        return None

    def find_song_info(self, html):
        ret = True
        prefix = '<div class="kashidescription">'
        suffix = '</div>'

        info = common.find_string_by_prefix_suffix(html, prefix, suffix, False)
        if not info:
            logging.info('Failed to get info html piece')

        info = common.to_one_line(info)

        patterns = {
            'title': u'<h1>([^<]+)</h1>',
            #             'artist': u'<th>歌手</th><td>(.*?)</td>',
            #             'lyricist': u'作詞：(.*?)　',
            #             'composer': u'作曲：(.*?)</td>'
        }

        for key in patterns:
            pattern = patterns[key]

            value = common.get_first_group_by_pattern(info, pattern)

            if not value:
                logging.info('Failed to get %s', key)
                ret = False
            else:
                value = common.unicode2string(common.strip_tags(value))
                setattr(self, key, value)

        return ret


def get_lyric(url):
    obj = AnimationSong(url)

    return obj.get()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('failed to get full lyric!')
        exit()
    print(full.encode('utf-8', 'ignore'))
