# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from kashisearch import KashiSearch as Lyric

class LyricTest(unittest.TestCase):
    def test_url_01(self):
        url = 'http://kashisearch.jp/lyrics/188242'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'二人の見る世界')
        self.assertEqual(obj.artist, u'茶太')
        self.assertEqual(obj.lyricist, u'寺山 修司')
        self.assertEqual(obj.composer, u'中田 喜直')
        self.assertEqual(len(obj.lyric), 390)

    def test_url_02(self):
        url = 'http://kashisearch.jp/lyrics/85683'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'マジックナンバー')
        self.assertEqual(obj.artist, u'坂本 真綾')
        self.assertEqual(obj.lyricist, u'坂本真綾')
        self.assertEqual(obj.composer, u'北川勝利')
        self.assertEqual(len(obj.lyric), 526)

if __name__ == '__main__':
    unittest.main()
