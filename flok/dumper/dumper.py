import threading
import csv
import os
from flok.dumper.base import BaseCsvDumper


class CollectionCsvDumper(BaseCsvDumper):

    def _save_objects(self, dump_object):
        # TODO assertion and another type checking
        with open(self._file_path, 'a', newline='') as csvfile:
            for row in dump_object:
                writer = csv.writer(csvfile)
                writer.writerow([row])


class DictCsvDumper(BaseCsvDumper):

    def _save_objects(self, dump_object):

        with open(self._file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(dump_object.values())
