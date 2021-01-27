import os
from threading import Thread
from queue import Queue
import binascii
import logging
from parser.base import BaseParser
from parser.dumper import write_links_to_file


class Parser(Thread):
    """ Parser class -
        TODO fill description reads queue and parse each urls using abstraction
    """

    LOGGER = logging.getLogger(__name__)

    def __init__(
            self,
            queue: Queue,
            output_file_path: str,
            parser: BaseParser,

    ):
        Thread.__init__(self, name=binascii.hexlify(os.urandom(16)))
        self.queue = queue
        self.output_file_path = output_file_path
        self.parser = parser

    def set_main_parser_id(self, main_id):
        self.parser.set_main_main_solver_id(main_id)

    def run(self):
        while True:
            url = self.queue.get()
            self.parser.retrieve_information(url)
            # TODO i can put url here is catch some error from parser
            self.queue.task_done()
            if self.queue.empty():
                self.parser._DRIVER.close()

        # TODO Solve task with driver closing when Thread finish his job
