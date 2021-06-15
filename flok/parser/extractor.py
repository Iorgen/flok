import binascii
import csv
import logging
import os
import threading
from queue import Queue
from threading import Thread
from flok.dumper.base import BaseDumper
from flok.parser.base import BaseParser

global_lock = threading.Lock()


class Extractor(Thread):
    """ Parser class -

    """

    LOGGER = logging.getLogger(__name__)

    def __init__(
            self,
            queue: Queue,
            parser: BaseParser,
            dump_func: BaseDumper
    ):
        Thread.__init__(self, name=binascii.hexlify(os.urandom(16)))
        self.queue = queue
        self.dumper = dump_func
        self.parser = parser

    def set_main_parser_id(self, main_id):
        self.parser.set_main_main_solver_id(main_id)

    def run(self):
        while True:
            try:
                url = self.queue.get()
                result = self.parser.retrieve_information(url)
                self.dumper.dump(dump_object=result)
                # self.csv_writer()
                self.queue.task_done()
                self.LOGGER.info(f"{self.parser.BASE_URL}{url} -" # {Source} {type} SUCCESS in {time}
                                 f" parsed successfully")
            except Exception as E:
                print(f'error{E}')
                # LOG SOMETHING
            if self.queue.empty():
                self.parser._DRIVER.close()

