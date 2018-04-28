import unittest
from lyric_engine.modules.kasi_time import KasiTime as Lyric

class KasiTimeTest(unittest.TestCase):
    def test_url_guren(self):
        url = 'http://www.kasi-time.com/item-67546.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, '紅蓮の弓矢')
        self.assertEqual(obj.artist, 'Linked Horizon')
        self.assertEqual(obj.lyricist, 'Revo')
        self.assertEqual(obj.composer, 'Revo')
        self.assertEqual(obj.arranger, 'Revo')
        self.assertEqual(len(obj.lyric), 783)

    def test_url_shiranai(self):
        url = 'http://www.kasi-time.com/item-43855.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, '君の知らない物語')
        self.assertEqual(obj.artist, 'supercell')
        self.assertEqual(obj.lyricist, 'ryo(supercell)')
        self.assertEqual(obj.composer, 'ryo(supercell)')
        self.assertEqual(obj.arranger, 'ryo(supercell)')
        self.assertEqual(len(obj.lyric), 565)

    def test_complex_artist(self):
        url = 'http://www.kasi-time.com/item-73971.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'Animetic Love Letter')
        self.assertEqual(obj.artist, '宮森あおい&安原絵麻&坂木しずか(cv.木村珠莉&佳村はるか&千菅春香)')
        self.assertEqual(obj.lyricist, '桃井はるこ')
        self.assertEqual(obj.composer, '桃井はるこ')
        self.assertEqual(obj.arranger, '渡辺剛')
        self.assertEqual(len(obj.lyric), 773)

if __name__ == '__main__':
    unittest.main()
