from parser.collection.find_org import

class MyParser(Parser):
    def parse(self, source_, type_, obj_):
        if type_ == "page":
            if source_ == 'avito.ru':
                return AvitoParser(obj_)
            elif source_ == 'youla.ru':
                return YoulaParser(obj_)
            elif source_ == 'n1.ru':
                return N1Parser(obj_)
            elif source_ == 'cian.ru':
                return CianParser(obj_)
        elif type_ == "collection":
            if source_ == 'avito.ru':
                return AvitoCollection(obj_)
            elif source_ == 'youla.ru':
                return YoulaCollection(obj_)
            elif source_ == 'n1.ru':
                return N1Collection(obj_)
            elif source_ == 'cian.ru':
                return CianCollection(obj_)
