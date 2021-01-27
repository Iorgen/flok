from parser.collection.find_org import (
    FindOrgRetrieveCompanyUrlsByOkvedPageChromeParser,
    FindOrgRetrieveInformationFromPageChromeParser
)


class ChromeDriverParserFabric:
    # TODO as Singleton

    def get_parser(self, _source, _type, _driver_path):
        if _type == "collection":
            if _source == 'find_org':
                return FindOrgRetrieveCompanyUrlsByOkvedPageChromeParser(
                    driver_path=_driver_path,
                    base_url='https://www.find-org.com/'
                )
        elif _type == "page":
            if _source == 'find_org':
                return FindOrgRetrieveInformationFromPageChromeParser(
                    driver_path=_driver_path,
                    base_url='https://www.find-org.com/'
                )

