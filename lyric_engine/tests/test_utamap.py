# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from utamap import UtaMap as Lyric

class UtaMapTest(unittest.TestCase):
    def test_url_one_more(self):
        url = 'http://www.utamap.com/showkasi.php?surl=59709'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'One more time,One more chance')
        self.assertEqual(obj.artist, u'山崎まさよし')
        self.assertEqual(obj.lyricist, u'山崎将義')
        self.assertEqual(obj.composer, u'山崎将義')
        self.assertEqual(len(obj.lyric), 794)

    def test_url_02(self):
        url = 'http://www.utamap.com/showkasi.php?surl=k-131226-001'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'ちっぽけな愛のうた')
        self.assertEqual(obj.artist, u'小枝理子&小笠原秋')
        self.assertEqual(obj.lyricist, u'亀田誠治')
        self.assertEqual(obj.composer, u'亀田誠治')
        self.assertEqual(len(obj.lyric), 572)

if __name__ == '__main__':
    unittest.main()
