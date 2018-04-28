import unittest
from lyric_engine.modules.utaten import UtaTen as Lyric

class UtaTenTest(unittest.TestCase):
    def test_url_guren(self):
        url = 'http://utaten.com/lyric/BUMP+OF+CHICKEN/beautiful+glider/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'beautiful glider')
        self.assertEqual(obj.artist, 'BUMP OF CHICKEN')
        self.assertEqual(obj.lyricist, '藤原基央')
        self.assertEqual(obj.composer, '藤原基央')
        self.assertEqual(len(obj.lyric), 959)

    def test_url_shiranai(self):
        url = 'http://utaten.com/lyric/AAA/Charge+%26++Go%21/'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'Charge & Go!')
        self.assertEqual(obj.artist, 'AAA')
        self.assertEqual(obj.lyricist, 'Kenn Kato')
        self.assertEqual(obj.composer, 'TETSUYA KOMURO')
        self.assertEqual(len(obj.lyric), 1256)

if __name__ == '__main__':
    unittest.main()
