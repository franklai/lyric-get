# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from utaten import UtaTen as Lyric

class UtaTenTest(unittest.TestCase):
    def test_url_guren(self):
        url = 'http://utaten.jp/lyric/BUMP+OF+CHICKEN/beautiful+glider/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'beautiful glider')
        self.assertEqual(obj.artist, u'BUMP OF CHICKEN')
        self.assertEqual(obj.lyricist, u'藤原基央')
        self.assertEqual(obj.composer, u'藤原基央')
        self.assertEqual(len(obj.lyric), 959)

    def test_url_shiranai(self):
        url = 'http://utaten.jp/lyric/AAA/Charge+%26++Go%21/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'Charge &  Go!')
        self.assertEqual(obj.artist, u'AAA')
        self.assertEqual(obj.lyricist, u'Kenn Kato')
        self.assertEqual(obj.composer, u'TETSUYA KOMURO')
        self.assertEqual(len(obj.lyric), 1256)

if __name__ == '__main__':
    unittest.main()
