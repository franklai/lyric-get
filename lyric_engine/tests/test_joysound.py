# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from joysound import JoySound as Lyric

class LyricTest(unittest.TestCase):
    def test_url_saved(self):
        url = 'https://www.joysound.com/web/search/song/402005'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'SAVED.')
        self.assertEqual(obj.artist, u'坂本真綾')
        self.assertEqual(obj.lyricist, u'鈴木祥子')
        self.assertEqual(obj.composer, u'鈴木祥子')
        self.assertEqual(len(obj.lyric), 397)

    def test_url_id(self):
        url = 'https://www.joysound.com/web/search/song/96127'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'I.D.')
        self.assertEqual(obj.artist, u'坂本真綾')
        self.assertEqual(obj.lyricist, u'坂本真綾')
        self.assertEqual(obj.composer, u'菅野よう子')
        self.assertEqual(len(obj.lyric), 394)

if __name__ == '__main__':
    unittest.main()
