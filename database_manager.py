import pyodbc
from patient import Patient

connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'


class DatabaseManager:
    def __init__(self, server, database, username, password):
        self.connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = pyodbc.connect(self.connection_string)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()