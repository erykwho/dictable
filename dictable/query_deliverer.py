import os


class QueryDeliverer:
    TSQL_CREATE_TABLE = 'TSQL_CREATE_TABLE'
    TSQL_QUERY_FOLDER = 'TSQL'
    QUERY_FOLDER = 'static/sql_templates'

    def get_query(self, query_name, folder=None):
        with open(self.query_path(query_name, folder)) as f:
            query = f.read()
        return query

    @property
    def tsql_create_table(self):
        return self.get_query(self.TSQL_CREATE_TABLE, self.TSQL_QUERY_FOLDER)

    def query_path(self, query_name, folder):
        query_folder = self.QUERY_FOLDER
        if folder:
            query_folder = os.path.join(query_folder, folder)

        path = os.path.dirname(os.path.realpath(__file__))
        query_path = os.path.join(path, query_folder, query_name + ".sql")
        return query_path
