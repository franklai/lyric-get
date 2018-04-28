import unittest
from lyric_engine.modules.yahoo import Yahoo as Lyric

class UtaMapTest(unittest.TestCase):
    def test_url_one_more(self):
        url = 'http://lyrics.gyao.yahoo.co.jp/ly/Y004402/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, '帰って来たヨッパライ')
        self.assertEqual(obj.artist, 'ザ・フォーク・クルセダーズ')
        self.assertEqual(obj.lyricist, 'ザ･フォーク･パロディ･ギャング')
        self.assertEqual(obj.composer, '加藤和彦')
        self.assertEqual(len(obj.lyric), 495)

    def test_url_02(self):
        url = 'http://lyrics.gyao.yahoo.co.jp/ly/Y160641/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'home')
        self.assertEqual(obj.artist, 'クリス・ハート')
        self.assertEqual(obj.lyricist, '多胡邦夫')
        self.assertEqual(obj.composer, '多胡邦夫')
        self.assertEqual(len(obj.lyric), 357)

if __name__ == '__main__':
    unittest.main()
