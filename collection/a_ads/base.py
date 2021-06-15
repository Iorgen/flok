import threading
import time

from selenium.common.exceptions import NoSuchElementException, WebDriverException
from parser.base import BaseChromeDriverParser
from parser.exceptions import (
    LoadPageException, ResolveCaptchaException, RetrieveInformationFromPageException
)


class BaseAAdsParser(BaseChromeDriverParser):
    _CAPTCHA_RETRIES = 3
    _CAP_MONSTER_SOLVER_SLEEP_TIME = 2
    _ONE_PROXY_LIMIT = 40

    CAPTCHA_ENDPOINT = 'bot.html'
    CAPTCHA_USAGE = 0
    """
        Using chrome based parser this class abstract retrieving information from
        collection of given pages.
        - for given pages load on every url using generator function
        """

    @classmethod
    def captcha_capacity(cls):
        print(cls.CAPTCHA_USAGE)
