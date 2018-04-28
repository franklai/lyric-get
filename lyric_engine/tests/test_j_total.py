import unittest
from lyric_engine.modules.j_total import JTotal as Lyric

class JTotalTest(unittest.TestCase):
    def test_url_01(self):
        url = 'http://music.j-total.net/data/013su/029_sukima_switch/004.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, '奏（かなで）')
        self.assertEqual(obj.artist, 'スキマスイッチ')
        self.assertEqual(obj.lyricist, '常田真太郎・大橋卓弥')
        self.assertEqual(obj.composer, '常田真太郎・大橋卓弥')
        self.assertEqual(len(obj.lyric), 1327)

    def test_url_02(self):
        url = 'http://music.j-total.net/data/026ha/048_hata_motohiro/010.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, '鱗(うろこ)')
        self.assertEqual(obj.artist, '秦基博')
        self.assertEqual(obj.lyricist, '秦基博')
        self.assertEqual(obj.composer, '秦基博')
        self.assertEqual(len(obj.lyric), 1267)

if __name__ == '__main__':
    unittest.main()
