import hashlib

from database import DB


class User:
    def __init__(self, user_id, email, username, password, address, telephone_number):
        self.user_id = user_id
        self.email = email
        self.username = username
        self.password = password
        self.address = address
        self.telephone_number = telephone_number

    def add_user(self):
        with DB() as db:
            values = (self.user_id, self.email, self.username, self.password, self.address, self.telephone_number)
            db.execute('''
                INSERT INTO users (user_id, email, username, password, address, telephone_number)
                VALUES (?, ?, ?, ?, ?, ?)''', values)
            return self

    @staticmethod
    def find_by_user_id(user_id):
        if not user_id:
            return None
        with DB() as db:
            row = db.execute(
                'SELECT * FROM users WHERE user_id = ?',
                (user_id,)
            ).fetchone()
            if row:
                return User(*row)

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()