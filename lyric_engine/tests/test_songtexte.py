import unittest
from lyric_engine.modules.songtexte import SongTexte as Lyric

class SongTexteTest(unittest.TestCase):
    def test_url_01(self):
        url = 'http://www.songtexte.com/songtext/taylor-swift/begin-again-63a6de47.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, 'Begin Again')
        self.assertEqual(obj.artist, 'Taylor Swift')
        self.assertEqual(len(obj.lyric), 1608)

    def test_url_03(self):
        url = 'http://www.songtexte.com/songtext/bone-thugs-n-harmony-feat-mariah-carey-and-bow-wow/c-town-6ba75a7e.html'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, "C-Town")
        self.assertEqual(obj.artist, 'Bone Thugs-n-Harmony feat. Mariah Carey & Bow Wow')
        self.assertEqual(len(obj.lyric), 2976)

if __name__ == '__main__':
    unittest.main()
