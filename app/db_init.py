import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = "./data/eneverre.db"


def init_db():
    os.makedirs("./data", exist_ok=True)

    first_time = not os.path.exists(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Init table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            fullname TEXT,
            role TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS device_login (
            device_code TEXT PRIMARY KEY,
            user_code TEXT,
            status TEXT,
            username TEXT,
            expires_at INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            token TEXT PRIMARY KEY,
            username TEXT,
            expires_at INTEGER
        )
    """)

    # Init users if needed
    count = cur.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    if count == 0:
        username = os.getenv("ENEVERRE_ADMIN_USER", "admin").lower()
        password = os.getenv("ENEVERRE_ADMIN_PASS", "eneverre")

        print(f"[INIT] No users found, creating admin: {username}")

        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, generate_password_hash(password), "admin")
        )

        conn.commit()
    else:
        print(f"[INIT] Users already exist ({count}), skipping initialization")

    if first_time:
        print("[INIT] First run - database created")

    conn.close()
