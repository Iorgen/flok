class date_parser():
    def isDate(self, str):
        if debug: print(str)
        try:
            datetime.datetime.strptime(str, '%d.%m.%Y')
            return True
        except ValueError:
            return False


class parser_3(date_parser):
    def parse(self, str):
        try:
            if debug: print(3)
            date = str.lower()
            date_format = '%d.%m.%Y'
            date = dateparser.parse(date).strftime(date_format)
            return date
        except:
            ...
        return False


class parser_2(date_parser):
    def parse(self, str):
        try:
            if debug: print(2)
            if ('Обн.' in str):
                date_format = '%d.%m.%Y'
                date = str.replace('Обн.', '')
                date = dateparser.parse(date).strftime(date_format)
                return date
            return False
        except:
            ...
        return False


class parser_1(date_parser):
    def parse(self, str):
        try:
            if debug: print(1)
            if ('Опубликовано' in str):
                if debug: print(1)
                date_format = '%d.%m.%Y'
                date = str.replace('Опубликовано', '')
                date = dateparser.parse(date).strftime(date_format)
                return date
            return False
        except:
            ...
        return False