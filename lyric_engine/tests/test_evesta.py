import unittest
from lyric_engine.modules.evesta import Evesta as Lyric

class EvestaTest(unittest.TestCase):
    def test_url_01(self):
        url = 'http://www.evesta.jp/lyric/artists/a10019/lyrics/l65161.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'Gift')
        self.assertEqual(obj.artist, '坂本真綾')
        self.assertEqual(obj.lyricist, '岩里 祐穂')
        self.assertEqual(obj.composer, '菅野よう子')
        self.assertEqual(len(obj.lyric), 454)

    def test_url_02(self):
        url = 'http://www.evesta.jp/lyric/artists/a10019/lyrics/l65156.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, '紅茶')
        self.assertEqual(obj.artist, '坂本真綾')
        self.assertEqual(obj.lyricist, '坂本真綾')
        self.assertEqual(obj.composer, '菅野よう子')
        self.assertEqual(len(obj.lyric), 383)

if __name__ == '__main__':
    unittest.main()
