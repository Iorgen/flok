from flok.managers.manager import ParserManager
from flok.dumper.dumper import DictCsvDumper
from collection.a_ads.detail_page import AAdsChromeBasedDetailParser
from config.config import Config
cfg = Config()


def parser_creator():
    return AAdsChromeBasedDetailParser(
        captcha_key=cfg.cap_monster_auth_key,
        driver_path='drivers/driver',
        base_url=' '
    )


def create_links(_range: int):
    for _i in range(10, 100):
        yield f"https://a-ads.com/campaigns/{_i}"


def n_create_links():
    # TODO hardcode
    links = []
    for _i in range(10, 129170):
        links.append(f"https://a-ads.com/campaigns/{_i}")
    return links


def main():
    linker = n_create_links()
    cfg = Config()
    dumper = DictCsvDumper(
        file_path=f'data/a-ads/a-ads.csv'
    )

    d_m = ParserManager(
        parse_urls=linker,
        thread_count=cfg.threads,
        dumper=dumper,
    )

    d_m.begin_downloads(
        parser_creator=parser_creator,
    )


if __name__ == '__main__':
    main()
