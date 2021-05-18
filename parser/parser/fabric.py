from collection.find_org.search_by_okved_page import FindOrgRetrieveCompanyUrlsByOkvedPageChromeParser
from collection.find_org.detail_page import FindOrgRetrieveInformationFromPageChromeParser
from collection.k_agent.detail_page import KAgentChromeBasedPageParser
from collection.charter.collection import CharterRetrieveCompanyUrlsByPageChromeParser
from collection.charter.detail_page import CharterChromeBasedPageParser
from parser.exceptions import NoParserByParamsException
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
            if _source == "charter":
                return CharterRetrieveCompanyUrlsByPageChromeParser(
                    captcha_key=cfg.cap_monster_auth_key,
                    driver_path=_driver_path,
                    base_url='https://хартия-атс.радо.рус/'
                )
            else:
                raise NoParserByParamsException()
        elif _type == "page":
            if _source == 'find_org':
                return FindOrgRetrieveInformationFromPageChromeParser(
                    captcha_key=cfg.cap_monster_auth_key,
                    driver_path=_driver_path,
                    base_url='https://www.find-org.com/'
                )
            if _source == 'k_agent':
                return KAgentChromeBasedPageParser(
                    captcha_key=cfg.cap_monster_auth_key,
                    driver_path=_driver_path,
                    base_url='https://www.k-agent.ru/catalog/'
                )
            if _source == "charter":
                return CharterChromeBasedPageParser(
                    captcha_key=cfg.cap_monster_auth_key,
                    driver_path=_driver_path,
                    base_url=' '
                )
            else:
                raise NoParserByParamsException()
        else:
            raise NoParserByParamsException()
