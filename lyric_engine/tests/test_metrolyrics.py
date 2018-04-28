import unittest
from metrolyrics import MetroLyrics as Lyric

class MetroLyricsTest(unittest.TestCase):
    def test_url_01(self):
        url = 'http://www.metrolyrics.com/red-lyrics-taylor-swift.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'Red')
        self.assertEqual(obj.artist, 'Taylor Swift')
        self.assertEqual(len(obj.lyric), 1540)

    def test_url_02(self):
        url = 'http://www.metrolyrics.com/my-awake-lyrics-late-night-alumni.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'My Awake')
        self.assertEqual(obj.artist, 'Late Night Alumni')
        self.assertEqual(len(obj.lyric), 1523)

if __name__ == '__main__':
    unittest.main()
