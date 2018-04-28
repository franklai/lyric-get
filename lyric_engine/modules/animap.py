import logging
from utils import common
from utils.lyric_base import LyricBase

site_class = "AniMap"
site_index = "animap"
site_keyword = "animap"
site_url = "http://www.animap.jp/"
test_url = "http://www.animap.jp/kasi/showkasi.php?surl=dk101202_50"


class AniMap(LyricBase):
    def parse_page(self):
        url = self.url

        if not self.find_lyric(url):
            logging.info("Failed to get lyric of url [%s]", url)
            return False

        if not self.find_song_info(url):
            logging.info("Failed to get song info of url [%s]", url)

        return True

    def find_lyric(self, url):
        pattern = "surl=([^&=]+)"

        song_id = common.get_first_group_by_pattern(url, pattern)

        if not song_id:
            logging.error("Failed to get id of url [%s]", url)
            return False

        song_url = "http://www.animap.jp/kasi/phpflash/flashphp.php?unum=" + song_id
        data = common.get_url_content(song_url, encoding="shift_jis")
        if not data:
            logging.error("Failed to get content of url [%s]", song_url)
            return False

        prefix = "test2="
        pos = data.find(prefix)
        if pos == -1:
            logging.error("Failed to find lyric position of url [%s]", url)
            return False

        lyric = data[pos + len(prefix):]

        # test for half to full
        lyric = common.half2full(lyric)

        self.lyric = lyric

        return True

    def find_song_info(self, url):
        ret = True
        html = common.get_url_content(url, encoding="euc_jp")

        prefix = '<TABLE cellspacing="1"'
        suffix = "</TABLE>"
        info_table = common.find_string_by_prefix_suffix(html, prefix, suffix)
        info_table = info_table.replace(r"\n", "")

        print(info_table)

        patterns = {
            "title": r"曲名</TD>\s*<TD .+?>&nbsp;(.+?)</TD>",
            "artist": r"歌手</TD>\s*<TD .+?>&nbsp;(.+?)</TD>",
            "lyricist": r"作詞</TD>\s*<TD .+?>&nbsp;(.+?)</TD>",
            "composer": r"作曲</TD>\s*<TD .+?>&nbsp;(.+?)</TD>",
        }

        self.set_attr(patterns, info_table)

        return ret


def get_lyric(url):
    obj = AniMap(url)

    return obj.get()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    url = "http://www.animap.jp/kasi/showkasi.php?surl=k-160525-032"

    full = get_lyric(url)
    if not full:
        print("Failed to get lyric")
        exit()
    print(full)
