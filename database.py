import sqlite3

DB_NAME = 'example.db'
conn = sqlite3.connect(DB_NAME)

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS users
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        email TEXT UNIQUE,
        address TEXT,
        telephone_number INTEGER
    )
''')

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS posts
    (
        post_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        owner TEXT,
        price INTEGER,
        date_of_release TEXT,
        is_active BOOL,
        user_bought INTEGER,
        FOREIGN KEY(user_bought) REFERENCES users(user_id)
    )
''')


class DB:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
