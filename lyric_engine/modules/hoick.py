import logging

from utils.lyric_base import LyricBase

site_class = 'Hoick'
site_index = 'hoick'
site_keyword = 'hoick'
site_url = 'https://hoick.jp/'
test_url = 'http://hoick.jp/mdb/detail/9920/%E3%81%AB%E3%81%98'


class Hoick(LyricBase):
    def parse_page(self):
        url = self.url

        if not self.get_from_azure(url):
            logging.info('Failed to get from azure, url [%s]', url)
            return False

        return True


def get_lyric(url):
    obj = Hoick(url)

    return obj.get()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Cannot get lyric')
        exit()
    print(full)
