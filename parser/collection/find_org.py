import time
import threading
from parser.base import BaseChromeDriverParser
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from parser.exceptions import (
    LoadPageException, ResolveCaptchaException, RetrieveInformationFromPageException
)
from parser.dumper import (
    write_links_to_file, write_dict_information_into_csv
)


class BaseFindOrgParser(BaseChromeDriverParser):
    _ONE_PROXY_LIMIT = 40
    CAPTCHA_ENDPOINT = 'bot.html'
    # TODO cut down BASE_URL via __init__

    """
        Using chrome based parser this class abstract retrieving information from
        collection of given pages.
        - for given pages load on every url using generator function
        """
    CAPTCHA_USAGE = 0

    @classmethod
    def captcha_capacity(cls):
        print(cls.CAPTCHA_USAGE)

    def load_page(self):
        raise NotImplementedError()

    def reload_page(self):
        raise NotImplementedError()

    def _load_html_page(self, _endpoint_url):
        """
        load page by url into self.DRIVER
        :param _page_url:
        :return:
        """
        try:
            self._DRIVER.get(f"{self.BASE_URL}{_endpoint_url}")
            # print(f" {self.BASE_URL}{_endpoint_url}")
        except WebDriverException as WDE:
            self._try_resolve_captcha()
        # except TimeoutException as TE:
        #     self.LOGGER
        #     # TODO wait and and retry
        except Exception as e:
            # TODO wait N seconds
            self._try_resolve_captcha()
            self.LOGGER.warining(f'Attempt to load page {self.BASE_URL}{_endpoint_url} fails with {e}')
            raise LoadPageException()

    def _try_resolve_captcha(self):
        try:
            # if BaseFindOrgParser.CAPTCHA_USAGE > self._ONE_PROXY_LIMIT:
            #     self._change_proxy()
            #     self._next_proxy()
            time.sleep(5)
            self._DRIVER.get(f"{self.BASE_URL}{self.CAPTCHA_ENDPOINT}")
            base64_captcha_image = self._try_to_find_captcha_block()
            if base64_captcha_image is not None:
                captcha_key = self._cap_monster_solver(image_base64=base64_captcha_image)
                if captcha_key is not None:
                    self._insert_captcha_and_submit_page(_captcha_key=captcha_key)
                    BaseFindOrgParser.CAPTCHA_USAGE = BaseFindOrgParser.CAPTCHA_USAGE + 1
                    self.LOGGER.info(f"Solved {BaseFindOrgParser.CAPTCHA_USAGE} captchas")
                    print("captcha solved")
                    # Save img with captcha answer name to data folder in debug mode
                    # image = base64.b64decode(str(base64_captcha_image))
                    # with open("data/imageToSave.png", "wb") as fh:
                    #     fh.write(base64.decodebytes(image))
                    # img = Image.open(io.BytesIO(image))
                    # img.save(f'data/{captcha_key}.jpeg', 'jpeg')
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
            # TODO maybe this needs to save and only then send
            # Need try to handle this sheet
            # with open(r"image.jpg", 'wb') as f:
            #     f.write(base64.b64decode(img_base64))
        except Exception as E:
            self.LOGGER.warning(f"Captcha was not found because {E}")
        finally:
            return img_captcha_base64

    def _insert_captcha_and_submit_page(self, _captcha_key: str):
        captcha_input = self._DRIVER.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/form[1]/input[@name="keystring"]')
        captcha_input.send_keys(_captcha_key)
        captcha_input.submit()
        # /html/body/div[1]/div[2]/div[1]/form[1]/input[@name='keystring'] XPATH for input
        # /html/body/div[1]/div[2]/div[1]/form[1]/input[@type='submit'] - for submit


class FindOrgRetrieveCompanyUrlsByOkvedPageChromeParser(BaseFindOrgParser):
    """
    Each parser class should working in his own Thread
    Based on Queue
    Or on
    """

    def _parse_page(self):
        """

        :return:
        """
        # TODO Refactor all as xpath
        links = []
        p_items = self._DRIVER.find_element_by_class_name(name='content-main').find_elements_by_tag_name(name='p')
        for _p in p_items:
            link = _p.find_element_by_tag_name("a")
            links.append(link.get_attribute('href').replace(self.BASE_URL, "", 1))
        return links

    def retrieve_information(self, url):
        """

        :return:
        """
        try:
            # JOB START
            self._load_html_page(_endpoint_url=url)
            result = self._parse_page()
            write_links_to_file(links=result, filename='find_org_collection_links')
            self.LOGGER.info(f"{self.BASE_URL}{url} - parsed successfully")
            # JOB DONE
        except (LoadPageException, ResolveCaptchaException) as INTER_E:
            self.LOGGER.warning(f"- {self.BASE_URL}{url} - load error with {INTER_E}")
            if self._MAIN_SOLVER_ID == threading.currentThread().getName():
                self._try_resolve_captcha()
            else:
                time.sleep(10)
                self.retrieve_information(url=url)
        except NoSuchElementException as NSEE:
            self.LOGGER.warning(f" No element on page - {self.BASE_URL}{url} - start captcha resolving")
            if self._MAIN_SOLVER_ID == threading.currentThread().getName():
                self._try_resolve_captcha()
            else:
                time.sleep(10)
                self.retrieve_information(url=url)
        except Exception as E:
            self.LOGGER.warning(f"- {self.BASE_URL}{url} - load error with {E}")
            if self._MAIN_SOLVER_ID == threading.currentThread().getName():
                self._try_resolve_captcha()
            else:
                time.sleep(10)
                self.retrieve_information(url=url)
        finally:
            pass


class FindOrgRetrieveInformationFromPageChromeParser(BaseFindOrgParser):
    """
    Из каждой страницы извлекается ниже указанная информация
    - Руководитель ФИО +
    - Телефоны +
    - Статус +
    - Телефон(ы) по данным госзакупок +
    - коды ОКВЕД -

    """

    @staticmethod
    def remove_prefix(s, prefix):
        return s[len(prefix):] if s.startswith(prefix) else s

    # TODO Retry decorator
    def _parse_page(self):
        """

        :return:
        """
        result = {
            'manager': '',
            'phones': '',
            'phones_government_buy': '',
            'status': '',
            'INN': '',
            # 'main_okved_codes': [],
            # 'additional_okved_codes': []
        }
        # Need to be sure we parse target page
        title = self._DRIVER.find_element_by_xpath(
            xpath=u"//body/div[1]/div[2]/div[1]/div[contains(@class, 'title')][1]"
        ).text
        self.LOGGER.info(f'Parsing {title}')
        # body/div[1]/div[2]/div[1]/div[contains(@class, 'title')][1]
        try:
            try:
                # GET Company status
                result['status'] = self._DRIVER.find_element_by_xpath(
                    xpath=u"//i[contains(text(), 'Статус')]/following-sibling::span"
                ).text
            except Exception as E:
                self.LOGGER.warning(f"Status name does not exists")
                pass

            try:
                # GET Company INN
                result['INN'] = self._DRIVER.find_element_by_xpath(
                    xpath=u"//i[contains(text(), 'ИНН')]/following-sibling::a"
                ).text
            except Exception as E:
                self.LOGGER.warning(f"INN does not exists")
                pass

            try:
                # Get company manager personal information
                result['manager'] = self._DRIVER.find_element_by_xpath(
                    xpath=u"//i[contains(text(), 'Руководитель')]/following-sibling::a"
                ).text
            except Exception as E:
                self.LOGGER.warning(f"manager name does not exists")
                pass

            try:
                # Get Company phones by gov
                result['phones_government_buy'] = self._DRIVER.find_element_by_xpath(
                    xpath=u"//i[contains(text(),'Телефон(ы) по данным госзакупок:')]/ancestor::p").text
                result['phones_government_buy'] = self.remove_prefix(result['phones_government_buy'], 'Телефон(ы) по данным госзакупок:')
            except Exception as E:
                self.LOGGER.warning(f"GOVERNMENT phone numbers does not exists")
                pass

            try:
                # Get Company phones
                result['phones'] = self._DRIVER.find_element_by_xpath(
                    xpath=u"//i[contains(text(), 'Телефон(ы):')]/ancestor::p"
                ).text
                result['phones'] = self.remove_prefix(result['phones'], 'Телефон(ы):')

            except Exception as E:
                self.LOGGER.warning(f"REGULAR phone numbers does not exists")
                pass

        except Exception as E:
            self.LOGGER.error(f"Information retrieve fails with {E}")
            raise RetrieveInformationFromPageException()

        return result

    def retrieve_information(self, url):
        """
        # TODO retry page amount
        :return:
        """

        try:
            # JOB START
            self._load_html_page(_endpoint_url=url)
            result = self._parse_page()
            # Better use database as storage for all links
            result['url'] = url
            write_dict_information_into_csv(links=result, filename='find_org_company_information.csv')
            self.LOGGER.info(f"Page {self.BASE_URL}{url} parsed successfully")
            # JOB DONE

        except (LoadPageException, ResolveCaptchaException, RetrieveInformationFromPageException) as INTER_E:
            self.LOGGER.warning(f"Page {self.BASE_URL}{url} loading error with {INTER_E}")
            if self._MAIN_SOLVER_ID == threading.currentThread().getName():
                self._try_resolve_captcha()
            else:
                time.sleep(10)
                self.retrieve_information(url=url)

        except Exception as E:
            self.LOGGER.warning(f"Page {self.BASE_URL}{url} loading error with {E}")
            if self._MAIN_SOLVER_ID == threading.currentThread().getName():
                self._try_resolve_captcha()
            else:
                time.sleep(10)
                self.retrieve_information(url=url)

        finally:
            pass
