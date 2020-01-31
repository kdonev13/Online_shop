from database import DB
from user import User
from datetime import date


class Post:
    def __init__(self, post_id, title, description, price, owner, date=date.today(), is_active=True, user_bought=0):
        self.post_id = post_id
        self.title = title
        self.description = description
        self.price = price
        self.owner = owner
        self.date = date
        self.is_active = is_active
        self.user_bought = user_bought

        self.values = (
            self.post_id, self.title, self.description, self.price, self.owner, self.date, self.is_active,
            self.user_bought)

        self.edit_values = (self.title, self.description, self.price, self.post_id)

    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM posts').fetchall()
            return [Post(*row) for row in rows]

    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute(
                'SELECT * FROM posts WHERE post_id = ?',
                (id,)
            ).fetchone()
            return Post(*row)

    def create(self):
        with DB() as db:
            db.execute('''
                INSERT INTO posts (post_id, title, description, price, owner, date, is_active, user_bought)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', self.values)
            return self

    @staticmethod
    def find_owner(owner):
        with DB() as db:
            username = db.execute(
                '''
                SELECT username FROM users 
                WHERE id = ?
                ''',
                (owner,)).fetchone()
        return username[0]

    @staticmethod
    def find_buyer(buyer):
        with DB() as db:
            user = db.execute(
                '''
                SELECT * FROM users
                WHERE id = ?
                ''', (buyer,)).fetchone()
            return user

    def update_bought_post(self):
        with DB() as db:
            buyer = (
                self.post_id,
                self.user_bought
            )
            db.execute('''
                        UPDATE posts SET user_bought = ?, is_active = False
                         WHERE post_id = ?''', buyer)
            return self

    def edit(self):
        with DB() as db:
            db.execute('''
            UPDATE posts SET title = ?, description = ?, price = ?
             WHERE post_id = ?''', self.edit_values)
            return self

    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM posts WHERE post_id = ?', (self.post_id,))
