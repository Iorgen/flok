import threading


class BaseDumper:

    def __init__(self, global_lock: bool = False):
        self._global_lock = global_lock

    def _save_objects(self, dump_object):
        raise NotImplementedError

    def dump(
            self,
            dump_object,
            *args,
            **kwargs
    ):
        # TODO rebuild is possible - incoming empty object
        raise NotImplementedError()


class BaseDbDumper(BaseDumper):
    pass


class BaseCsvDumper(BaseDumper):

    def __init__(
            self,
            file_path: str = 'data/parsed_data.csv',
            delimiter: str = ';',
            **kwargs
    ):
        super().__init__(**kwargs)
        self._file_path = file_path

    def init_file_name(self, addition):
        self._file_path = f"{self._file_path}_{addition}"
        if os.path.exists(self._file_path):
            pass
        else:
            # TODO create file
            raise Exception('No file, create pls')

    def dump(
            self,
            dump_object,
            *args,
            **kwargs
    ):
        if self._global_lock:
            global_lock = threading.Lock()
            with global_lock:
                self._save_objects(dump_object=dump_object)
        else:
            self._save_objects(dump_object=dump_object)
