import os


class QueryDeliverer:
    TSQL_CREATE_TABLE = 'TSQL_CREATE_TABLE'
    QUERY_FOLDER = 'queries'

    def get_query(self, query_name):
        with open(self.query_path(query_name)) as f:
            query = f.read()
        return query

    @property
    def tsql_create_table(self):
        return self.get_query(self.TSQL_CREATE_TABLE)

    def query_path(self, query_name):
        path = os.path.dirname(os.path.realpath(__file__))
        query_path = os.path.join(path, self.QUERY_FOLDER, query_name + ".sql")
        return query_path
