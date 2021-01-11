from datetime import datetime, timedelta
from selenium import webdriver
import time
import json
import base64
import pytesseract
import os
import requests
import dateparser
import asyncio
from parser.exceptions import LoadPageException
import logging


class BaseParser:
    """
    Extend validators in base class and implement in child class
    """
    DATE_VALIDATORS = None
    PHONE_VALIDATORS = None
    BASE_URL = None
    LOGGER = None

    def __init__(self, _base_url):
        self.BASE_URL = _base_url
        self.LOGGER = logging.getLogger(__name__)
        # TODO send date and phone validators
        self.DATE_VALIDATORS = None
        self.PHONE_VALIDATORS = None

    def get(self):
        raise NotImplementedError()

    def retrieve_information(self):
        raise NotImplementedError()

    # def imgb64_to_str(self, src):
    #     add = src[11:14]
    #     fh = open("temp." + add, "wb")
    #     fh.write(base64.b64decode(src[22:]))
    #     fh.close()
    #     img = Image.open("temp." + add)
    #     phone = pytesseract.image_to_string(img)
    #     img.close()
    #     phone = phone.replace("\n", '').replace("\t", "").replace(" ", "").replace("-", "")[:11]
    #     os.remove("temp." + add)
    #     return str(phone)

    def date_parser(self, str):
        date = ''
        for validator in self.DATE_VALIDATORS:
            date = validator.parse(str)
            if date == False:
                continue
            else:
                break
        return date

    def now_date(self):
        date_format = '%d.%m.%Y'
        return dateparser.parse('сейчас').strftime(date_format)


class BaseChromeDriverParser(BaseParser):

    """
    TODO
        change parser configurations
        renew proxy web servers

    """
    _DRIVER = None

    def __init__(self, _driver_path, _chrome_options, **kwargs):
        super(BaseParser, self).__init__(**kwargs)
        self._DRIVER = webdriver.Chrome(executable_path=_driver_path, chrome_options=_chrome_options)

    def _load_html_page(self, _page_url):
        try:
            self._DRIVER.get(_page_url)
        except Exception as e:
            self.LOGGER.exception(f'Attempt to load page {_page_url} fails with {e}')
            raise LoadPageException()

    def _change_proxy(self):
        pass

    def preload_page(self, _entrypoint_url_addtition):
        raise NotImplementedError()

    def loop_collection(self):
        raise NotImplementedError()


class BaseChromeCollectionParser(BaseChromeDriverParser):

    def __init__(self, **kwargs):
        super(BaseChromeDriverParser, self).__init__(**kwargs)

    def preload_page(self, _entrypoint_url_addtition):
        entry_point_url = f'{self.BASE_URL}/{_entrypoint_url_addtition}'
        self._load_html_page(entry_point_url)


class BaseChromePageParser(BaseChromeDriverParser):

    def __init__(self, **kwargs):
        super(BaseChromeDriverParser, self).__init__(**kwargs)

    def load_page(self, ):
        raise NotImplementedError()
