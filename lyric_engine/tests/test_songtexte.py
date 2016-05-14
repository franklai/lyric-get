# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from songtexte import SongTexte as Lyric

class SongTexteTest(unittest.TestCase):
    def test_url_01(self):
        url = 'http://www.songtexte.com/songtext/taylor-swift/begin-again-63a6de47.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'Begin Again')
        self.assertEqual(obj.artist, u'Taylor Swift')
        self.assertEqual(len(obj.lyric), 1618)

    def test_url_02(self):
        url = 'http://www.songtexte.com/songtext/guns-n-roses/sweet-child-o-mine-33d0c849.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u"Sweet Child o' Mine")
        self.assertEqual(obj.artist, u'Guns N’ Roses')
        self.assertEqual(len(obj.lyric), 1066)

    def test_url_03(self):
        url = 'http://www.songtexte.com/songtext/bone-thugs-n-harmony-feat-mariah-carey-and-bow-wow/c-town-6ba75a7e.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u"C-Town")
        self.assertEqual(obj.artist, u'Bone Thugs-n-Harmony feat. Mariah Carey & Bow Wow')
        self.assertEqual(len(obj.lyric), 2977)

if __name__ == '__main__':
    unittest.main()
