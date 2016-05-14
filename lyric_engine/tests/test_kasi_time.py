# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from kasi_time import KasiTime as Lyric

class KasiTimeTest(unittest.TestCase):
    def test_url_guren(self):
        url = 'http://www.kasi-time.com/item-67546.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'紅蓮の弓矢')
        self.assertEqual(obj.artist, u'Linked Horizon')
        self.assertEqual(obj.lyricist, u'Revo')
        self.assertEqual(obj.composer, u'Revo')
        self.assertEqual(obj.arranger, u'Revo')
        self.assertEqual(len(obj.lyric), 778)

    def test_url_shiranai(self):
        url = 'http://www.kasi-time.com/item-43855.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'君の知らない物語')
        self.assertEqual(obj.artist, u'supercell')
        self.assertEqual(obj.lyricist, u'ryo(supercell)')
        self.assertEqual(obj.composer, u'ryo(supercell)')
        self.assertEqual(obj.arranger, u'ryo(supercell)')
        self.assertEqual(len(obj.lyric), 565)

if __name__ == '__main__':
    unittest.main()
