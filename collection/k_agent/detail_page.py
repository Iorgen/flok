import threading
import time
from collection.find_org.base import BaseFindOrgParser
from parser.exceptions import (
    LoadPageException, ResolveCaptchaException, RetrieveInformationFromPageException
)


class KAgentChromeBasedPageParser(BaseFindOrgParser):
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

        }
        # Need to be sure we parse target page
        base_info_tbl_x_path = """
            //body/form[1]/
            table[contains(@id, 'maintbl')][1]//
            td[contains(@id, 'maintbl_m')][1]//
            table[contains(@id, 'middletbl')][1]//
            td[contains(@id, 'middletbl_c')][1]//
            table[contains(@id, 'twintbl')][1]//
            td[contains(@id, 'twintbl_c')][1]    
        """
        main_table_sub_path = "/table[contains(@class, 'compdate')]/tbody"

        main_table_naming_path = {
            'name': "//span[contains(text(), 'Наименование')]/ancestor::th/following-sibling::td",
            'INN': "//span[contains(text(), 'ИНН')]/ancestor::th/following-sibling::td",
            'KPP': "//span[contains(text(), 'КПП')]/ancestor::th/following-sibling::td",
            'ORGN': "//span[contains(text(), 'ОГРН')]/ancestor::th/following-sibling::td",
            'OKPO': "//span[contains(text(), 'ОКПО')]/ancestor::th/following-sibling::td",
            'address': "//span[contains(text(), 'Адрес')]/ancestor::th/following-sibling::td",
            'phones': "//span[contains(text(), 'Телефон(ы)')]/ancestor::th/following-sibling::td",
        }
        okved_table_mapping = {
            # Main okved code
            'main_okved_code': "//tr[contains(@id, 'okvedRow_0')]/td[1]",
            # 'main_okved_code_type': "//tr[contains(@id, 'okvedRow_0')]/td[2]",
            # Additional okveds
            'okved_1_code': "//tr[contains(@id, 'okvedRow_1')]/td[1]",
            'okved_2_code': "//tr[contains(@id, 'okvedRow_2')]/td[1]",
            'okved_3_code': "//tr[contains(@id, 'okvedRowHdn_3')]/td[1]",
            'okved_4_code': "//tr[contains(@id, 'okvedRowHdn_4')]/td[1]",
            'okved_5_code': "//tr[contains(@id, 'okvedRowHdn_5')]/td[1]",
            'okved_6_code': "//tr[contains(@id, 'okvedRowHdn_6')]/td[1]",
        }

        for key, value in main_table_naming_path.items():
            try:
                target_text = self._DRIVER.find_element_by_xpath(
                    xpath=f"{base_info_tbl_x_path}{main_table_sub_path}{value}"
                ).text
                result[key] = target_text
            except Exception as E:
                self.LOGGER.warning(f"extract {key} from {self._DRIVER.current_url} fails with {E}")
                result[key] = ''

        for key, value in okved_table_mapping.items():
            try:
                target_text = self._DRIVER.find_element_by_xpath(
                    xpath=f"{value}"
                ).text
                result[key] = target_text
            except Exception as E:
                self.LOGGER.warning(f"extract {key} from {self._DRIVER.current_url} fails with {E}")
                result[key] = ''

        self.LOGGER.info(f'Parsing')
        try:
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
            result['url'] = url
            self.LOGGER.info(f"Page {self.BASE_URL}{url} parsed successfully")
            return result
            # JOB DONE

        except (LoadPageException, ResolveCaptchaException, RetrieveInformationFromPageException) as INTER_E:
            self.LOGGER.warning(f"Page {self.BASE_URL}{url} loading error with {INTER_E}")
            # self.LOGGER.warning(f"Page {self.BASE_URL}{url} loading error with {INTER_E}")
            # if self._MAIN_SOLVER_ID == threading.currentThread().getName():
            #     self._try_resolve_captcha()
            # else:
            #     time.sleep(10)
            #     self.retrieve_information(url=url)

        except Exception as E:
            self.LOGGER.warning(f"Page {self.BASE_URL}{url} loading error with {E}")
            # self.LOGGER.warning(f"Page {self.BASE_URL}{url} loading error with {E}")
            # if self._MAIN_SOLVER_ID == threading.currentThread().getName():
            #     self._try_resolve_captcha()
            # else:
            #     time.sleep(10)
            #     self.retrieve_information(url=url)

        finally:
            pass
