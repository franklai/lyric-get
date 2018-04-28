import unittest
from lyric_engine.modules.kget import KGet as Lyric

class KGetTest(unittest.TestCase):
    def test_url_zutto(self):
        url = 'http://www.kget.jp/lyric/188989/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'ずっと feat.HAN-KUN & TEE')
        self.assertEqual(obj.artist, 'SPICY CHOCOLATE, HAN-KUN, TEE')
        self.assertEqual(obj.lyricist, 'HAN-KUN, TEE')
        self.assertEqual(obj.composer, 'DJ CONTROLER, U.M.E.D.Y., WolfJunk')
        self.assertEqual(len(obj.lyric), 769)

    def test_url_kanjani8(self):
        url = 'http://www.kget.jp/lyric/185146/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'ビースト!!')
        self.assertEqual(obj.artist, '関ジャニ∞')
        self.assertEqual(obj.lyricist, '錦戸亮')
        self.assertEqual(obj.composer, '朱鷺羽ソウ')
        self.assertEqual(len(obj.lyric), 924)

    def test_url_maaya(self):
        url = 'http://www.kget.jp/lyric/11066/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'tune the rainbow')
        self.assertEqual(obj.artist, '坂本真綾')
        self.assertEqual(obj.lyricist, '岩里祐穂')
        self.assertEqual(obj.composer, '菅野よう子')
        self.assertEqual(len(obj.lyric), 520)

if __name__ == '__main__':
    unittest.main()
