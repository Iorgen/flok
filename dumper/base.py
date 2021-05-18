import binascii
import csv
import logging
import os
import threading
from queue import Queue
from threading import Thread

from parser.base import BaseParser

global_lock = threading.Lock()


class DumpFabric:
    @staticmethod
    def get_dumper(_type: str):
        if _type == "collection":
            return CsvDumper.dump_collection_to_csv
        if _type == "page":
            return CsvDumper.dump_row_to_csv


class CsvDumper:
    """
    Dump methods library
    """
    # TODO unify dump function interface
    @staticmethod
    def dump_collection_to_csv(collection, output_file):
        with global_lock:
            with open(output_file, 'a', newline='') as csvfile:
                for row in collection:
                    writer = csv.writer(csvfile)
                    writer.writerow([row])

    @staticmethod
    def dump_row_to_csv(row, output_file):
        with global_lock:
            with open(output_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(row.values())


@staticmethod
def csv_writer(output_file_path: str, row: dict):
    with global_lock:
        with open(output_file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(row.values())


# TODO FABRIC for dumper functions with choosing storing way (NoSQL, SQL, File)
def write_links_to_file(links, filename):
    with global_lock:
        with open(filename, "a") as file:
            for link in links:
                file.write(str(link))
                # file.write(str(threading.get_ident()))
                file.write("\n")


def write_dict_information_into_csv(links, filename):
    # with open(filename, "a") as file:
    #     for key, value in links.items():
    #         file.write(f'{value};')
    #     file.write("\n")
    with global_lock:
        with open(filename, 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(links.values())
