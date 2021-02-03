from config import Config
from parser.managers.manager import ParserManager
from parser.collection.find_org import FindOrgRetrieveInformationFromPageChromeParser

path_driver = '/drivers/chromedriver'


def main():
    cfg = Config()
    """ Execute parser script for OKVED parsing"""
    print("------------------------------------")
    # https://www.find-org.com/okved2/49.4/page/{N} - N_max 950 - ready
    # https://www.find-org.com/okved2/49.42/page/{N} - N_max 305
    # https://www.find-org.com/okved2/49.41.1/page/{N} - N_max 174
    # https://www.find-org.com/okved2/49.41.2/page/{N} - N_max 124
    # https://www.find-org.com/okved2/49.41.3/page/{N} - N_max 37
    parse_urls = []
    for i in range(1, 305):
        parse_urls.append(f'okved2/49.42/page/{i}')

    # Collections
    download_manager = ParserManager(
        parse_urls=parse_urls,
        output_file_path='dummy_path',
        thread_count=cfg.threads
    )

    download_manager.begin_downloads(
        _type='collection',
        _source='find_org'
    )

    # with open('find_org_collection_links', 'r') as file:
    #     pages_urls = file.readlines()
    # pages_urls = [x.strip() for x in pages_urls]
    # # manager;phones;phones_government_buy;status;INN;url
    #
    # d_m = ParserManager(
    #     parse_urls=pages_urls,
    #     output_file_path='dummy_path',
    #     thread_count=cfg.threads
    # )
    #
    # d_m.begin_downloads(
    #     _type='page',
    #     _source='find_org'
    # )
    print('parsing complete')

# my cap "91588f4fb9475bde03fdfee20cd709ed" -
# TODO optimize selenium settings page upload too long
# TODO An idea to mix selenium and bs4 - selenium for captcha insert bs4 for information retrieving
# TODO all dynamic params or in config or in args
# TODO if very after N captcha resolving setup new proxy change proxy
# TODO insert parsed url into result page
# Start not on server parser for MUST


if __name__ == '__main__':
    main()
