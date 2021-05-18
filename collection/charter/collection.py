
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


class CharterRetrieveCompanyUrlsByPageChromeParser(BaseCharter):
    """
    Each parser class should working in his own Thread
    Based on Queue
    """
    _retry_count = 3

    def _parse_page(self):
        try:
            orgs = self._DRIVER.find_elements_by_xpath("//body//a[contains(@data-link, 'organization-page')]")
            links = []
            for org in orgs:
                links.append(org.get_attribute('href'))
            return links
        except Exception as E:
            raise RetrieveInformationFromPageException()
