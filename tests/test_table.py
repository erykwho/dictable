import unittest
from decimal import Decimal

from dictable.dict_table import DicTable


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
        actual = DicTable(self.table_1)
        expected = self.table_1
        self.assertEqual(expected, actual)

    def test_table_must_be_different_than_other_table(self):
        self.assertNotEqual(DicTable(self.table_1), DicTable(self.table_4))

    def test_table_match_another_table(self):
        table_1 = DicTable(self.table_1)
        self.assertTrue(table_1.match(self.table_2))

    def test_table_match_a_list_like_table(self):
        table_1 = DicTable(self.table_1)
        self.assertTrue(table_1.match(self.table_2))

    def test_table_match_another_table_with_unordered_rows(self):
        table_1 = DicTable(self.table_1)
        self.assertTrue(table_1.match(self.table_3, ordered=False))

    def test_table_should_not_match_another_table_with_unordered_rows_with_ordered_param_true(self):
        table_1 = DicTable(self.table_1)
        self.assertFalse(table_1.match(self.table_3, ordered=True))

    def test_table_does_not_match_another_table(self):
        table_1 = DicTable(self.table_1)
        self.assertTrue(table_1.match(self.table_4))

    def test_table_match_another_table_with_specific_columns(self):
        table_1 = DicTable(self.table_1)
        self.assertTrue(table_1.match(self.table_2, columns_to_match=self.columns_to_match))

    def test_table_distinct(self):
        table_1 = DicTable(self.table_1)
        actual = table_1.distinct_column('colA')
        expected = [1, 2]
        self.assertEqual(expected, actual)

    def test_table_distinct_columns(self):
        table_4 = DicTable(self.table_4)
        actual = table_4.distinct_columns(['colA', 'colC'])
        expected = {'colA': [1, 2], 'colC': [5]}
        self.assertEqual(expected, actual)

    def test_get_summary_value_from_table(self):
        group_by_options = {
            'colA': [1, 2],
            'colB': [1, 2]
        }
        columns_to_sum = ['value_column']

        table = DicTable([
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

        self.assertEqual(DicTable.sort(expected, 'colA'), DicTable.sort(actual, 'colA'))

    def test_merge_tables(self):
        table_1 = DicTable([
            {'colA': 1, 'colB': 1, 'value_column': 21},
            {'colA': 2, 'colB': 1, 'value_column': 45},
            {'colA': 3, 'colB': 2, 'value_column': 76},
            {'colA': 5, 'colB': 3, 'value_column': 91},
        ])

        table_2 = DicTable([
            {'colA': 1, 'colB': 1, 'value_column': 1},
            {'colA': 2, 'colB': 1, 'value_column': 2},
            {'colA': 3, 'colB': 2, 'value_column': 3},
            {'colA': 5, 'colB': 3, 'value_column': 4},
            {'colA': 1, 'colB': 2, 'value_column': 6},
            {'colA': 2, 'colB': 9, 'value_column': 7},
        ])

        expected = DicTable([
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
        table_1 = DicTable([
            {'colC': 1, 'colD': 1, 'value_column': 21},
            {'colC': 2, 'colD': 1, 'value_column': 45},
            {'colC': 3, 'colD': 2, 'value_column': 76},
            {'colC': 5, 'colD': 3, 'value_column': 91},
        ])

        table_2 = DicTable([
            {'colA': 1, 'colB': 1, 'value_column': 1},
            {'colA': 2, 'colB': 1, 'value_column': 2},
            {'colA': 3, 'colB': 2, 'value_column': 3},
            {'colA': 5, 'colB': 3, 'value_column': 4},
            {'colA': 1, 'colB': 2, 'value_column': 6},
            {'colA': 2, 'colB': 9, 'value_column': 7},
        ])

        expected = DicTable([
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


class TestGroupBy(unittest.TestCase):
    def setUp(self):
        self.table = DicTable([
            {'A': 1, 'B': 'foo'},
            {'A': 2, 'B': 'bar'},
            {'A': 3, 'B': 'bar'},
            {'A': 1, 'B': 'bar'},
            {'A': 2, 'B': 'bar'},
            {'A': 3, 'B': 'bar'},
            {'A': 1, 'B': 'foo'},
        ])

        self.table_1 = DicTable([
            {'A': 1, 'B': 'foo'},
            {'A': 2, 'B': 'bar'},
            {'A': 3, 'B': 'wat'},
            {'A': 1, 'B': 'wat'},
            {'A': 2, 'B': 'bar'},
            {'A': 3, 'B': 'bar'},
            {'A': 1, 'B': 'foo'},
        ])

    def tearDown(self):
        pass

    def test_group_by_without_passing_arguments(self):
        expected = DicTable([
            {'A': 1, 'B': 'foo'},
            {'A': 1, 'B': 'bar'},
            {'A': 2, 'B': 'bar'},
            {'A': 3, 'B': 'bar'},
        ])
        actual = self.table.group_by()
        self.assertTrue(expected.match(actual))

    def test_group_by_without_passing_arguments_2(self):
        expected = DicTable([
            {'A': 1, 'B': 'foo'},
            {'A': 3, 'B': 'wat'},
            {'A': 2, 'B': 'bar'},
            {'A': 1, 'B': 'wat'},
            {'A': 3, 'B': 'bar'},
        ])
        actual = self.table_1.group_by()
        self.assertTrue(expected.match(actual))

    def test_group_by_passing_group_by_columns(self):
        expected = DicTable([
            {'A': 1, 'B': 'foo'},
            {'A': 1, 'B': 'bar'},
            {'A': 2, 'B': 'bar'},
            {'A': 3, 'B': 'bar'},
        ])
        actual = self.table.group_by(['A', 'B'])
        self.assertTrue(expected.match(actual))

    def test_group_by_count(self):
        expected = DicTable([
            {'A': 1, 'B': 'foo', 'count': 2},
            {'A': 1, 'B': 'bar', 'count': 1},
            {'A': 2, 'B': 'bar', 'count': 2},
            {'A': 3, 'B': 'bar', 'count': 2},
        ])

        actual = self.table.group_by(count=True)
        self.assertTrue(expected.match(actual))


class TestSum(unittest.TestCase):
    def setUp(self):
        self.table = [
            {'a': 1, 'b': '2.50', 'c': 1},
            {'a': 2, 'b': '3.5', 'c': 'a'},
            {'a': 5, 'b': '7.5', 'c': 10},
        ]

    def tearDown(self):
        pass

    def test_sum_column_type_number(self):
        expected = 1 + 2 + 5
        actual = DicTable(self.table).sum('a')
        self.assertEqual(expected, actual)

    def test_sum_column_type_not_number_but_number(self):
        expected = 2.5 + 3.5 + 7.5
        actual = DicTable(self.table).sum('b')
        self.assertEqual(expected, actual)

    def test_sum_column_type_not_number_should_raise_exception(self):
        with self.assertRaises(Exception):
            DicTable(self.table).sum('c')


if __name__ == '__main__':
    unittest.main()
