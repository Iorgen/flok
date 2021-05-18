import threading
import time
from collection.find_org.base import BaseFindOrgParser
from parser.exceptions import (
    LoadPageException, ResolveCaptchaException, RetrieveInformationFromPageException
)


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

    # def retrieve_information(self, url):
    #     """
    #     # TODO retry page amount
    #     :return:
    #     """
    #     try:
    #         # JOB START
    #         self._load_html_page(_endpoint_url=url)
    #         result = self._parse_page()
    #         result['url'] = url
    #         self.LOGGER.info(f"Page {self.BASE_URL}{url} parsed successfully")
    #         return result
    #
    #     except Exception as E:
    #         self.LOGGER.warning(f"Page {self.BASE_URL}{url} loading error with {E}")
    #         if self._MAIN_SOLVER_ID == threading.currentThread().getName():
    #             self._try_resolve_captcha()
    #         else:
    #             time.sleep(10)
    #             self.retrieve_information(url=url)
    #     finally:
    #         pass
