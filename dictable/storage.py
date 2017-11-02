from dictable.dict_table import DicTable


class TableCsvStorage(object):
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
            writer = storage.DictWriter(file, fieldnames=headers or content[0].keys(), delimiter=delimiter)
            writer.writeheader()
            writer.writerows(content)


def _import_from_file(file, delimiter=';'):
    reader = storage.DictReader(file, delimiter=delimiter)
    content = list()
    for row in reader:
        content.append(row)
    return DicTable(content)
