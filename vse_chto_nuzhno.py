import sqlite3


class Shaverma:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_all_in_this_level(self, level):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `shaverma` WHERE `zvezda` = ?", (level,)).fetchall()

    def get_by_name(self, name):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `shaverma` WHERE `name` = ?", (name,)).fetchall()
