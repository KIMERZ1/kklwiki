from flask_login import UserMixin
import bcrypt

from app.extensions import get_db


class User(UserMixin):
    def __init__(self, id, username, password_hash, role="member", is_banned=False):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.is_banned = is_banned

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        return not self.is_banned

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode("utf-8"), self.password_hash.encode("utf-8"))

    def set_banned(self, is_banned):
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("UPDATE users SET is_banned = %s WHERE id = %s", (is_banned, self.id))
        conn.commit()
        self.is_banned = is_banned

    @staticmethod
    def _from_row(row):
        if row is None:
            return None
        return User(
            id=row["id"],
            username=row["username"],
            password_hash=row["password_hash"],
            role=row["role"],
            is_banned=bool(row["is_banned"]),
        )

    @staticmethod
    def get_by_id(user_id):
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            row = cursor.fetchone()
        return User._from_row(row)

    @staticmethod
    def get_by_username(username):
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            row = cursor.fetchone()
        return User._from_row(row)

    @staticmethod
    def list_all():
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users ORDER BY id")
            rows = cursor.fetchall()
        return [User._from_row(row) for row in rows]

    @staticmethod
    def create(username, raw_password):
        password_hash = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username, password_hash),
            )
            new_id = cursor.lastrowid
        conn.commit()
        return User.get_by_id(new_id)
