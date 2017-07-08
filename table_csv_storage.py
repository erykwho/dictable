import csv

from dict_table import DictTable


class TableCsvStorage(object):
    def __init__(self):
        pass

    @staticmethod
    def import_from_file_path(file_path, delimiter=';'):
        with open(file_path, 'r') as file:
            return _import_from_file(file, delimiter)

    @staticmethod
    def import_from_file(file, delimiter=';'):
        return _import_from_file(file, delimiter)

    @staticmethod
    def export(file_path, content, headers, delimiter=';'):
        with open(file_path, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=headers or content[0].keys(), delimiter=delimiter)
            writer.writeheader()
            writer.writerows(content)


def _import_from_file(file, delimiter=';'):
    reader = csv.DictReader(file, delimiter=delimiter)
    content = list()
    for row in reader:
        content.append(row)
    return DictTable(content)
