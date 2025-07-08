# auth.py

import bcrypt
import sqlite3
import streamlit as st

DB_PATH = "feelwrite.db"

# --- DB Setup ---
def create_user_table():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')

# --- Signup ---
def signup_user(name, username, password):
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT INTO users (name, username, password) VALUES (?, ?, ?)", 
                         (name, username, hashed_pw))
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists

# --- Login ---
def login_user(username, password):
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if result and bcrypt.checkpw(password.encode(), result[3].encode()):
            return {"id": result[0], "name": result[1], "username": result[2]}
    return None

# --- Session ---
def is_logged_in():
    return st.session_state.get("user") is not None

def logout_user():
    st.session_state["user"] = None
