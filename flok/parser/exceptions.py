class BaseParserException(Exception):
    default_message = 'Unknown parser exception'
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


class LoadPageException(BaseParserException):
    default_message = 'Load page Exception'


class ResolveCaptchaException(BaseParserException):
    default_message = 'Resolve captcha exception'


class RetrieveInformationFromPageException(BaseParserException):
    default_message = 'Retrieve information from page exception'


class NoParserByParamsException(BaseParserException):
    default_message = 'Non existing parser'
