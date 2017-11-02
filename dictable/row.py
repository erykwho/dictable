class DicTableRow(dict):
    def __init__(self, row):
        dict.__init__(self, row)
        self.row = row

    def match(self, row_to_match, columns=None, equivalence=None):
        """
        This method will compare the rows. You can choose which columns to match.     
        This method supports equivalence matching (keyA of self.row -> keyB of row_to_match).
            
        :param row_to_match: Target row to match with self.row
        :param columns: A list containing the columns to be matched. If Not specified, it will match all the columns.
        :param equivalence: A list containing the equivalence between columns if there is one.
        :return: True if rows match, else otherwise.
        """
        columns = columns or list(self.row.keys())

        for column in columns:
            if self.row.get(column) != (row_to_match.get(equivalence[column]) if equivalence
                                        else row_to_match.get(column)):
                return False

        return True
