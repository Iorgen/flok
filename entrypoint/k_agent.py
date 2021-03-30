from config.config import Config
from parser.managers.manager import ParserManager
import csv
import logging
logger = logging.getLogger("K-agent Parser")


def parse_k_agent_target_page():
    # restart from
    cfg = Config()
    print("K AGENT ")
    links = []

    with open('data/legal_entities.csv', 'rU') as infile:
        # read the file as a dictionary for each row ({header : value})
        reader = csv.DictReader(infile, delimiter=';')
        data = {}
        for row in reader:
            for header, value in row.items():
                try:
                    data[header].append(value)
                except KeyError:
                    data[header] = [value]

    for _i in range(len(data['inn'])):
        links.append(f"{data['inn'][_i]}-{data['ogrn'][_i]}")
    # for _row in len(data['inn']:
    #     links.append()

    print("LINKS READY")

    d_m = ParserManager(
        parse_urls=links,
        output_file_path='data/k_agent_results.csv',
        thread_count=cfg.threads
    )

    d_m.begin_downloads(
        _type='page',
        _source='k_agent'
    )
    print('DONE -----------------------------------')
