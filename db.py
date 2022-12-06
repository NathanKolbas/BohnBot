import sqlite3


class DB:
    def __init__(self):
        self.conn = None
        self.cursor = None

        # Create database
        self.create_table()

    def close(self):
        self.conn.close()

    def create_table(self):
        self.conn = sqlite3.connect('bohnbot.db')
        self.cursor = self.conn.cursor()
        self.cursor.executescript('''
        CREATE TABLE IF NOT EXISTS Quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        quote TEXT NOT NULL,
        created_by INT,
        FOREIGN KEY(created_by) REFERENCES Users(id));

        CREATE TABLE IF NOT EXISTS Users (
        id INT PRIMARY KEY NOT NULL UNIQUE);
        ''')
        self.conn.commit()

    def drop_table(self):
        self.cursor.executescript('''
        DROP TABLE IF EXISTS Quotes;
        DROP TABLE IF EXISTS Users;
        ''')
        self.conn.commit()
        self.close()

    def import_file(self):
        QUOTES_FILE = 'quotes.txt'
        with open(QUOTES_FILE, 'r', encoding="utf8") as f:
            quotes = [x.strip() for x in f.readlines()]

        for i, quote in enumerate(quotes):
            self.cursor.execute("INSERT INTO Quotes(quote) VALUES(?)", [quote])
        self.conn.commit()

    def get_quotes(self):
        res = self.cursor.execute("SELECT * FROM Quotes")
        return res.fetchall()

    def get_quote(self, quote_id):
        res = self.cursor.execute("SELECT * FROM Quotes where id = ?", [quote_id])
        return res.fetchone()

    def insert_quote(self, quote):
        self.cursor.execute("INSERT INTO Quotes(quote) VALUES(?)", [quote])
        self.conn.commit()
        return self.cursor.lastrowid

    def delete_quote(self, quote_id):
        self.cursor.execute("DELETE from Quotes where id = ?", [quote_id])
        self.conn.commit()
        return self.cursor.lastrowid
