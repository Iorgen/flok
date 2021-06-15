from config.config import Config
from parser.managers.manager import ParserManager


def parse_find_org_collection():
    cfg = Config()
    with open('find_org_collection_links', 'r') as file:
        pages_urls = file.readlines()
    pages_urls = [x.strip() for x in pages_urls]
    # manager;phones;phones_government_buy;status;INN;url

    d_m = ParserManager(
        parse_urls=pages_urls,
        output_file_path='find_org_company_information.csv',
        thread_count=cfg.threads
    )

    d_m.begin_downloads(
        _type='page',
        _source='find_org'
    )
    print('parsing complete')