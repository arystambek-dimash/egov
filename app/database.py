import psycopg2

from app.config import config


class DBManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            params = config()
            self.connection = psycopg2.connect(**params)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(e)

    def execute_query(self, query):
        if self.connection is None or self.connection.closed:
            self.connect()

        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(e)
        finally:
            self.close()

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()


db_manager = DBManager()
