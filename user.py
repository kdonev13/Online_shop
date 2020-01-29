import hashlib

from database import DB


class User:
    def __init__(self, id, username, password, email, address, telephone_number):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.address = address
        self.telephone_number = telephone_number
        self.values = (self.id, self.username, self.password, self.email, self.address, self.telephone_number)

    def add_user(self):
        with DB() as db:
            db.execute('''
                INSERT INTO users (id, username, password, email, address, telephone_number)
                VALUES (?, ?, ?, ?, ?, ?)''', self.values)
            return self

    @staticmethod
    def find_by_email(email):
        if not email:
            return None
        with DB() as db:
            row = db.execute(
                'SELECT * FROM users WHERE username = ?',
                (email,)
            ).fetchone()
            if row:
                return User(*row)

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()