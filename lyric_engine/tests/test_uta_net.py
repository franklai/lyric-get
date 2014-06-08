# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from uta_net import UtaNet as Lyric

class UtaNetTest(unittest.TestCase):
    def test_url_nekose(self):
        url = 'http://www.uta-net.com/song/138139/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'猫背')
        self.assertEqual(obj.artist, u'坂本真綾')
        self.assertEqual(obj.lyricist, u'岩里祐穂')
        self.assertEqual(obj.composer, u'菅野よう子')
        self.assertEqual(len(obj.lyric), 366)

    def test_url_rpg(self):
        url = 'http://www.uta-net.com/song/145480/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'RPG')
        self.assertEqual(obj.artist, u'SEKAI NO OWARI')
        self.assertEqual(obj.lyricist, u'Saori・Fukase')
        self.assertEqual(obj.composer, u'Fukase')
        self.assertEqual(len(obj.lyric), 574)

    def test_url_movie_format(self):
        url = 'http://www.uta-net.com/movie/162972/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'望郷エトランゼ')
        self.assertEqual(obj.artist, u'冠二郎')
        self.assertEqual(obj.lyricist, u'三浦康照')
        self.assertEqual(obj.composer, u'岡千秋')
        self.assertEqual(len(obj.lyric), 216)

if __name__ == '__main__':
    unittest.main()
