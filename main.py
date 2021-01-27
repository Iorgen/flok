# Read csv with inn, kpp, ogrn
# This can help
# https://pastebin.com/QrZG9e9T
# https://pymotw.com/2/multiprocessing/basics.html
# https://medium.com/analytics-vidhya/asyncio-threading-and-multiprocessing-in-python-4f5ff6ca75e8
# https://www.machinelearningplus.com/python/parallel-processing-python/


import csv
from parser.managers.manager import ParserManager

path_driver = '/drivers/chromedriver'

def main():

    """ Execute """
    print("------------------------------------")
    # TODO as args while script starting
    # TODO read all from file firstly need to generate
    # https://www.find-org.com/okved2/49.4/page/{N} - N_max 950
    # https://www.find-org.com/okved2/49.42/page/{N} - N_max 305
    # https://www.find-org.com/okved2/49.41.1/page/{N} - N_max 174
    # https://www.find-org.com/okved2/49.41.2/page/{N} - N_max 124
    # https://www.find-org.com/okved2/49.41.3/page/{N} - N_max 37
    parse_urls = []
    for i in range(1, 949):
        parse_urls.append(f'okved2/49.4/page/{i}')

    # Collections
    # download_manager = ParserManager(
    #     parse_urls=parse_urls,
    #     output_file_path='dummy_path',
    #     thread_count=6
    # )
    #
    # download_manager.begin_downloads(
    #     _type='collection',
    #     _source='find_org'
    # )
    with open('find_org_collection_links', 'r') as file:
        pages_urls = file.readlines()
    pages_urls = [x.strip() for x in pages_urls]

    # with open('find_org_company_information.csv', 'w', newline='') as csvfile:
    #     fieldnames = ['first_name', 'last_name']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #
    #     writer.writeheader()
    #     writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    # Pages

    # manager;phones;phones_government_buy;status;INN;main_okved_codes;additional_okved_codes

    d_m = ParserManager(
        parse_urls=pages_urls,
        output_file_path='dummy_path',
        thread_count=4
    )
    d_m.begin_downloads(
        _type='page',
        _source='find_org'
    )


if __name__ == '__main__':
    main()
