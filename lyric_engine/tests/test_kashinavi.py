import unittest
from lyric_engine.modules.kashinavi import KashiNavi as Lyric

class KashiNaviTest(unittest.TestCase):
    def test_url_guren(self):
        url = 'http://kashinavi.com/song_view.html?65545'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, '猫背')
        self.assertEqual(obj.artist, '坂本真綾')
        self.assertEqual(obj.lyricist, '岩里祐穂')
        self.assertEqual(obj.composer, '菅野よう子')
        self.assertEqual(len(obj.lyric), 358)

    def test_url_shiranai(self):
        url = 'http://kashinavi.com/song_view.html?77597'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, "We Don't Stop")
        self.assertEqual(obj.artist, '西野カナ')
        self.assertEqual(obj.lyricist, 'Kana Nishino・GIORGIO 13')
        self.assertEqual(obj.composer, 'Giorgio Cancemi')
        self.assertEqual(len(obj.lyric), 1247)

if __name__ == '__main__':
    unittest.main()
