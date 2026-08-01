from flask_login import UserMixin
from db import db

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def get(user_id):
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                return None
            return User(id=user[0], username=user[1], password=user[2])
        except Exception as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def find_by_username(username):
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if not user:
                return None
            return User(id=user[0], username=user[1], password=user[2])
        except Exception as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def add_user(username, password):
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id", (username, password))
            user_id = cursor.fetchone()[0]
            conn.commit()
            return User(id=user_id, username=username, password=password)
        except Exception as e:
            print(f"Database error: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()