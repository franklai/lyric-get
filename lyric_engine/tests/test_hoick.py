import unittest
from lyric_engine.modules.hoick import Hoick as Lyric

class LyricTest(unittest.TestCase):
    def test_url_saved(self):
        url = 'http://hoick.jp/mdb/detail/9920/%E3%81%AB%E3%81%98'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'にじ')

        self.assertEqual(obj.lyricist, '新沢としひこ')
        self.assertEqual(obj.composer, '中川ひろたか')
        self.assertEqual(len(obj.lyric), 509)

    def test_url_id(self):
        url = 'http://hoick.jp/mdb/detail/19471/%E3%83%93%E3%83%BC%E3%81%A0%E3%81%BE%E3%83%93%E3%83%BC%E3%81%99%E3%81%91%E3%81%AE%E5%A4%A7%E5%86%92%E9%99%BA'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'ビーだまビーすけの大冒険')

        self.assertEqual(obj.lyricist, '佐藤雅彦,内野真澄')
        self.assertEqual(obj.composer, '栗原正己')
        self.assertEqual(len(obj.lyric), 275)

if __name__ == '__main__':
    unittest.main()
