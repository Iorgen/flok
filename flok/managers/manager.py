from queue import Queue
from flok.managers.exceptions import *
from flok.parser.extractor import Extractor
from flok.parser.base import BaseChromeDriverParser
from typing import Union
from collections.abc import Generator


class ParserManager:
    """ Spawns parser threads and manages URL's queue """

    PARSERS = []
    MAIN_THREAD_NAME = None

    def __init__(
            self,
            parse_urls: Union[Generator, list],
            thread_count: int = 4,
            dumper=None
    ):
        # How to defend own object
        # Check incoming types
        assert isinstance(thread_count, int)
        # TODO as BaseParser - Task (move non implemented functions into parser)

        if parse_urls is None:
            raise NothingToParseException

        elif isinstance(parse_urls, Generator):
            print('using generator')

        elif isinstance(parse_urls, list):
            if len(parse_urls) < 1:
                raise NothingToParseException
            else:
                pass

        else:
            raise TypeError("parse_urls should be Generator or list")
        # if isinstance(dumper, abc.Iterable):
        # Use it as iterable

        if dumper is None:
            # create default csv dumper object
            # self._dumper =
            pass

        # TODO write into csv header values
        self.thread_count = thread_count
        self._dumper = dumper
        self.parse_urls = parse_urls

    def begin_downloads(
            self,
            parser_creator,
    ):
        """
        Start the downloader threads, fill the queue with the URLs and\n
        then feed the threads URLs via the queue
        """
        queue = Queue()

        # TODO accept as parsing params dict and pass by key and value
        # Create a thread pool and give them a queue
        for i in range(self.thread_count):
            # Create new parser object
            parser = parser_creator()
            t = Extractor(
                queue=queue,
                parser=parser,
                dump_func=self._dumper
            )

            if i == 0:
                t.set_main_parser_id(t.name)
                self.MAIN_THREAD_NAME = t.name
            else:
                t.set_main_parser_id(self.MAIN_THREAD_NAME)

            t.setDaemon(True)
            t.start()

        # Load the queue from urls list
        for linkname in self.parse_urls:
            queue.put(linkname)
        # Wait for the queue to finish
        queue.join()
        # for _parser in self.PARSERS:
        #     _parser._DRIVER.stop_client()
        #     _parser._DRIVER.close()


# pass fabric class object which inherits from base fabric class
# Calling method get_parser