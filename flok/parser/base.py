import logging
import time
import threading
import dateparser
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from flok.parser.exceptions import (
    LoadPageException
)


class BaseParser:
    """
    Extend validators in base class and implement in child class
    Each parser class should deal with his job in his own Thread
    Queue based
    Or direct task based
    Depends on implementation
    """
    DATE_VALIDATORS = None
    PHONE_VALIDATORS = None
    BASE_URL = None
    # TODO Refactor into _MAIN_SOLVER_NAME
    _MAIN_SOLVER_ID = None

    def __init__(self, base_url: str):
        logging.basicConfig(level=logging.INFO, format='%(relativeCreated)6d %(threadName)s %(message)s')
        self.LOGGER = logging.getLogger(__name__)
        # self.LOGGER.info(base_url)
        # self.BASE_URL = kwargs.get('base_url', None)
        self.BASE_URL = base_url
        # TODO custom error
        if not self.BASE_URL:
            raise NotImplementedError()
        # TODO send date and phone validators
        self.DATE_VALIDATORS = None
        self.PHONE_VALIDATORS = None

    def set_main_main_solver_id(self, _main_solver_id: str):
        self._MAIN_SOLVER_ID = _main_solver_id

    def get(self):
        raise NotImplementedError()

    def retrieve_information(self, url):
        raise NotImplementedError()

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
    _CAPTCHA_RETRIES = 3
    _CAP_MONSTER_SOLVER_SLEEP_TIME = 2
    _ONE_PROXY_LIMIT = 40
    _PAGES_LOAD = 0
    CAPTCHA_USAGE = 0
    _USE_PROXY = False

    def __init__(self, driver_path, captcha_key, *args, **kwargs):
        self._driver_path = driver_path
        self._captcha_key = captcha_key
        _chrome_options = self._initialize_driver_options()
        self._initialize_driver(_driver_path=driver_path, _chrome_options=_chrome_options)
        super(BaseChromeDriverParser, self).__init__(*args, **kwargs)
        # Initial proxy setup
        # TODO as POP from list
        # self._change_proxy("5.133.122.207:8085")

    @classmethod
    def increment_loaded_pages(cls):
        cls._PAGES_LOAD += 1

    @classmethod
    def change_proxy_necessary(cls):
        necessary = False
        if cls._PAGES_LOAD >= cls._ONE_PROXY_LIMIT:
            necessary = True
        if cls._CAPTCHA_RETRIES > cls.CAPTCHA_USAGE:
            necessary = True
        return necessary

    class Retry(object):
        """
        A decorator inner class for retry functionality.
        Set the custom retry_count and retry_interval in
        outer class constructor
        """

        def __init__(self):
            pass

        def __call__(self, decor_method):
            def wrapper(self, *args, **kwargs):
                """
                decorator func
                """
                return_values = None
                for count in range(self._retry_count):
                    try:
                        result = decor_method(self, *args, **kwargs)
                        return result

                    except Exception as E:
                        BaseChromeDriverParser.increment_loaded_pages()
                        if BaseChromeDriverParser.change_proxy_necessary() and self._USE_PROXY:
                            # TODO get next proxy IP address
                            # self._change_proxy("5.133.122.207:8085")
                            pass
                        if self._MAIN_SOLVER_ID == threading.currentThread().getName():
                            self._try_resolve_captcha()
                        else:
                            time.sleep(10)
                        self._retrieve_information_exception_handler(exc=E, endpoint=kwargs.get('url', None))
                        BaseChromeDriverParser.retry_check(count, self._retry_count, E)
            return wrapper

        def __set__(self):
            return NotImplementedError("Cannot change value")

    @staticmethod
    def retry_check(name: str, curr_count: int, retry_count: int, err):
        """
        :param name:
        :param curr_count:
        :param retry_count:
        :return:
        """
        # log something {name}
        if curr_count == retry_count - 1:
            raise err()

    @staticmethod
    def _initialize_driver_options():
        # TODO read some papers for selenium optimization
        # prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options = webdriver.ChromeOptions()
        # if not debug:
        #     chrome_options.add_argument("--headless")
        # chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('window-size=1920x1480')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument("--disable-extensions")
        return chrome_options

    def _try_find_element_text_by_xpath(self, x_path: str):
        try:
            return self._DRIVER.find_element_by_xpath(xpath=x_path).text
        except NoSuchElementException as NSEE:
            self.LOGGER.warning(f"element by {x_path} does not exists because {NSEE}")
            return ' '
        except Exception as E:
            self.LOGGER.warning(f"element by {x_path} does not exists because {E}")
            return ' '

    def _cap_monster_base64_image_solver(self, image_base64):
        """
        # TODO get from config
        :param image_base64:
        :return:
        """
        def _cap_monster_task_result(task_id: str):

            response = requests.request(
                method='POST',
                url='https://api.capmonster.cloud/getTaskResult',
                json={
                    "clientKey": self._captcha_key,
                    "taskId": task_id
                },
            ).json()

            error_id = response.get('errorId', None)
            status = response.get('status', None)
            if status is not None and status == 'processing':
                return None

            if status is not None and status == 'ready':
                solution = response.get("solution", None)
                self.LOGGER.info(f'Cap Monster task:{task_id} answer retrieve successfully')
                return solution

        # Get api key from CapMonsterHadnler
        response = requests.request(
            method='POST',
            url='https://api.capmonster.cloud/createTask',
            json={
                "clientKey": self._captcha_key,
                "task":
                    {
                        "type": "ImageToTextTask",
                        "body": image_base64
                    }
            },
        ).json()

        error_id = response.get('errorId', None)
        task_id = response.get('taskId', None)

        if error_id == 0 and task_id is not None:
            self.LOGGER.info(f'Cap Monster task id {task_id} setup successfully, start solving')
            for _retry in range(self._CAPTCHA_RETRIES):
                time.sleep(self._CAP_MONSTER_SOLVER_SLEEP_TIME)
                cap_res = _cap_monster_task_result(task_id=task_id)
                if cap_res is not None:
                    return cap_res['text']
        return 0

    def _initialize_driver(self, _driver_path: str,  _chrome_options:  webdriver.ChromeOptions()):
        self._DRIVER = webdriver.Chrome(executable_path=_driver_path, chrome_options=_chrome_options)

    def _change_proxy(self, _proxy_url: str):
        """
        TODO check how this working
        :param _proxy_url:
        :return:
        """
        #
        _chrome_options = self._initialize_driver_options()
        _chrome_options.add_argument('--proxy-server=%s' % _proxy_url)
        self._initialize_driver(_driver_path=self._driver_path, _chrome_options=_chrome_options)
        self.LOGGER.info(f"PROXY Server changed to {_proxy_url}")

    def _load_html_page(self, _endpoint_url):
        """
        PREDICATE
        Default for loading html page via selenium browser
        :param _endpoint_url:
            template {self.BASE_URL}{_endpoint_url}
            target page for information retrieving
        """
        try:
            self._DRIVER.get(f"{self.BASE_URL}{_endpoint_url}")
        except Exception as E:
            raise LoadPageException()

    @Retry()
    def retrieve_information(self, url):
        """
            :return:
        """
        self._load_html_page(_endpoint_url=url)
        result = self._parse_page()
        return result

    def _new_proxy_needed(self):
        """
        implement in target page type class
        :return:
        """
        raise NotImplementedError()

    def _parse_page(self):
        """
        XPATH docs - https://www.w3schools.com/xml/xpath_syntax.asp
        CSS Selectors - https://www.w3schools.com/cssref/css_selectors.asp
        implement in target page type class
        :return:
        """
        raise NotImplementedError()

    def _try_resolve_captcha(self):
        """
        implement in target page type class using different
        methods from base class
        """
        raise NotImplementedError()

    def _is_current_page_captcha(self):
        """
        implement in target page type class
        :return:
        """
        raise NotImplementedError()

    def _find_captcha_block(self):
        """
        implement in target page type class
        :return:
        """
        raise NotImplementedError()

    def _insert_captcha_and_submit_page(self, _captcha_key: str):
        """
        implement in target page type class
        :param _captcha_key: captcha response key
        :return:
        """
        raise NotImplementedError()

    def _retrieve_information_exception_handler(self, exc: Exception, endpoint: str):
        """
        implement in target page type class
        :return:
        """
        raise NotImplementedError()
