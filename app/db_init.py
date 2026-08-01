from db import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def init_db():
    conn = db.get_connection()
    cursor = conn.cursor()

    try:
        # Create users table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(150) UNIQUE NOT NULL,
                password VARCHAR(150) NOT NULL
            )
        """)

        # Check if the 'admin' user exists, otherwise create it
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        user = cursor.fetchone()
        if not user:
            # We use a default password 'password' for testing purposes, but it's hashed
            hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                ('admin', hashed_password)
            )
            print("Default user 'admin' created with password 'password'.")

    except Exception as e:
        print(f"Database error during initialization: {e}")
    finally:
        conn.commit()
        conn.close()

if __name__ == '__main__':
    init_db()
