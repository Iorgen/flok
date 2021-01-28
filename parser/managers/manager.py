from queue import Queue
from parser.managers.parser import Parser
from parser.parser.fabric import ChromeDriverParserFabric


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
        CDF = ChromeDriverParserFabric()
        for i in range(self.thread_count):
            # parser = CDF.get_parser(
            #     _source=_source,
            #     _type=_type,
            #     _driver_path='drivers/chromedriver'
            # )
            # self.PARSERS.append(parser)

            t = Parser(
                queue=queue,
                output_file_path=self.output_file_path,
                parser=CDF.get_parser(
                    _source=_source,
                    _type=_type,
                    _driver_path='drivers/chromedriver'
                )
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
