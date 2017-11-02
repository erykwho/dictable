from dictable.query_deliverer import QueryDeliverer
from dictable.dict_table import DicTable


class DicTSQL(DicTable):
    def __init__(self, table):
        super().__init__(table)

    def create_table_syntax(self, table_name, column_order=None):
        """
            Generates a create table tsql statement
            for self.table
        Args:
            table_name: the name of the table to be created
            column_order: the order of columns

        Returns: String containing the static script to create table
            The generated query will have the provided column order
            and will follow the order of the rows of the dictable
        """
        template = QueryDeliverer().tsql_create_table
        select_statement = self.select_query_syntax(column_order)
        return template.format(table_name=table_name, select_statement=select_statement)

    def select_query_syntax(self, column_order=None):
        if not column_order:
            column_order = self.columns(ordered=True)

        row_queries = []
        for row in self.table:
            row_columns = ', '.join(
                '{} AS {}'.format(self._parse_type(row[column]), column)
                for column in column_order)
            row_queries.append('SELECT {}'.format(row_columns))

        return self._union_queries(row_queries)

    @staticmethod
    def _parse_type(variable):
        """
        Args:
            variable: variable

        Returns:
            The variable with the correct syntax for TSQL

        """
        if isinstance(variable, str):
            return '\"{}\"'.format(variable)

        return str(variable)

    @staticmethod
    def _union_queries(queries):
        """
            UNION-ALL-lize a list of static
        """
        return ' UNION ALL\n'.join(queries)
