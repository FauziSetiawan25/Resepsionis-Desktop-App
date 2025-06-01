import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "auth_db.db")

def init_auth_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        hospital TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def check_credentials(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT hospital FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]  # return hospital name
    return None

def add_user(username, password, hospital):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, hospital) VALUES (?, ?, ?)", (username, password, hospital))
    conn.commit()
    conn.close()