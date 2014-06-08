# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from animesong import AnimeSong as Lyric

class AnimeSongTest(unittest.TestCase):
    def test_url_01(self):
        url = 'http://www.jtw.zaq.ne.jp/animesong/ki/zenki/aoi.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'青い輝き・転生降臨')
        self.assertEqual(obj.artist, u'緒方恵美')
        self.assertEqual(obj.lyricist, u'黒岩よしひろ')
        self.assertEqual(obj.composer, u'小川幸夫')
        self.assertEqual(obj.arranger, u'小川幸夫')
        self.assertEqual(len(obj.lyric), 205)

    def test_url_02(self):
        url = 'http://www.jtw.zaq.ne.jp/animesong/ho/hozuki/jigoku.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'地獄の沙汰も君次第')
        self.assertEqual(obj.artist, u'地獄の沙汰オールスターズ')
        self.assertEqual(obj.lyricist, u'サイトウ"JxJx"ジュン、獄卒音楽連盟')
        self.assertEqual(obj.composer, u'サイトウ"JxJx"ジュン')
        self.assertEqual(obj.arranger, u'サイトウ"JxJx"ジュン')
        self.assertEqual(len(obj.lyric), 1828)

if __name__ == '__main__':
    unittest.main()
