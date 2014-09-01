# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from music_jp import MusicJp as Lyric

class MusicJpTest(unittest.TestCase):
    def test_url_01(self):
        url = 'http://music-book.jp/music/Kashi/aaa1fw1p?artistname=miwa&title=%25e3%2583%2592%25e3%2582%25ab%25e3%2583%25aa%25e3%2583%2598&packageName=%25e3%2583%2592%25e3%2582%25ab%25e3%2583%25aa%25e3%2583%2598'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'ヒカリヘ')
        self.assertEqual(obj.artist, u'miwa')
        self.assertEqual(obj.lyricist, u'miwa')
        self.assertEqual(obj.composer, u'miwa')
        self.assertEqual(len(obj.lyric), 636)

    def test_url_02(self):
        url = 'http://music-book.jp/music/Kashi/aaa1pa8u?artistname=%25e8%2597%258d%25e4%25ba%2595%25e3%2582%25a8%25e3%2582%25a4%25e3%2583%25ab&title=INNOCENCE&packageName=INNOCENCE'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'INNOCENCE')
        self.assertEqual(obj.artist, u'藍井エイル')
        self.assertEqual(obj.lyricist, u'Eir/Ryosuke Shigenaga')
        self.assertEqual(obj.composer, u'Ryosuke Shigenaga')
        self.assertEqual(len(obj.lyric), 470)

if __name__ == '__main__':
    unittest.main()
