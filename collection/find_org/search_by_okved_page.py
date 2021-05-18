
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


class FindOrgRetrieveCompanyUrlsByOkvedPageChromeParser(BaseFindOrgParser):
    """
    Each parser class should working in his own Thread
    Based on Queue
    """

    def _parse_page(self):
        """

        :return:
        """
        # TODO Refactor all as xpath
        try:

            links = []
            p_items = self._DRIVER.find_element_by_class_name(name='content-entrypoint').find_elements_by_tag_name(name='p')
            for _p in p_items:
                link = _p.find_element_by_tag_name("a")
                links.append(link.get_attribute('href').replace(self.BASE_URL, "", 1))
            return links
        except Exception as E:
            raise RetrieveInformationFromPageException()

    # def retrieve_information(self, url):
    #     """
    #
    #     :return:
    #     """
    #     try:
    #         # JOB START
    #         self._load_html_page(_endpoint_url=url)
    #         result = self._parse_page()
    #         write_links_to_file(links=result, filename='find_org_collection_links')
    #         self.LOGGER.info(f"{self.BASE_URL}{url} - parsed successfully")
    #         # JOB DONE
    #     except Exception as E:
    #         self.LOGGER.warning(f"- {self.BASE_URL}{url} - load error with {E}")
    #         if self._MAIN_SOLVER_ID == threading.currentThread().getName():
    #             self._try_resolve_captcha()
    #         else:
    #             time.sleep(10)
    #             self.retrieve_information(url=url)
    #     finally:
    #         pass


