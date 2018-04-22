# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from j_total import JTotal as Lyric

class JTotalTest(unittest.TestCase):
    def test_url_01(self):
        url = 'http://music.j-total.net/data/013su/029_sukima_switch/004.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'奏（かなで）')
        self.assertEqual(obj.artist, u'スキマスイッチ')
        self.assertEqual(obj.lyricist, u'常田真太郎・大橋卓弥')
        self.assertEqual(obj.composer, u'常田真太郎・大橋卓弥')
        self.assertEqual(len(obj.lyric), 1327)

    def test_url_02(self):
        url = 'http://music.j-total.net/data/026ha/048_hata_motohiro/010.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'鱗(うろこ)')
        self.assertEqual(obj.artist, u'秦基博')
        self.assertEqual(obj.lyricist, u'秦基博')
        self.assertEqual(obj.composer, u'秦基博')
        self.assertEqual(len(obj.lyric), 1267)

if __name__ == '__main__':
    unittest.main()
