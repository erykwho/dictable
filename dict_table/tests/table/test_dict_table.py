import unittest
from decimal import Decimal

from dict_table import DictTable


class TestTable(unittest.TestCase):
    def setUp(self):
        self.table_1 = [
            {
                'colA': 1,
                'colB': 1
            },
            {
                'colA': 2,
                'colB': 4
            }
        ]

        self.table_2 = [
            {
                'colA': 1,
                'colB': 1
            },
            {
                'colA': 2,
                'colB': 4
            }
        ]

        self.table_3 = [
            {
                'colA': 2,
                'colB': 4
            },
            {
                'colA': 1,
                'colB': 1
            }
        ]

        self.table_4 = [
            {
                'colA': 1,
                'colB': 1,
                'colC': 5
            },
            {
                'colA': 2,
                'colB': 4,
                'colC': 5
            }
        ]
        self.columns_to_match = ['colA', 'colB']

    def tearDown(self):
        pass

    def test_table_must_be_table(self):
        actual = DictTable(self.table_1)
        expected = self.table_1
        self.assertEqual(expected, actual)

    def test_table_must_be_different_than_other_table(self):
        self.assertNotEqual(DictTable(self.table_1), DictTable(self.table_4))

    def test_table_match_another_table(self):
        table_1 = DictTable(self.table_1)
        self.assertTrue(table_1.match(self.table_2))

    def test_table_match_a_list_like_table(self):
        table_1 = DictTable(self.table_1)
        self.assertTrue(table_1.match(self.table_2))

    def test_table_match_another_table_with_unordered_rows(self):
        table_1 = DictTable(self.table_1)
        self.assertTrue(table_1.match(self.table_3, ordered=False))

    def test_table_should_not_match_another_table_with_unordered_rows_with_ordered_param_true(self):
        table_1 = DictTable(self.table_1)
        self.assertFalse(table_1.match(self.table_3, ordered=True))

    def test_table_does_not_match_another_table(self):
        table_1 = DictTable(self.table_1)
        self.assertTrue(table_1.match(self.table_4))

    def test_table_match_another_table_with_specific_columns(self):
        table_1 = DictTable(self.table_1)
        self.assertTrue(table_1.match(self.table_2, columns_to_match=self.columns_to_match))

    def test_table_distinct(self):
        table_1 = DictTable(self.table_1)
        actual = table_1.get_distinct_column('colA')
        expected = [1, 2]
        self.assertEqual(expected, actual)

    def test_table_distinct_columns(self):
        table_4 = DictTable(self.table_4)
        actual = table_4.get_distinct_columns(['colA', 'colC'])
        expected = {'colA': [1, 2], 'colC': [5]}
        self.assertEqual(expected, actual)

    def test_get_summary_value_from_table(self):
        group_by_options = {
            'colA': [1, 2],
            'colB': [1, 2]
        }
        columns_to_sum = ['value_column']

        table = DictTable([
            {'colA': 1, 'colB': 1, 'value_column': 1},
            {'colA': 2, 'colB': 1, 'value_column': 7},
            {'colA': 1, 'colB': 2, 'value_column': 10},
            {'colA': 2, 'colB': 2, 'value_column': 5},
            {'colA': 1, 'colB': 1, 'value_column': 4},
            {'colA': 1, 'colB': 2, 'value_column': 20},
        ])
        expected = [
            {'colA': 1, 'colB': 1, 'value_column': Decimal(5)},
            {'colA': 2, 'colB': 1, 'value_column': Decimal(7)},
            {'colA': 1, 'colB': 2, 'value_column': Decimal(30)},
            {'colA': 2, 'colB': 2, 'value_column': Decimal(5)},
        ]

        actual = table.summarize(group_by_options=group_by_options, columns_to_sum=columns_to_sum)

        self.assertEqual(DictTable.sort(expected, 'colA'), DictTable.sort(actual, 'colA'))

    def test_merge_tables(self):
        table_1 = DictTable([
            {'colA': 1, 'colB': 1, 'value_column': 21},
            {'colA': 2, 'colB': 1, 'value_column': 45},
            {'colA': 3, 'colB': 2, 'value_column': 76},
            {'colA': 5, 'colB': 3, 'value_column': 91},
        ])

        table_2 = DictTable([
            {'colA': 1, 'colB': 1, 'value_column': 1},
            {'colA': 2, 'colB': 1, 'value_column': 2},
            {'colA': 3, 'colB': 2, 'value_column': 3},
            {'colA': 5, 'colB': 3, 'value_column': 4},
            {'colA': 1, 'colB': 2, 'value_column': 6},
            {'colA': 2, 'colB': 9, 'value_column': 7},
        ])

        expected = DictTable([
            {'colA': 1, 'colB': 1, 'value_column': '1'},
            {'colA': 2, 'colB': 1, 'value_column': '2'},
            {'colA': 3, 'colB': 2, 'value_column': '3'},
            {'colA': 5, 'colB': 3, 'value_column': '4'},
        ])
        constraints = ['colA', 'colB']
        merge_columns = ['value_column']
        equivalence = {
            'colA': 'colA',
            'colB': 'colB',
            'value_column': 'value_column',
        }
        actual = table_2.merge(target=table_1, constraints=constraints, merge_columns=merge_columns,
                               equivalence=equivalence)

        self.assertEqual(expected, actual)

    def test_merge_tables_with_column_equivalence(self):
        table_1 = DictTable([
            {'colC': 1, 'colD': 1, 'value_column': 21},
            {'colC': 2, 'colD': 1, 'value_column': 45},
            {'colC': 3, 'colD': 2, 'value_column': 76},
            {'colC': 5, 'colD': 3, 'value_column': 91},
        ])

        table_2 = DictTable([
            {'colA': 1, 'colB': 1, 'value_column': 1},
            {'colA': 2, 'colB': 1, 'value_column': 2},
            {'colA': 3, 'colB': 2, 'value_column': 3},
            {'colA': 5, 'colB': 3, 'value_column': 4},
            {'colA': 1, 'colB': 2, 'value_column': 6},
            {'colA': 2, 'colB': 9, 'value_column': 7},
        ])

        expected = DictTable([
            {'colC': 1, 'colD': 1, 'value_column': '1'},
            {'colC': 2, 'colD': 1, 'value_column': '2'},
            {'colC': 3, 'colD': 2, 'value_column': '3'},
            {'colC': 5, 'colD': 3, 'value_column': '4'},
        ])
        constraints = ['colA', 'colB']
        merge_columns = ['value_column']
        equivalence = {
            'colA': 'colC',
            'colB': 'colD',
            'value_column': 'value_column',
        }
        actual = table_2.merge(target=table_1, constraints=constraints, merge_columns=merge_columns,
                               equivalence=equivalence)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
