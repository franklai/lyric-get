import unittest
from lyric_engine.modules.lyricwiki import LyricWiki as Lyric

class LyricWikiTest(unittest.TestCase):
    def test_url_01(self):
        url = 'http://lyrics.wikia.com/%E5%9D%82%E6%9C%AC%E7%9C%9F%E7%B6%BE_(Maaya_Sakamoto):%E5%83%95%E3%81%9F%E3%81%A1%E3%81%8C%E6%81%8B%E3%82%92%E3%81%99%E3%82%8B%E7%90%86%E7%94%B1'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, '僕たちが恋をする理由')
        self.assertEqual(obj.artist, 'Maaya Sakamoto')
        self.assertEqual(len(obj.lyric), 410)

    def test_url_02(self):
        url = 'http://lyrics.wikia.com/Zard:%E9%81%8B%E5%91%BD%E3%81%AE%E3%83%AB%E3%83%BC%E3%83%AC%E3%83%83%E3%83%88%E5%BB%BB%E3%81%97%E3%81%A6'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, '運命のルーレット廻して')
        self.assertEqual(obj.artist, 'Zard')
        self.assertEqual(len(obj.lyric), 319)

if __name__ == '__main__':
    unittest.main()
