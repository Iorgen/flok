import time

from selenium.common.exceptions import WebDriverException

from parser.base import BaseChromeDriverParser
from parser.exceptions import (
    ResolveCaptchaException
)


# TODO retrieve information should return dict or None
#   for parser manager
class BaseFindOrgParser(BaseChromeDriverParser):
    _CAPTCHA_RETRIES = 3
    _CAP_MONSTER_SOLVER_SLEEP_TIME = 2
    _ONE_PROXY_LIMIT = 40
    CAPTCHA_ENDPOINT = 'bot.html'
    CAPTCHA_USAGE = 0
    """
        # Description for Find Org
        Using chrome based parser this class abstract retrieving information from
        collection
        """

    @classmethod
    def captcha_capacity(cls):
        return cls.CAPTCHA_USAGE

    def _try_resolve_captcha(self):
        try:
            # TODO setup maximum delay for captcha
            # if BaseFindOrgParser.CAPTCHA_USAGE > self._ONE_PROXY_LIMIT:
            #     self._change_proxy()
            #     self._next_proxy()
            time.sleep(5)
            self._DRIVER.get(f"{self.BASE_URL}{self.CAPTCHA_ENDPOINT}")
            base64_captcha_image = self._try_to_find_captcha_block()
            if base64_captcha_image is not None:
                captcha_key = self._cap_monster_base64_image_solver(image_base64=base64_captcha_image)
                if captcha_key is not None:
                    self._insert_captcha_and_submit_page(_captcha_key=captcha_key)
                    BaseFindOrgParser.CAPTCHA_USAGE = BaseFindOrgParser.CAPTCHA_USAGE + 1
                    self.LOGGER.info(f"Solved {BaseFindOrgParser.CAPTCHA_USAGE} captchas")
                else:
                    raise ResolveCaptchaException()
            else:
                raise ResolveCaptchaException()

        except WebDriverException as WE:
            self.LOGGER.exception(f'Attempt to load resolve captcha fails with {WE}')
            raise ResolveCaptchaException()
        except Exception as E:
            self.LOGGER.exception(f'Attempt to load resolve captcha fails with {E}')
            raise ResolveCaptchaException()

    def _try_to_find_captcha_block(self):
        img_captcha_base64 = None
        try:
            captcha_block = self._DRIVER.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/form[1]/img")
            img_captcha_base64 = self._DRIVER.execute_async_script("""
                    var ele = arguments[0], callback = arguments[1];
                    ele.addEventListener('load', function fn(){
                      ele.removeEventListener('load', fn, false);
                      var cnv = document.createElement('canvas');
                      cnv.width = this.width; cnv.height = this.height;
                      cnv.getContext('2d').drawImage(this, 0, 0);
                      callback(cnv.toDataURL('image/jpeg').substring(22));
                    }, false);
                    ele.dispatchEvent(new Event('load'));
                    """, captcha_block)
        except Exception as E:
            self.LOGGER.warning(f"Captcha was not found because {E}")
        finally:
            return img_captcha_base64

    def _insert_captcha_and_submit_page(self, _captcha_key: str):
        captcha_input = self._DRIVER.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/form[1]/input[@name="keystring"]')
        captcha_input.send_keys(_captcha_key)
        captcha_input.submit()
