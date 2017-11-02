from dictable.query_deliverer import QueryDeliverer
from tests.dictsql_test_case import DicTSQLTestCase
from dictable.dict_tsql import DicTSQL


class TestTableToSql(DicTSQLTestCase):
    def setUp(self):
        table = [
            {'B': '2.50', 'A': 1, 'C': 'foo'},
            {'B': '3.5', 'A': 2, 'C': 'bar'},
            {'B': '7.5', 'A': 5, 'C': 'pip'},
        ]
        self.dictable = DicTSQL(table)
        self.skeleton_query = QueryDeliverer().tsql_create_table
        self.table_name = 'fooTable'

        self.select_query = '''\
        SELECT 1 AS A, "2.50" AS B, "foo" AS C UNION ALL
        SELECT 2 AS A, "3.5" AS B, "bar" AS C UNION ALL
        SELECT 5 AS A, "7.5" AS B, "pip" AS C\
        '''

    def test_tsql_create_table(self):
        expected_query = self.skeleton_query.format(table_name=self.table_name,
                                                    select_statement=self.select_query)

        actual_query = self.dictable.create_table_syntax(table_name=self.table_name, column_order=['A', 'B', 'C'])

        self.assertEqualQueries(expected_query, actual_query)

    def test_tsql_create_table_no_column_order(self):
        """
            Asserts returned query from parse_to_tsql
            when no column_order argument is passed.
            The order of columns in returned query must
            be in the alphabetical order of keys of the DicTable.
        """
        expected_query = self.skeleton_query.format(table_name=self.table_name,
                                                    select_statement=self.select_query)

        actual_query = self.dictable.create_table_syntax(table_name=self.table_name)

        self.assertEqualQueries(expected_query, actual_query)

    def test_tsql_select(self):
        """
            Asserts returned select query
            It should be in the format of
            '''
                SELECT 1 AS A UNION ALL
                SELECT 2 AS A UNION ALL
                SELECT 3 AS A
            '''

        """
        expected_query = self.select_query
        actual_query = self.dictable.select_query_syntax()
        self.assertEqualQueries(expected_query, actual_query)
