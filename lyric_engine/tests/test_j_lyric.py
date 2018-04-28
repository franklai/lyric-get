import unittest
from lyric_engine.modules.j_lyric import JLyric as Lyric

class JLyricTest(unittest.TestCase):
    def test_url_01(self):
        url = 'http://j-lyric.net/artist/a002723/l001e83.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'tune the rainbow')
        self.assertEqual(obj.artist, '坂本真綾')
        self.assertEqual(obj.lyricist, '岩里祐穂')
        self.assertEqual(obj.composer, '菅野よう子')
        self.assertEqual(len(obj.lyric), 447)

    def test_url_02(self):
        url = 'http://j-lyric.net/artist/a000673/l000bea.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, '天体観測')
        self.assertEqual(obj.artist, 'BUMP OF CHICKEN')
        self.assertEqual(obj.lyricist, '藤原基央')
        self.assertEqual(obj.composer, '藤原基央')
        self.assertEqual(len(obj.lyric), 734)

if __name__ == '__main__':
    unittest.main()
