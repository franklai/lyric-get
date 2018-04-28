#/usr/bin/env python3
import os
import sys

import unittest
from lyric_engine.modules.animap import AniMap as Lyric

class AniMapTest(unittest.TestCase):
    def test_url_01(self):
        url = 'http://www.animap.jp/kasi/showkasi.php?surl=B38260'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, "Don't be long")
        self.assertEqual(obj.artist, '水樹奈々')
        self.assertEqual(obj.lyricist, '矢吹俊郎')
        self.assertEqual(obj.composer, '矢吹俊郎')
        self.assertEqual(len(obj.lyric), 541)

    def test_url_02(self):
        url = 'http://www.animap.jp/kasi/showkasi.php?surl=dk130730_30'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'ViViD')
        self.assertEqual(obj.artist, "May'n")
        self.assertEqual(obj.lyricist, '藤林聖子')
        self.assertEqual(obj.composer, '秋田博之')
        self.assertEqual(len(obj.lyric), 788)

if __name__ == '__main__':
    unittest.main()
