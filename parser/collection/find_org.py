from parser.base import BaseChromeCollectionParser


class FindOrgChromeCollectionParser(BaseChromeCollectionParser):

    def get(self):
        url = 'https://' + self.obj_ + ".n1.ru/snyat/dolgosrochno/kvartiry/?author=owner&page="
        pass

    def retrieve_information(self):
        # WHole logic about retrieve information
        # Simple steps
        #
        pass
