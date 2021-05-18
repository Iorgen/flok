import binascii
import csv
import logging
import os
import threading
from queue import Queue
from threading import Thread
from dumper.base import CsvDumper
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
            dump_func=None
    ):
        Thread.__init__(self, name=binascii.hexlify(os.urandom(16)))
        self.queue = queue
        self.output_file_path = output_file_path
        if dump_func is None:
            self._dump_func = CsvDumper.dump_row_to_csv
        else:
            self._dump_func = dump_func
        self.parser = parser

    def set_main_parser_id(self, main_id):
        self.parser.set_main_main_solver_id(main_id)

    def run(self):
        while True:
            try:
                url = self.queue.get()
                result = self.parser.retrieve_information(url)
                self._dump_func(result, self.output_file_path)
                # self.csv_writer()
                self.queue.task_done()
                self.LOGGER.info(f"{self.parser.BASE_URL}{url} -" # {Source} {type} SUCCESS in {time}
                                 f" parsed successfully")
            except Exception as E:
                print(f'error{E}')
                # LOG SOMETHING

            if self.queue.empty():
                self.parser._DRIVER.close()

    # @staticmethod
    # def csv_writer(output_file_path: str, row: dict):
    #     with global_lock:
    #         with open(output_file_path, 'a', newline='') as csvfile:
    #             writer = csv.writer(csvfile, delimiter=';',
    #                                     quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #             writer.writerow(row.values())
