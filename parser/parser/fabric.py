from collection.find_org.search_by_okved_page import FindOrgRetrieveCompanyUrlsByOkvedPageChromeParser
from collection.find_org.detail_page import FindOrgRetrieveInformationFromPageChromeParser
from collection.k_agent.detail_page import KAgentChromeBasedPageParser
from config.config import Config
cfg = Config()


class ChromeDriverParserFabric:
    # TODO as Singleton
    def get_parser(self, _source, _type, _driver_path):
        if _type == "collection":
            if _source == 'find_org':
                return FindOrgRetrieveCompanyUrlsByOkvedPageChromeParser(
                    captcha_key=cfg.cap_monster_auth_key,
                    driver_path=_driver_path,
                    base_url='https://www.find-org.com/'

                )
        elif _type == "page":
            if _source == 'find_org':
                return FindOrgRetrieveInformationFromPageChromeParser(
                    captcha_key=cfg.cap_monster_auth_key,
                    driver_path=_driver_path,
                    base_url='https://www.find-org.com/'
                )
            if _source == 'k_agent':
                pass
                return KAgentChromeBasedPageParser(
                    captcha_key=cfg.cap_monster_auth_key,
                    driver_path=_driver_path,
                    base_url='https://www.k-agent.ru/catalog/'
                )
