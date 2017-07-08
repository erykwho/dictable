from decimal import Decimal


def parse_decimal(value):
    return Decimal(str(value).replace(',', '.'))


def number_to_str(value):
    return str(value).replace('.', ',')
