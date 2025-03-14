# database.py
import sqlite3

class Database:
    def __init__(self, db_url):
        self.connection = sqlite3.connect(db_url)
        self.cursor = self.connection.cursor()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

# Создаем глобальный объект подключения
db = Database("example.db")