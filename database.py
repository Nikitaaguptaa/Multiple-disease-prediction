import sqlite3
import hashlib

# ---------- DB CONNECT ----------
def create_users_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# ---------- PASSWORD HASH ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- SIGNUP ----------
def add_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users VALUES (?, ?)", 
                  (username, hash_password(password)))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

# ---------- LOGIN CHECK ----------
def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))

    data = c.fetchone()
    conn.close()

    return data is not None

# history table (user ke records)
def create_history_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            username TEXT,
            disease TEXT,
            result TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_history(username, disease, result):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("INSERT INTO history VALUES (?, ?, ?)",
              (username, disease, result))

    conn.commit()
    conn.close()


def get_history(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT disease, result FROM history WHERE username=?",
              (username,))

    data = c.fetchall()
    conn.close()
    return data