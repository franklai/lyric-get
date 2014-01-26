# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from animap import AniMap as Lyric

class AniMapTest(unittest.TestCase):
    def test_url_01(self):
        url = 'http://www.animap.jp/kasi/showkasi.php?surl=B38260'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u"Don't be long")
        self.assertEqual(obj.artist, u'水樹奈々')
        self.assertEqual(obj.lyricist, u'矢吹俊郎')
        self.assertEqual(obj.composer, u'矢吹俊郎')
        self.assertEqual(len(obj.lyric), 541)

    def test_url_02(self):
        url = 'http://www.animap.jp/kasi/showkasi.php?surl=dk130730_30'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'ViViD')
        self.assertEqual(obj.artist, u"May'n")
        self.assertEqual(obj.lyricist, u'藤林聖子')
        self.assertEqual(obj.composer, u'秋田博之')
        self.assertEqual(len(obj.lyric), 788)

if __name__ == '__main__':
    unittest.main()
