from database import DB
from user import User


class Post:
    def __init__(self, post_id, title, description, owner, price, date_of_release, is_active, user_bought):
        self.post_id = post_id
        self.title = title
        self.description = description
        self.owner = owner
        self.price = price
        self.date_of_release = date_of_release
        self.is_active = is_active
        self.user_bought = user_bought

    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM posts').fetchall()
            return [Post(*row) for row in rows]

    @staticmethod
    def find(post_id):
        with DB() as db:
            row = db.execute(
                'SELECT * FROM posts WHERE id = ?',
                (post_id,)
            ).fetchone()
            return Post(*row)

    def create(self):
        with DB() as db:
            values = (
                self.post_id, self.title, self.description, self.owner, self.price, self.date_of_release, True, None)
            db.execute('''
                INSERT INTO posts (post_id, title, description, owner, price, date_of_release, is_active, user_bought)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', values)
            return self

    def save(self):
        with DB() as db:
            values = (
                self.post_id,
                self.title,
                self.description,
                self.owner,
                self.price,
                self.date_of_release,
                self.is_active,
                self.user_bought
            )
            db.execute(
                '''UPDATE posts
                SET post_id = ?, title = ?, description = ?, owner = ?, price = ?, date_of_release = ?, is_active = ?, user_bought = ?
                WHERE post_id = ?''', values)
            return self

    def update(self):
        with DB() as db:
            values = (self.title, self.description, self.price)
            db.execute('''
                UPDATE INTO posts (title, description, price)
                VALUES (?, ?, ?)''', values)
            return self

    def buy(self):
        with DB() as db:
            buy_user = User
            values = (self.is_active, self.user_bought)
            db.execute('''
                SET is_active = False, user_bought = buy_user 
                WHERE post_id = ?''', values, buy_user)
        return self

    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM posts WHERE post_id = ?', (self.post_id,))
