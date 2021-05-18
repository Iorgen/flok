import csv
from config.config import Config


class TransportCharterCollectionLinksCreator:
    def create_links(self):
        return [
            f"uchastniki?page={i}&dp-1-per-page=50"
            for i in range(1, 70)
        ]


class TransportCharterDetailLinksCreator:
    def create_links(self):
        with open('data/charter/charter_collection_result.csv', 'r') as file:
            pages_urls = file.readlines()
        pages_urls = [x.strip() for x in pages_urls]
        return pages_urls


class FindOrgCollectionLinksCreator:
    def create_links(self):
        return []


class FindOrgPagesLinksCreator:
    def create_links(self):
        with open('find_org_collection_links', 'r') as file:
            pages_urls = file.readlines()
        pages_urls = [x.strip() for x in pages_urls]


class KAgentPagesLinksCreator:
    def create_links(self):
        cfg = Config()
        links = []

        with open('data/legal_entities.csv', 'rU') as infile:
            # read the file as a dictionary for each row ({header : value})
            reader = csv.DictReader(infile, delimiter=';')
            data = {}
            for row in reader:
                for header, value in row.items():
                    try:
                        data[header].append(value)
                    except KeyError:
                        data[header] = [value]

        for _i in range(len(data['inn'])):
            links.append(f"{data['inn'][_i]}-{data['ogrn'][_i]}")
