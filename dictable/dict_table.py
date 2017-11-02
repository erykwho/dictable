import itertools
from collections import OrderedDict
from decimal import Decimal

from dictable.number_utils import parse_decimal, number_to_str
from dictable.dict_table_row import DicTableRow


class DicTable(list):
    """
        A TableManager object is an abstraction of a real Table.
        It is a list of dicts containing the same headers.
        
        Example:
            my_table = [
                {
                    'column_1': 1,
                    'column_2': 2,
                },
                {
                    'column_1': 3,
                    'column_2': 4,
                },
            ]

            my_table is the same as the table:

            | column_1 | column_2 |
            |----------|----------|
            |    1     |    2     |
            |    3     |    4     |

        """

    def __init__(self, table, sort=False):
        list.__init__(self, table)
        self.table = self._sort() if sort else table

    def _sort(self):
        self.table = self.sort(self.table)

    def sort_all(self, table):
        table = self.sort_by_keys(table)

        for column in set(table[0].keys()):
            table = self.sort(table, column)

        return table

    @staticmethod
    def sort_by_keys(table):
        for (index, row) in enumerate(table):
            table[index] = OrderedDict(sorted(row.items()))
        return table

    @staticmethod
    def sort(table, column=None, **kwargs):
        column = column or sorted(table[0].keys())[0]
        return sorted(table, key=lambda k: k[column])

    def match(self, table_to_match, columns_to_match=None, ordered=False):
        """
        Match self with table_to_match
        
        :param table_to_match: table object or a kind like table list to compare
        :param columns_to_match: (optional) a list containing columns to match 
        :param ordered: (optional) whether the tables are in the same order or not.
         If they are not ordered, this function will sort then
        :return: True if table contents are equal and False otherwise.
        """
        if len(self) != len(table_to_match):
            return False

        table = self.table
        if not ordered:
            table_to_match = self.sort_all(table_to_match)
            table = self.sort_all(self.table)

        return self._match(table, table_to_match, columns_to_match)

    @staticmethod
    def _match(table_1, table_2, columns_to_match):
        for i in range(len(table_2)):
            if not DicTableRow(table_1[i]).match(table_2[i], columns_to_match):
                return False
        return True

    def distinct_column(self, column):
        """
        Get the distinct values of a given column
        
        :param column: A column (dictionary key)
        :return: A list containing all distinct values from this table
        """
        distinct_values = list()
        for row in self.table:
            if row.get(column):
                distinct_values.append(row[column])
        return list(set(distinct_values))

    def distinct_columns(self, columns=None):
        """
        Get the distinct values form a list of columns
        
        :param columns: A list of columns. If None, all the columns of self will be considered.
        :return: A dictionary-list containing all distinct values for each column
        """

        if not columns:
            columns = self[0].keys()

        return {
            column: self.distinct_column(column) for column in columns
        }

    def summarize(self, group_by_options, columns_to_sum):

        group_by_columns = list(group_by_options.keys())
        summary_options = self.combinations(group_by_options)

        for row in self.table:
            for (index, summary_option) in enumerate(summary_options):
                if DicTableRow(row).match(summary_option, group_by_columns):
                    for element in columns_to_sum:
                        summary_options[index][element] = summary_options[index].get(element, 0) + parse_decimal(
                            row[element])
                    break

        return DicTable(summary_options)

    @staticmethod
    def combinations(combinations):
        """
        Create a table using combinatorial analysis. 
        
        :param combinations: Must be a dict where the value of each key is a list containing all the possible 
        combinations for the key.  
        :return: A Table where each row is a different combination
        """
        combination_table = DicTable(list())
        columns = list(combinations.keys())

        for combination in itertools.product(*(combinations[column] for column in columns)):
            combination_table.append(dict((column, combination[index]) for (index, column) in enumerate(columns)))

        return combination_table

    def merge(self, target, constraints, merge_columns, equivalence):
        for target_row in target:
            for table_row in self.table:
                if DicTableRow(table_row).match(target_row, constraints, equivalence):
                    for replace_column in merge_columns:
                        target_row.update({equivalence[replace_column]: number_to_str(table_row[replace_column])})
        return target

    def group_by(self, columns=None, count=False):
        distinct_columns = self.distinct_columns(columns)
        summary_options = self.combinations(distinct_columns)

        result = list()
        for summary_option in summary_options:
            matches = 0
            for row in self.table:
                if DicTableRow(row).match(row_to_match=summary_option, columns=distinct_columns.keys()):
                    matches += 1

            if matches:
                if count:
                    summary_option['count'] = matches
                result.append(summary_option)

        return result

    def sum(self, column):
        value = 0
        for row in self.table:
            value += Decimal(row[column])
        return value

    def columns(self, ordered=False):
        """
            Get dictable columns
        :param ordered: Boolean. If true, the returned
            will follow the ascendant order of the
            columns
        Returns: List containing columns of dictable
        """
        row = self.table[0]
        keys = row.keys()
        if ordered:
            keys = sorted(keys)

        return keys
