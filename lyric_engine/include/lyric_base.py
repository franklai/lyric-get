# coding: utf-8

class LyricBase:
    def __init__(self, url):
        self.url = url
        self.title = None
        self.artist = None
        self.lyricist = None
        self.composer = None
        self.arranger = None
        self.lyric = None

    def get(self, url=None):
        if url:
            self.url = url

        if not self.parse_page():
            return None

        return self.get_full()

    def get_full(self):
        # template of full information
        template = []

        if self.title:
            template.append(self.title)
            template.append('')

        if self.artist:
            template.append(u'歌手：%s' % (self.artist))
        if self.lyricist:
            template.append(u'作詞：%s' % (self.lyricist))
        if self.composer:
            template.append(u'作曲：%s' % (self.composer))
        if self.arranger:
            template.append(u'編曲：%s' % (self.arranger))

        if len(template) > 0:
            template.append('')
            template.append('')
        template.append(self.lyric)

        return '\n'.join(template)

    def parse(self, url=None):
        # fetch self.url, and parse
        if url:
            self.url = url

        return self.parse_page()

    def parse_page(self):
        return True
