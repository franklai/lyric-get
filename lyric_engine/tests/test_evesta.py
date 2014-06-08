# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from evesta import Evesta as Lyric

class EvestaTest(unittest.TestCase):
    def test_url_01(self):
        url = 'http://www.evesta.jp/lyric/artists/a10019/lyrics/l65161.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'Gift')
        self.assertEqual(obj.artist, u'坂本真綾')
        self.assertEqual(obj.lyricist, u'岩里 祐穂')
        self.assertEqual(obj.composer, u'菅野よう子')
        self.assertEqual(len(obj.lyric), 454)

    def test_url_02(self):
        url = 'http://www.evesta.jp/lyric/artists/a10019/lyrics/l65156.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'紅茶')
        self.assertEqual(obj.artist, u'坂本真綾')
        self.assertEqual(obj.lyricist, u'坂本真綾')
        self.assertEqual(obj.composer, u'菅野よう子')
        self.assertEqual(len(obj.lyric), 383)

if __name__ == '__main__':
    unittest.main()
