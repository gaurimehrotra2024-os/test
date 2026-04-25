from flask import Flask, request, session
import sqlite3
import os
import pickle
import random

app = Flask(__name__)
app.secret_key = "hardcoded-secret-key"   # Vulnerability: hardcoded secret

# ---------------------------
# Database setup
# ---------------------------
def get_db():
    conn = sqlite3.connect("users.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT
        )
    """)

    conn.execute("""
        INSERT OR IGNORE INTO users
        VALUES (1, 'admin', 'supersecret123', 'admin')
    """)

    conn.commit()
    return conn


# ---------------------------
# SQL Injection Vulnerability
# ---------------------------
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = get_db()

    query = f"""
        SELECT * FROM users
        WHERE username = '{username}'
        AND password = '{password}'
    """

    print("Executing:", query)

    cursor = conn.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        session["user"] = user[1]

        # Weak session token vulnerability
        session["token"] = str(random.randint(1000, 9999))

        return f"Logged in as {user[1]}"
    
    return "Login failed"


# ---------------------------
# Broken Access Control
# ---------------------------
@app.route("/admin/delete_user")
def delete_user():
    user_id = request.args.get("id")

    conn = get_db()

    # No authorization check
    conn.execute(f"DELETE FROM users WHERE id = {user_id}")
    conn.commit()
    conn.close()

    return "User deleted"


# ---------------------------
# Command Injection
# ---------------------------
@app.route("/backup")
def backup():
    filename = request.args.get("file")

    command = f"cp users.db backups/{filename}"

    print("Running command:", command)

    os.system(command)

    return "Backup complete"


# ---------------------------
# Path Traversal
# ---------------------------
@app.route("/read")
def read_file():
    filename = request.args.get("file")

    with open(f"uploads/{filename}", "r") as f:
        return f.read()


# ---------------------------
# Insecure Deserialization
# ---------------------------
@app.route("/load_profile", methods=["POST"])
def load_profile():
    data = request.data

    profile = pickle.loads(data)

    return f"Loaded profile: {profile}"


# ---------------------------
# User lookup SQL injection
# ---------------------------
@app.route("/user")
def get_user():
    user_id = request.args.get("id")

    conn = get_db()

    cursor = conn.execute(
        f"SELECT * FROM users WHERE id = {user_id}"
    )

    user = cursor.fetchone()
    conn.close()

    return str(user)


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("backups", exist_ok=True)

    app.run(debug=True)