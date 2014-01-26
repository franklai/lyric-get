# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from kget import KGet as Lyric

class KGetTest(unittest.TestCase):
    def test_url_zutto(self):
        url = 'http://www.kget.jp/lyric/188989/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'ずっと feat.HAN-KUN & TEE')
        self.assertEqual(obj.artist, u'SPICY CHOCOLATE, HAN-KUN, TEE')
        self.assertEqual(obj.lyricist, u'HAN-KUN, TEE')
        self.assertEqual(obj.composer, u'DJ CONTROLER, U.M.E.D.Y., WolfJunk')
        self.assertEqual(len(obj.lyric), 769)

    def test_url_kanjani8(self):
        url = 'http://www.kget.jp/lyric/185146/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'ビースト!!')
        self.assertEqual(obj.artist, u'関ジャニ∞')
        self.assertEqual(obj.lyricist, u'錦戸亮')
        self.assertEqual(obj.composer, u'朱鷺羽ソウ')
        self.assertEqual(len(obj.lyric), 924)

if __name__ == '__main__':
    unittest.main()
