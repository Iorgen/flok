import threading
global_lock = threading.Lock()
import csv


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
