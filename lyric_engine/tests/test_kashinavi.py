# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from kashinavi import KashiNavi as Lyric

class KashiNaviTest(unittest.TestCase):
    def test_url_guren(self):
        url = 'http://kashinavi.com/song_view.html?65545'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'猫背')
        self.assertEqual(obj.artist, u'坂本真綾')
        self.assertEqual(obj.lyricist, u'岩里祐穂')
        self.assertEqual(obj.composer, u'菅野よう子')
        self.assertEqual(len(obj.lyric), 374)

    def test_url_shiranai(self):
        url = 'http://kashinavi.com/song_view.html?77597'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u"We Don't Stop")
        self.assertEqual(obj.artist, u'西野カナ')
        self.assertEqual(obj.lyricist, u'Kana Nishino・GIORGIO 13')
        self.assertEqual(obj.composer, u'Giorgio Cancemi')
        self.assertEqual(len(obj.lyric), 1273)

if __name__ == '__main__':
    unittest.main()
