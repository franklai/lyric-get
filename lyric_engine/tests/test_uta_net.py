import unittest
from lyric_engine.modules.uta_net import UtaNet as Lyric

class UtaNetTest(unittest.TestCase):
    def test_url_nekose(self):
        url = 'http://www.uta-net.com/song/138139/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, '猫背')
        self.assertEqual(obj.artist, '坂本真綾')
        self.assertEqual(obj.lyricist, '岩里祐穂')
        self.assertEqual(obj.composer, '菅野よう子')
        self.assertEqual(len(obj.lyric), 366)

    def test_url_rpg(self):
        url = 'http://www.uta-net.com/song/145480/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'RPG')
        self.assertEqual(obj.artist, 'SEKAI NO OWARI')
        self.assertEqual(obj.lyricist, 'Saori・Fukase')
        self.assertEqual(obj.composer, 'Fukase')
        self.assertEqual(len(obj.lyric), 574)

    def test_url_movie_format(self):
        url = 'http://www.uta-net.com/movie/162972/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, '望郷エトランゼ')
        self.assertEqual(obj.artist, '冠二郎')
        self.assertEqual(obj.lyricist, '三浦康照')
        self.assertEqual(obj.composer, '岡千秋')
        self.assertEqual(len(obj.lyric), 216)

    def test_url_bz_single_quote(self):
        url = 'http://www.uta-net.com/song/181206/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'Las Vegas')
        self.assertEqual(obj.artist, "B'z")
        self.assertEqual(obj.lyricist, '稲葉浩志')
        self.assertEqual(obj.composer, '松本孝弘')
        self.assertEqual(len(obj.lyric), 426)

if __name__ == '__main__':
    unittest.main()
