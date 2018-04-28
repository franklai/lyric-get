import logging
from utils import common
from utils.lyric_base import LyricBase

site_class = 'PetitLyrics'
site_index = 'petitlyrics'
site_keyword = 'petitlyrics'
site_url = 'https://petitlyrics.com/'
test_url = 'https://petitlyrics.com/lyrics/914675'
test_expect_length = 1275


class PetitLyrics(LyricBase):
    def parse_page(self):
        url = self.url

        if not self.get_from_azure(url):
            logging.info('Failed to get from azure, url [%s]', url)
            return False

        return True

def get_lyric(url):
    obj = PetitLyrics(url)

    return obj.get()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url
    url = 'https://petitlyrics.com/lyrics/1175487'
    url = 'https://petitlyrics.com/lyrics/1015689'
    url = 'https://petitlyrics.com/lyrics/34690'

    full = get_lyric(url)
    if not full:
        print('Cannot get lyric')
        exit()
    print(full)
