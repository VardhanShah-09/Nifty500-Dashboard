import sqlite3
import bcrypt
from datetime import datetime
from pathlib import Path

DB_NAME = Path(__file__).parent / "users.db"


def get_connection():
    """
    Create and return a connection to the SQLite database.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_users_table():
    """
    Create the users table if it does not already exist.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            full_name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            role TEXT NOT NULL DEFAULT 'USER',

            is_admin INTEGER NOT NULL DEFAULT 0,

            is_active INTEGER NOT NULL DEFAULT 1,

            created_at TEXT NOT NULL,

            last_login TEXT
        )
    """)

    conn.commit()
    conn.close()

    print("Users table created successfully!")


def create_default_admin():
    """
    Create the first administrator account if no users exist.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    if user_count == 0:

        username = "admin"
        full_name = "System Administrator"
        email = "admin@nifty500.com"
        password = "admin123"

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO users
            (
                username,
                full_name,
                email,
                password,
                role,
                is_admin,
                is_active,
                created_at,
                last_login
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username,
            full_name,
            email,
            hashed_password,
            "ADMIN",
            1,
            1,
            created_at,
            None
        ))

        conn.commit()

        print("Default admin created successfully!")

    else:
        print("Users already exist. Skipping admin creation.")

    conn.close()


if __name__ == "__main__":
    create_users_table()
    create_default_admin()
