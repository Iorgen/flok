from flok.parser.exceptions import (
    LoadPageException, ResolveCaptchaException, RetrieveInformationFromPageException
)
from flok.parser.base import BaseChromeDriverParser


class AAdsChromeBasedDetailParser(BaseChromeDriverParser):
    """
    Each parser class should working in his own Thread
    Based on Queue
    """
    _USE_PROXY = True
    _retry_count = 3
    _CAPTCHA_RETRIES = 3
    _CAP_MONSTER_SOLVER_SLEEP_TIME = 2
    _ONE_PROXY_LIMIT = 40

    CAPTCHA_ENDPOINT = 'bot.html'
    CAPTCHA_USAGE = 0

    def _parse_page(self):
        result = {
            'campaign_url': self._DRIVER.current_url,
            'resource_link': ' ',
            'is404': False,
            'daily_budget': ' ',
            'total_budget': ' ',
            'already_spent': ' ',
            'impressions': ' ',
            'clicks': ' ',
            'traffic': ' '
        }
        """

        :return:
        """
        try:
            # Try check 404 page if success return fully empty array
            try:
                status = self._DRIVER.find_element_by_xpath(
                    "//body//div[contains(@class,'errors__status')]"
                )
                if status.text == '404':
                    result['is404'] = True
                    return result
            except Exception as E:
                pass

            try:
                resource_links = self._DRIVER.find_element_by_xpath(
                    "//body//div[contains(@class,'v--campaigns--show')]//"
                    "div[contains(@class, 'ad-preview')]//div[contains(@class, 'ad')]//a"
                )
                result['resource_link'] = resource_links.get_attribute('href')
            except Exception as E:
                self.LOGGER.warning(f"non exist")
                pass
            # Budgets
            try:
                daily_budget = self._DRIVER.find_element_by_xpath(
                    "//div[contains(@class, 'p--campaigns--show--main-block')]"
                    "//strong[contains(text(),'Daily budget:')]/parent::div/nobr"
                )
                result['daily_budget'] = daily_budget.text
            except Exception as E:
                self.LOGGER.warning(f"non exist")
                pass

            try:
                total_budget = self._DRIVER.find_element_by_xpath(
                    "//div[contains(@class, 'p--campaigns--show--main-block')]"
                    "//strong[contains(text(),'Total budget:')]/parent::div/nobr"
                )
                result['total_budget'] = total_budget.text
            except Exception as E:
                self.LOGGER.warning(f"non exist")
                pass

            try:
                already_spent = self._DRIVER.find_element_by_xpath(
                    "//div[contains(@class, 'p--campaigns--show--main-block')]"
                    "//strong[contains(text(),'Already spent:')]/parent::div/nobr"
                )
                result['already_spent'] = already_spent.text
            except Exception as E:
                self.LOGGER.warning(f"non exist")
                pass

            # Impressions
            try:
                impressions = self._DRIVER.find_element_by_xpath(
                    "//span[contains(@data-metric, 'impressions_sum_human')]"
                )
                result['impressions'] = impressions.text
            except Exception as E:
                self.LOGGER.warning(f"non exist")
                pass

            # clicks

            try:
                clicks = self._DRIVER.find_element_by_xpath(
                    "//span[contains(@data-metric, 'clicks_sum_human')]"
                )
                result['clicks'] = clicks.text
            except Exception as E:
                self.LOGGER.warning(f"non exist")
                pass

            # Traffic
            try:
                traffic = self._DRIVER.find_element_by_xpath(
                    "//p[contains(text(), 'Traffic sources:')]/following-sibling::ul"
                )
                result['traffic'] = traffic.text
            except Exception as E:
                self.LOGGER.warning(f"non exist")
                pass

            return result
        except Exception as E:
            raise RetrieveInformationFromPageException()