from config.config import Config
from parser.managers.manager import ParserManager
from entrypoint.k_agent import parse_k_agent_target_page
from preparation.links.fabric import LinkCreatorFabric
from dumper.base import DumpFabric
import argparse
parser = argparse.ArgumentParser(description='Videos to images')
parser.add_argument(
    '-s', '--source',
    type=str,
    default='',
    help='source from which to get information'
)
parser.add_argument(
    '-t', '--type',
    type=str,
    default='',
    help='Output dir for image'
)


def main():
    cfg = Config()
    """ Execute parser script for"""
    print("------------------------------------")
    dependencies = parser.parse_args()
    link_creator = LinkCreatorFabric.get_link_creator(
        _source=dependencies.source,
        _type=dependencies.type
    )
    links = link_creator.create_links()
    d_m = ParserManager(
        parse_urls=links,
        output_file_path=f'data/{dependencies.source}/charter_page_results.csv',
        thread_count=cfg.threads,
        dump_func=DumpFabric.get_dumper(_type=dependencies.type)
    )

    d_m.begin_downloads(
        _type=dependencies.type,
        _source=dependencies.source
    )

# my cap "91588f4fb9475bde03fdfee20cd709ed" -


if __name__ == '__main__':
    main()

# Main tasks
# singleton config - перенести все параметры в него
# TODO optimize selenium settings page upload too long
# TODO An idea to mix selenium and bs4 - selenium for captcha insert bs4 for information retrieving
# TODO Метод wait перенести все sleep используя wait
# TODO Check on previous parsers that all changed struct is working
# TODO if very after N captcha resolving setup new proxy change proxy
# TODO insert parsed url into result page
# TODO Get link creator, parser and result writer from fabric methods
