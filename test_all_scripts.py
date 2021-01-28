import os
from threading import Thread
from queue import Queue
import binascii
import logging
from parser.base import BaseParser
from parser.dumper import write_links_to_file
import time

class Parser(Thread):
    """ Parser class -
        TODO fill description reads queue and parse each urls using abstraction
    """
    CAP_USE = 0
    LOGGER = logging.getLogger(__name__)

    def __init__(
            self,
            queue: Queue,

    ):
        Thread.__init__(self, name=binascii.hexlify(os.urandom(16)))
        self.queue = queue


    @classmethod
    def dum_m(cls):
        print(cls.CAP_USE)

    def run(self):
        while True:
            Parser.CAP_USE = Parser.CAP_USE + 1
            url = self.queue.get()
            # time.sleep(5)
            self.queue.task_done()
            print(url)


class ParserManager:
    """ Spawns parser threads and manages URL's queue """

    PARSERS = []
    MAIN_THREAD_NAME = None

    def __init__(self, parse_urls: list, output_file_path: str, thread_count: int =4):
        self.thread_count = thread_count
        self.output_file_path = output_file_path
        self.parse_urls = parse_urls

    def begin_downloads(self, _type: str, _source: str):
        # TODO raise error if queue is not empty for this manager
        #   this manager is busy
        #   refactor on *args **kwargs which
        #   invokes directly into Parser class
        #   Exceptions on empty input etc

        """
        Start the downloader threads, fill the queue with the URLs and\n
        then feed the threads URLs via the queue
        """

        queue = Queue()

        # TODO accept as parsing params dict and pass by key and value
        # Create a thread pool and give them a queue
        for i in range(self.thread_count):

            t = Parser(
                queue=queue
            )
            t.setDaemon(True)
            t.start()

        # Load the queue from urls list
        for linkname in self.parse_urls:
            queue.put(linkname)

        # Wait for the queue to finish
        queue.join()


if __name__ == '__main__':
    with open('find_org_collection_links', 'r') as file:
        pages_urls = file.readlines()
    pages_urls = [x.strip() for x in pages_urls]

    d_m = ParserManager(
        parse_urls=pages_urls,
        output_file_path='dummy_path',
        thread_count=4
    )
    d_m.begin_downloads(
        _type='page',
        _source='find_org'
    )
    Parser.dum_m()
