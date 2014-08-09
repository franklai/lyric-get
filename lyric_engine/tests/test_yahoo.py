# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from yahoo import Yahoo as Lyric

class UtaMapTest(unittest.TestCase):
    def test_url_one_more(self):
        url = 'http://lyrics.gyao.yahoo.co.jp/ly/Y004402/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'帰って来たヨッパライ')
        self.assertEqual(obj.artist, u'ザ・フォーク・クルセダーズ')
        self.assertEqual(obj.lyricist, u'ザ･フォーク･パロディ･ギャング')
        self.assertEqual(obj.composer, u'加藤和彦')
        self.assertEqual(len(obj.lyric), 536)

    def test_url_02(self):
        url = 'http://lyrics.gyao.yahoo.co.jp/ly/Y160641/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'home')
        self.assertEqual(obj.artist, u'クリス・ハート')
        self.assertEqual(obj.lyricist, u'多胡邦夫')
        self.assertEqual(obj.composer, u'多胡邦夫')
        self.assertEqual(len(obj.lyric), 376)

if __name__ == '__main__':
    unittest.main()
