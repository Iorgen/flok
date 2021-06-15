class BaseManagerException(Exception):
    default_message = 'Unknown manager exception'
    message = None

    def __str__(self):
        return f'' \
               f'{self.message if self.message is not None else self.default_message } - ' \
               f'{self.service_code}'

    def __init__(
            self,
            message: str = None,
            service_code: str = None,
            source: str = None,
    ):
        self.service_code = service_code
        self.message = message
        self.source = source
        super().__init__(self)

class NothingToParseException(Exception):
    default_message = 'empty parsing array'

class WrongParserException(Exception):
    default_message = 'empty parsing array'