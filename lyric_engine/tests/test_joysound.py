import unittest
from lyric_engine.modules.joysound import JoySound as Lyric

class LyricTest(unittest.TestCase):
    def test_url_saved(self):
        url = 'https://www.joysound.com/web/search/song/402005'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'SAVED.')
        self.assertEqual(obj.artist, '坂本真綾')
        self.assertEqual(obj.lyricist, '鈴木祥子')
        self.assertEqual(obj.composer, '鈴木祥子')
        self.assertEqual(len(obj.lyric), 397)

    def test_url_id(self):
        url = 'https://www.joysound.com/web/search/song/96127'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'I.D.')
        self.assertEqual(obj.artist, '坂本真綾')
        self.assertEqual(obj.lyricist, '坂本真綾')
        self.assertEqual(obj.composer, '菅野よう子')
        self.assertEqual(len(obj.lyric), 394)

if __name__ == '__main__':
    unittest.main()
