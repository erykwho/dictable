import unittest

from dictable.dict_table_row import DicTableRow


class TestTableRow(unittest.TestCase):
    def setUp(self):
        self.row_1 = DicTableRow({'a': 2, 'b': 3, 'c': 4})
        self.row_2 = DicTableRow({'a': 2, 'b': 3, 'c': 4})
        self.row_3 = DicTableRow({'aa': 2, 'ba': 3, 'ca': 4})
        self.row_4 = DicTableRow({'a': 1, 'b': 3, 'c': 4})
        self.row_5 = DicTableRow({'a': 2, 'b': 3, 'c': 4, 'd': 5})

    def tearDown(self):
        pass

    def test_rows_should_match(self):
        self.assertTrue(self.row_1.match(self.row_2))

    def test_rows_should_not_match(self):
        self.assertFalse(self.row_1.match(self.row_4))

    def test_rows_should_match_with_specific_columns(self):
        self.assertTrue(self.row_5.match(self.row_1, columns=['a', 'b', 'c']))

    def test_rows_should_not_match_with_specific_columns(self):
        self.assertFalse(self.row_5.match(self.row_1, columns=['a', 'b', 'd']))

    def test_rows_should_match_with_equivalence(self):
        self.assertTrue(self.row_1.match(self.row_3, columns=['a', 'b', 'c'],
                                         equivalence={
                                             'a': 'aa',
                                             'b': 'ba',
                                             'c': 'ca'
                                         }))


if __name__ == '__main__':
    unittest.main()
