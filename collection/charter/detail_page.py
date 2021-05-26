

import threading
import time

from selenium.common.exceptions import NoSuchElementException

from collection.find_org.base import BaseFindOrgParser
from parser.dumper import (
    write_links_to_file
)
from parser.exceptions import (
    LoadPageException, ResolveCaptchaException, RetrieveInformationFromPageException
)
from collection.charter.base import BaseCharter


class CharterChromeBasedPageParser(BaseCharter):
    """
    Each parser class should working in his own Thread
    Based on Queue
    """
    _retry_count = 3

    # @property
    def _parse_page(self):
        result = {
            'PROFILE': ' ',
            'OKVED': ' ',
            'ACTIVITY': ' ',
            'TITLE': '',

            'ADDRESS': ' ',
            'NAME': ' ',
            'TYPE': ' ',
            'PHONE': ' ',
            'E-MAIL': ' ',

            'added_date': ' ',
            'ORGN': ' ',
            'INN': ' ',
            'KPP': ' ',
        }
        """
        
        :return:
        """
        try:
            try:
                result['PROFILE'] = self._DRIVER.find_element_by_xpath(
                    xpath=u"//dt[contains(text(), 'Профиль')]/following-sibling::dd/a/span"
                ).text
            except Exception as E:
                self.LOGGER.warning(f"Status name does not exists")
                pass

            try:
                result['OKVED'] = self._DRIVER.find_element_by_xpath(
                    xpath=u"//dt[contains(text(), 'ОКВЭД')]/following-sibling::dd"
                ).text

                result['OKVED'] = result['OKVED'].replace("\n", " ")
            except Exception as E:
                self.LOGGER.warning(f"Status name does not exists")
                pass

            try:
                block = self._DRIVER.find_element_by_xpath(
                    xpath=u"//body/div[1]"
                )
                result['ACTIVITY'] = block.text.split('\n')[-1]
            except Exception as E:
                self.LOGGER.warning(f"Status name does not exists")
                pass

            try:
                result['TITLE'] = self._DRIVER.find_element_by_xpath(
                    xpath=u"//body/section[1]/div[1]/div[1]/div[1]/h1"
                ).text
            except Exception as E:
                self.LOGGER.warning(f"Status name does not exists")
                pass

            try:
                result['ADDRESS'] = self._DRIVER.find_element_by_xpath(
                    xpath=u"//dt[contains(text(), 'Адрес')]/following-sibling::dd"
                ).text
            except Exception as E:
                self.LOGGER.warning(f"Status name does not exists")
                pass

            try:
                result['NAME'] = self._DRIVER.find_element_by_xpath(
                    xpath=u"//dt[contains(text(), 'ФИО руководителя')]/following-sibling::dd"
                ).text
            except Exception as E:
                self.LOGGER.warning(f"INN does not exists")
                pass

            try:
                result['TYPE'] = self._DRIVER.find_element_by_xpath(
                    xpath=u"//dt[contains(text(), 'Должность руководителя')]/following-sibling::dd"
                ).text
            except Exception as E:
                self.LOGGER.warning(f"INN does not exists")
                pass

            try:
                result['PHONE'] = self._DRIVER.find_element_by_xpath(
                    xpath=u"//dt[contains(text(), 'Телефон')]/following-sibling::dd"
                ).text
            except Exception as E:
                self.LOGGER.warning(f"manager name does not exists")
                pass

            try:
                result['E-MAIL'] = self._DRIVER.find_element_by_xpath(
                    xpath=u"//dt[contains(text(), 'E-mail')]/following-sibling::dd"
                ).text
            except Exception as E:
                self.LOGGER.warning(f"GOVERNMENT phone numbers does not exists")
                pass

            # Second block
            try:
                result['added_date'] = self._DRIVER.find_element_by_xpath(
                    xpath=u"//dt[contains(text(), 'Дата присоединения')]/following-sibling::dd"
                ).text
            except Exception as E:
                self.LOGGER.warning(f"REGULAR phone numbers does not exists")
                pass

            try:
                result['ORGN'] = self._DRIVER.find_element_by_xpath(
                    xpath=u"//dt[contains(text(), 'ОГРН')]/following-sibling::dd"
                ).text
            except Exception as E:
                self.LOGGER.warning(f"REGULAR phone numbers does not exists")
                pass

            try:
                result['INN'] = self._DRIVER.find_element_by_xpath(
                    xpath=u"//dt[contains(text(), 'ИНН')]/following-sibling::dd"
                ).text
            except Exception as E:
                self.LOGGER.warning(f"REGULAR phone numbers does not exists")
                pass

            try:
                result['KPP'] = self._DRIVER.find_element_by_xpath(
                    xpath=u"//dt[contains(text(), 'КПП')]/following-sibling::dd"
                ).text
            except Exception as E:
                self.LOGGER.warning(f"REGULAR phone numbers does not exists")
                pass
            return result
        except Exception as E:
            raise RetrieveInformationFromPageException()
