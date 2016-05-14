# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from musixmatch import MusixMatch as Lyric

class MusixMatchTest(unittest.TestCase):
    def test_url_01(self):
        url = 'https://www.musixmatch.com/lyrics/LINKIN-PARK/One-Step-Closer'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'One Step Closer')
        self.assertEqual(obj.artist, u'LINKIN PARK')
        self.assertEqual(len(obj.lyric), 1456)
        self.assertEqual(obj.lyric[:26], u'I cannot take this anymore')

    def test_url_02(self):
        url = 'https://www.musixmatch.com/lyrics/坂本真綾/猫背'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'猫背')
        self.assertEqual(obj.artist, u'坂本真綾')
        self.assertEqual(len(obj.lyric), 358)
        self.assertEqual(obj.lyric[:6], u'背の高い君は')

if __name__ == '__main__':
    unittest.main()
