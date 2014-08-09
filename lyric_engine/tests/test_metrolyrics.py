# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from metrolyrics import MetroLyrics as Lyric

class MetroLyricsTest(unittest.TestCase):
    def test_url_01(self):
        url = 'http://www.metrolyrics.com/red-lyrics-taylor-swift.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'Red')
        self.assertEqual(obj.artist, u'Taylor Swift')
        self.assertEqual(len(obj.lyric), 1541)

    def test_url_02(self):
        url = 'http://www.metrolyrics.com/my-awake-lyrics-late-night-alumni.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'My Awake')
        self.assertEqual(obj.artist, u'Late Night Alumni')
        self.assertEqual(len(obj.lyric), 1523)

if __name__ == '__main__':
    unittest.main()
