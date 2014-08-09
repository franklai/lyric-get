# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from utaten import UtaTen as Lyric

class UtaTenTest(unittest.TestCase):
    def test_url_guren(self):
        url = 'http://utaten.com/lyric/jb71208131'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(len(obj.lyric), 1783)

    def test_url_shiranai(self):
        url = 'http://utaten.com/lyric/jb71404001'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(len(obj.lyric), 760)

if __name__ == '__main__':
    unittest.main()
