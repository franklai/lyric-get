# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from j_lyric import JLyric as Lyric

class JLyricTest(unittest.TestCase):
    def test_url_01(self):
        url = 'http://j-lyric.net/artist/a002723/l001e83.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'tune the rainbow')
        self.assertEqual(obj.artist, u'坂本真綾')
        self.assertEqual(obj.lyricist, u'岩里祐穂')
        self.assertEqual(obj.composer, u'菅野よう子')
        self.assertEqual(len(obj.lyric), 447)

    def test_url_02(self):
        url = 'http://j-lyric.net/artist/a000673/l000bea.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'天体観測')
        self.assertEqual(obj.artist, u'BUMP OF CHICKEN')
        self.assertEqual(obj.lyricist, u'藤原基央')
        self.assertEqual(obj.composer, u'藤原基央')
        self.assertEqual(len(obj.lyric), 734)

if __name__ == '__main__':
    unittest.main()
