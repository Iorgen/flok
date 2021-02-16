import binascii
import csv
import logging
import os
import threading
from queue import Queue
from threading import Thread

from parser.base import BaseParser

global_lock = threading.Lock()


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
            result = self.parser.retrieve_information(url)
            self.csv_writer(output_file_path=self.output_file_path, row=result)
            self.queue.task_done()
            if self.queue.empty():
                self.parser._DRIVER.close()

        # TODO Solve task with driver closing when Thread finish his job
    @staticmethod
    def csv_writer(output_file_path: str, row: dict):
        with global_lock:
            with open(output_file_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(row.values())
