from databricks import sql

class Connection():
    def __init__(self, SERVER_HOSTNAME, HTTP_PATH, ACCESS_TOKEN):
        self.SERVER_HOSTNAME = SERVER_HOSTNAME
        self.HTTP_PATH = HTTP_PATH
        self.ACCESS_TOKEN = ACCESS_TOKEN
        
    def make_query(self, query):
        connection = sql.connect(
            server_hostname=self.SERVER_HOSTNAME, http_path=self.HTTP_PATH, access_token=self.ACCESS_TOKEN
        )

        cursor = connection.cursor()
        cursor.execute(query)

        df = cursor.fetchall_arrow()

        cursor.close()
        connection.close()

        return df
