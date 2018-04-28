import unittest
from lyric_engine.modules.petitlyrics import PetitLyrics as Lyric

class PetitLyricsTest(unittest.TestCase):
    def test_url_01(self):
        url = 'https://petitlyrics.com/lyrics/914421'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, '猫背')
        self.assertEqual(obj.artist, '坂本 真綾')
        self.assertEqual(obj.lyricist, '岩里祐穂')
        self.assertEqual(obj.composer, '菅野よう子')
        self.assertEqual(len(obj.lyric), 410)
        self.assertEqual(obj.lyric[:6], '背の高い君は')

    def test_url_02(self):
        url = 'http://petitlyrics.com/lyrics/936622'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'RPG')
        self.assertEqual(obj.artist, 'SEKAI NO OWARI')
        self.assertEqual(obj.lyricist, 'Saori/Fukase')
        self.assertEqual(obj.composer, 'Fukase')
        self.assertEqual(len(obj.lyric), 612)
        self.assertEqual(obj.lyric[:17], '空は青く澄み渡り 海を目指して歩く')

if __name__ == '__main__':
    unittest.main()
