import sqlite3

def get_db():
    conn = sqlite3.connect("users.db")
    conn.execute(""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT DEFAULT 'user'
        )
    "")
    conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'supersecret123', 'admin')")
    conn.commit()
    return conn


def login(username: str, password: str):
    conn = get_db()
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor = conn.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    return user


def get_user(user_id: int):
    conn = get_db()
    cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user