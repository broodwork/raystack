import sqlite3


class Database:
    def __init__(self):
        self.db_url = "db.sqlite3"

    def connect(self):
        """Creates new database connection."""
        return sqlite3.connect(self.db_url)
    
    def execute(self, query, params=None, fetch=False):
        """
        Executes SQL query and returns result (if required).
        :param query: SQL query to execute.
        :param params: Parameters to substitute in query.
        :param fetch: If True, returns query results.
        :return: Cursor or query results.
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            if fetch:
                return cursor.fetchall()
            return cursor  # Return cursor for accessing attributes

    def commit(self):
        """Commits changes to database."""
        with self.connect() as conn:
            conn.commit()


# Create Database instance
db = Database()