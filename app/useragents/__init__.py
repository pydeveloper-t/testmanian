from config import logger
from random import randint


class UA:
    DEFAULT_UA = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) ' \
                 'Version/5.0.4 Safari/533.20.27'

    def __init__(self, ua_file):
        self.useragents = [UA.DEFAULT_UA]
        try:
            with open(ua_file, 'r') as f_ua:
                self.useragents.extend([ua.strip() for ua in f_ua.readlines()])
        except Exception as exc:
            logger.error(f'[USER AGENTS] Exception: {exc}')

    def get_random_useragent(self):
        bound_b = len(self.useragents) - 1
        index = randint(0, bound_b)
        return self.useragents[index]

